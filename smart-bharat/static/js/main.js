/**
 * Smart Bharat - Main JS
 * Shared UI behaviors: mobile nav toggle, flash message dismissal,
 * copy-to-clipboard buttons, reveal-on-scroll animations.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Mobile nav toggle
  const navToggle = document.getElementById("nav-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  if (navToggle && mobileMenu) {
    navToggle.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // Auto-dismiss flash messages
  document.querySelectorAll("[data-flash]").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.5s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    }, 4500);
  });

  // Generic copy-to-clipboard buttons
  document.querySelectorAll("[data-copy-target]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-copy-target");
      const target = document.getElementById(targetId);
      if (!target) return;
      const text = target.innerText || target.value || "";
      navigator.clipboard.writeText(text).then(() => {
        const original = btn.innerHTML;
        btn.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i><span>Copied!</span>';
        if (window.lucide) window.lucide.createIcons();
        setTimeout(() => {
          btn.innerHTML = original;
          if (window.lucide) window.lucide.createIcons();
        }, 1800);
      });
    });
  });

  // Reveal-on-scroll
  const revealEls = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in-up");
          entry.target.style.opacity = "1";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  revealEls.forEach((el) => {
    el.style.opacity = "0";
    observer.observe(el);
  });

  if (window.lucide) window.lucide.createIcons();
});
