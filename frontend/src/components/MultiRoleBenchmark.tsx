import React from "react";
import { ArrowUpRight, CheckCircle2, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface MultiRoleBenchmarkProps {
  benchmarks: Array<{
    role: string;
    match_percentage: number;
    top_matched: string[];
    top_missing: string[];
  }>;
  onSelectRole: (role: string) => void;
}

export function MultiRoleBenchmark({ benchmarks, onSelectRole }: MultiRoleBenchmarkProps) {
  if (!benchmarks || benchmarks.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          Adjacent role benchmark matrix
        </h4>
        <span className="text-[11px] text-slate-400 dark:text-slate-500">
          Multi-track qualification benchmark
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {benchmarks.map((item) => (
          <div
            key={item.role}
            className="flex flex-col justify-between rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a] p-4 transition-all hover:border-[#0071e3]/60 shadow-[0_2px_8px_rgba(0,0,0,0.02)]"
          >
            <div>
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h5 className="text-xs font-bold text-slate-900 dark:text-white">
                    {item.role}
                  </h5>
                  <span className="text-[11px] font-mono tabular-nums text-slate-500 dark:text-slate-400">
                    {item.match_percentage}% compatibility
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => onSelectRole(item.role)}
                  className="rounded-lg p-1 text-slate-400 hover:text-[#0071e3] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  title={`Switch evaluation to ${item.role}`}
                >
                  <ArrowUpRight size={16} />
                </button>
              </div>

              <ProgressBar
                value={item.match_percentage}
                indicatorClassName={
                  item.match_percentage >= 70
                    ? "bg-[#28cd41]"
                    : item.match_percentage >= 40
                    ? "bg-[#ff9f0a]"
                    : "bg-[#ff3b30]"
                }
              />
            </div>

            <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/80 space-y-1.5 text-[11px]">
              <div className="flex items-center space-x-1.5 text-slate-600 dark:text-slate-300">
                <CheckCircle2 size={12} className="text-emerald-500 shrink-0" />
                <span className="truncate">
                  {item.top_matched?.slice(0, 2).join(", ") || "None"}
                </span>
              </div>
              <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400">
                <AlertCircle size={12} className="text-rose-500 shrink-0" />
                <span className="truncate">
                  Gaps: {item.top_missing?.slice(0, 2).join(", ") || "None"}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
