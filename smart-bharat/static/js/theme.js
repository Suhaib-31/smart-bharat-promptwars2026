/**
 * Smart Bharat - Theme Switcher
 * Handles Dark/Light mode toggle with localStorage persistence.
 */

(function () {
  const root = document.documentElement;
  const STORAGE_KEY = "smart-bharat-theme";

  function applyTheme(theme) {
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    updateToggleIcons(theme);
  }

  function updateToggleIcons(theme) {
    document.querySelectorAll("[data-theme-icon-dark]").forEach((el) => {
      el.classList.toggle("hidden", theme !== "light");
    });
    document.querySelectorAll("[data-theme-icon-light]").forEach((el) => {
      el.classList.toggle("hidden", theme !== "dark");
    });
  }

  function getStoredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function toggleTheme() {
    const current = root.classList.contains("dark") ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  }

  // Apply theme immediately on load
  applyTheme(getStoredTheme());

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", toggleTheme);
    });
    if (window.lucide) window.lucide.createIcons();
  });
})();
