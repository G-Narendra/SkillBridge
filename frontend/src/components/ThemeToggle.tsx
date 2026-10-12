import React, { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";

export function ThemeToggle() {
  const [isDark, setIsDark] = useState<boolean>(false);

  useEffect(() => {
    // Check local storage or system preference
    const saved = localStorage.getItem("skillbridge-theme");
    if (saved === "dark") {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    } else if (saved === "light") {
      setIsDark(false);
      document.documentElement.classList.remove("dark");
    } else {
      // Default to Apple light mode as requested
      setIsDark(false);
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const toggleTheme = () => {
    const nextDark = !isDark;
    setIsDark(nextDark);
    if (nextDark) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("skillbridge-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("skillbridge-theme", "light");
    }
  };

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label="Toggle theme appearance"
      className="flex items-center space-x-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] px-2.5 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-300 shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800/80 transition-all select-none"
    >
      {isDark ? (
        <>
          <Sun size={14} className="text-amber-400" />
          <span className="hidden sm:inline">Light</span>
        </>
      ) : (
        <>
          <Moon size={14} className="text-slate-600" />
          <span className="hidden sm:inline">Dark</span>
        </>
      )}
    </button>
  );
}
