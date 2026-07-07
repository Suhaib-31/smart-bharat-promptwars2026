/**
 * Smart Bharat - AI Civic Assistant Chat Logic
 * Handles sending messages, rendering markdown responses, voice input/output,
 * language switching, and local chat history.
 */

(function () {
  const chatWindow = document.getElementById("chat-window");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const langSelect = document.getElementById("lang-select");
  const micBtn = document.getElementById("mic-btn");
  const sendBtn = document.getElementById("send-btn");

  if (!chatForm) return; // not on chat page

  let conversationHistory = [];
  let speechEnabled = false;

  const suggestedPrompts = document.querySelectorAll("[data-suggested-prompt]");

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function renderMarkdown(text) {
    if (window.marked) {
      return window.marked.parse(text);
    }
    return text.replace(/\n/g, "<br>");
  }

  function appendMessage(role, text, animate = true) {
    const wrapper = document.createElement("div");
    wrapper.className = `flex w-full ${role === "user" ? "justify-end" : "justify-start"} ${animate ? "fade-in-up" : ""}`;

    if (role === "user") {
      wrapper.innerHTML = `
        <div class="chat-bubble-user px-4 py-3 max-w-[85%] md:max-w-[70%] shadow-md">
          <p class="text-sm md:text-base whitespace-pre-wrap">${escapeHtml(text)}</p>
        </div>`;
    } else {
      const msgId = "msg-" + Date.now() + Math.floor(Math.random() * 1000);
      wrapper.innerHTML = `
        <div class="chat-bubble-ai glass-card px-4 py-3 max-w-[85%] md:max-w-[70%] text-gray-800 dark:text-gray-100">
          <div class="flex items-center gap-2 mb-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Smart Bharat AI
          </div>
          <div id="${msgId}" class="markdown-content text-sm md:text-base leading-relaxed">${renderMarkdown(text)}</div>
          <div class="flex items-center gap-3 mt-2 pt-2 border-t border-gray-200/50 dark:border-gray-700/50">
            <button data-copy-target="${msgId}" class="flex items-center gap-1 text-xs text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 transition">
              <i data-lucide="copy" class="w-3.5 h-3.5"></i><span>Copy</span>
            </button>
            <button data-speak-target="${msgId}" class="flex items-center gap-1 text-xs text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 transition">
              <i data-lucide="volume-2" class="w-3.5 h-3.5"></i><span>Listen</span>
            </button>
          </div>
        </div>`;
    }
    chatWindow.appendChild(wrapper);
    if (window.lucide) window.lucide.createIcons();
    attachDynamicListeners(wrapper);
    scrollToBottom();
  }

  function attachDynamicListeners(scope) {
    scope.querySelectorAll("[data-copy-target]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = document.getElementById(btn.getAttribute("data-copy-target"));
        if (!target) return;
        navigator.clipboard.writeText(target.innerText);
        const span = btn.querySelector("span");
        const original = span.textContent;
        span.textContent = "Copied!";
        setTimeout(() => (span.textContent = original), 1500);
      });
    });
    scope.querySelectorAll("[data-speak-target]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = document.getElementById(btn.getAttribute("data-speak-target"));
        if (!target) return;
        speak(target.innerText);
      });
    });
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function showTypingIndicator() {
    const wrapper = document.createElement("div");
    wrapper.id = "typing-indicator";
    wrapper.className = "flex justify-start fade-in-up";
    wrapper.innerHTML = `
      <div class="chat-bubble-ai glass-card px-4 py-3 text-gray-500 dark:text-gray-300">
        <span class="typing-indicator"><span></span><span></span><span></span></span>
      </div>`;
    chatWindow.appendChild(wrapper);
    scrollToBottom();
  }

  function removeTypingIndicator() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
  }

  function speak(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text.replace(/[#*_`]/g, ""));
    utterance.lang = langSelect && langSelect.value === "hi" ? "hi-IN" : "en-IN";
    window.speechSynthesis.speak(utterance);
  }

  async function sendMessage(message) {
    if (!message.trim()) return;
    appendMessage("user", message);
    conversationHistory.push({ role: "user", text: message });
    saveHistoryLocal(message, "user");

    chatInput.value = "";
    sendBtn.disabled = true;
    showTypingIndicator();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          language: langSelect ? langSelect.value : "en",
          history: conversationHistory.slice(-10),
        }),
      });
      const data = await res.json();
      removeTypingIndicator();

      if (data.success) {
        appendMessage("ai", data.response);
        conversationHistory.push({ role: "model", text: data.response });
        saveHistoryLocal(data.response, "ai");
      } else {
        appendMessage("ai", `⚠️ ${data.error || "Something went wrong. Please try again."}`);
      }
    } catch (err) {
      removeTypingIndicator();
      appendMessage("ai", "⚠️ Network error. Please check your connection and try again.");
    } finally {
      sendBtn.disabled = false;
    }
  }

  function saveHistoryLocal(text, role) {
    try {
      const key = "smart-bharat-chat-history";
      const existing = JSON.parse(localStorage.getItem(key) || "[]");
      existing.push({ role, text, ts: Date.now() });
      localStorage.setItem(key, JSON.stringify(existing.slice(-50)));
    } catch (e) {
      /* ignore storage errors */
    }
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(chatInput.value);
  });

  suggestedPrompts.forEach((btn) => {
    btn.addEventListener("click", () => {
      sendMessage(btn.getAttribute("data-suggested-prompt"));
    });
  });

  // Voice Input (Web Speech API)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (micBtn) {
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;

      micBtn.addEventListener("click", () => {
        recognition.lang = langSelect && langSelect.value === "hi" ? "hi-IN" : "en-IN";
        micBtn.classList.add("text-red-500", "animate-pulse");
        recognition.start();
      });

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        micBtn.classList.remove("text-red-500", "animate-pulse");
      };
      recognition.onerror = () => micBtn.classList.remove("text-red-500", "animate-pulse");
      recognition.onend = () => micBtn.classList.remove("text-red-500", "animate-pulse");
    } else {
      micBtn.style.display = "none";
    }
  }

  scrollToBottom();
})();
