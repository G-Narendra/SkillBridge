import React, { useState, useRef, useEffect } from "react";
import { ChevronDown, Search, Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface RoleComboboxProps {
  value: string;
  onChange: (value: string) => void;
  options: string[];
  className?: string;
}

export function RoleCombobox({ value, onChange, options, className }: RoleComboboxProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);

  const filteredOptions = options.filter((option) =>
    option.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (option: string) => {
    onChange(option);
    setSearchTerm("");
    setIsOpen(false);
  };

  const handleCustomInput = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchTerm.trim()) {
      onChange(searchTerm.trim());
      setSearchTerm("");
      setIsOpen(false);
    }
  };

  return (
    <div ref={containerRef} className={cn("relative w-full", className)}>
      <div
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-controls="role-listbox"
        tabIndex={0}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            setIsOpen(!isOpen);
          }
        }}
        className="flex w-full cursor-pointer items-center justify-between rounded-xl border border-slate-300 dark:border-slate-800 bg-white dark:bg-[#0f172a] px-3.5 py-2.5 text-xs sm:text-sm text-slate-800 dark:text-slate-100 transition-colors hover:border-slate-400 dark:hover:border-slate-700 focus:border-[#0071e3] focus:outline-none focus:ring-1 focus:ring-[#0071e3]"
      >
        <span className="truncate font-medium">{value || "Select target technology role"}</span>
        <ChevronDown size={16} className={cn("text-slate-400 transition-transform", isOpen && "rotate-180")} />
      </div>

      {isOpen && (
        <div
          id="role-listbox"
          className="absolute left-0 right-0 top-full z-50 mt-1 max-h-64 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] shadow-2xl backdrop-blur-md"
        >
          <div className="flex items-center border-b border-slate-100 dark:border-slate-800 px-3 py-2">
            <Search size={14} className="mr-2 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={handleCustomInput}
              placeholder="Search or enter custom role..."
              className="w-full bg-transparent text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none"
              autoFocus
            />
          </div>

          <div role="listbox" className="max-h-52 overflow-y-auto p-1 text-sm">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <div
                  key={option}
                  role="option"
                  aria-selected={value === option}
                  onClick={() => handleSelect(option)}
                  className={cn(
                    "flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-xs transition-colors",
                    value === option
                      ? "bg-[#0071e3]/15 text-[#0071e3] font-medium"
                      : "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white"
                  )}
                >
                  <span>{option}</span>
                  {value === option && <Check size={14} className="text-[#0071e3]" />}
                </div>
              ))
            ) : (
              <div className="p-3 text-center">
                <p className="text-xs text-slate-500 mb-2">No standard role matches query.</p>
                {searchTerm.trim() && (
                  <button
                    type="button"
                    onClick={() => handleSelect(searchTerm.trim())}
                    className="w-full rounded-lg bg-[#0071e3]/15 px-2 py-1 text-xs text-[#0071e3] hover:bg-[#0071e3]/25 font-medium"
                  >
                    Use custom: &quot;{searchTerm.trim()}&quot;
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
