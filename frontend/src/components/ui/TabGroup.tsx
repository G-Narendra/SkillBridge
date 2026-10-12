import React, { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export interface TabItem {
  id: string;
  label: string;
  count?: number;
}

interface TabGroupProps {
  tabs: TabItem[];
  value?: string;
  defaultTab?: string;
  onChange?: (tabId: string) => void;
  className?: string;
}

export function TabGroup({
  tabs,
  value,
  defaultTab,
  onChange,
  className
}: TabGroupProps) {
  const [internalTab, setInternalTab] = useState(value || defaultTab || tabs[0]?.id || "");

  useEffect(() => {
    if (value !== undefined) {
      setInternalTab(value);
    }
  }, [value]);

  const activeTab = value !== undefined ? value : internalTab;

  const handleTabClick = (tabId: string) => {
    if (value === undefined) {
      setInternalTab(tabId);
    }
    if (onChange) {
      onChange(tabId);
    }
  };

  return (
    <div
      role="tablist"
      aria-label="Category filters"
      className={cn(
        "flex items-center space-x-1 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100/80 dark:bg-[#0f172a]/90 p-1 backdrop-blur-md transition-colors",
        className
      )}
    >
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            tabIndex={isActive ? 0 : -1}
            onClick={() => handleTabClick(tab.id)}
            className={cn(
              "flex items-center justify-center rounded-lg px-3 py-1.5 text-xs font-medium transition-all focus:outline-none focus:ring-2 focus:ring-[#0071e3]",
              isActive
                ? "bg-white dark:bg-[#0071e3] text-slate-900 dark:text-white shadow-sm font-semibold"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-white/50 dark:hover:bg-slate-800/60"
            )}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span
                className={cn(
                  "ml-1.5 rounded px-1.5 py-0.2 text-[10px] font-mono tabular-nums",
                  isActive
                    ? "bg-slate-200 dark:bg-white/20 text-slate-800 dark:text-white"
                    : "bg-slate-200/80 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
                )}
              >
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
