import React from "react";
import { CheckCircle2, XCircle, Code2, Layers, Database, Wrench } from "lucide-react";
import { Badge } from "./ui/Badge";
import { ProgressBar } from "./ui/ProgressBar";

interface CategoryData {
  tier_label?: string;
  matched: string[];
  missing: string[];
  percentage: number;
  total_required: number;
  weight?: number;
}

interface GranularCapabilityGridProps {
  breakdown: Record<string, CategoryData>;
}

export const GranularCapabilityGrid: React.FC<GranularCapabilityGridProps> = ({ breakdown }) => {
  const tiers = [
    {
      key: "languages",
      title: "Languages",
      weightLabel: "40% weight",
      icon: Code2,
      color: "blue",
    },
    {
      key: "frameworks",
      title: "Frameworks",
      weightLabel: "30% weight",
      icon: Layers,
      color: "purple",
    },
    {
      key: "databases",
      title: "Databases",
      weightLabel: "20% weight",
      icon: Database,
      color: "emerald",
    },
    {
      key: "tools",
      altKey: "tools_infrastructure",
      title: "Tools & Infrastructure",
      weightLabel: "10% weight",
      icon: Wrench,
      color: "amber",
    },
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-bold text-slate-900 dark:text-white tracking-tight flex items-center">
          <span>4-Tier Technical Competency Distribution</span>
        </h4>
        <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
          Evaluated against 4 canonical skill categories
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {tiers.map((tier) => {
          const data = breakdown[tier.key] || (tier.altKey ? breakdown[tier.altKey] : null) || {
            matched: [],
            missing: [],
            percentage: 100,
            total_required: 0,
          };

          const matchedList = data.matched || [];
          const missingList = data.missing || [];
          const Icon = tier.icon;
          const percentage = data.percentage ?? 100;

          return (
            <div
              key={tier.key}
              className="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/70 p-4 flex flex-col justify-between shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3.5"
            >
              {/* Header */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center space-x-2">
                    <div className="rounded-lg bg-slate-100 dark:bg-[#1e293b] p-1.5 text-slate-700 dark:text-slate-300">
                      <Icon size={14} />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-900 dark:text-white block leading-tight">
                        {tier.title}
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">{tier.weightLabel}</span>
                    </div>
                  </div>
                  <span className="text-sm font-mono font-bold text-slate-900 dark:text-slate-100 tabular-nums">
                    {percentage}%
                  </span>
                </div>
                <ProgressBar
                  value={percentage}
                  indicatorClassName={
                    percentage >= 70
                      ? "bg-emerald-500"
                      : percentage >= 40
                      ? "bg-amber-500"
                      : "bg-rose-500"
                  }
                />
              </div>

              {/* Skills breakdown */}
              <div className="space-y-2.5 pt-1 text-xs">
                {/* Verified Skills */}
                <div>
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 flex items-center mb-1">
                    <CheckCircle2 size={11} className="mr-1 inline text-emerald-500" />
                    Verified ({matchedList.length})
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {matchedList.length > 0 ? (
                      matchedList.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center rounded-md border border-emerald-500/20 bg-emerald-50 dark:bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-800 dark:text-emerald-300 font-mono"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-[11px] text-slate-400 italic">None verified in CV</span>
                    )}
                  </div>
                </div>

                {/* Missing Benchmark Gaps */}
                <div>
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center mb-1">
                    <XCircle size={11} className="mr-1 inline text-rose-500" />
                    Missing Gaps ({missingList.length})
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {missingList.length > 0 ? (
                      missingList.map((skill) => (
                        <span
                          key={skill}
                          className="inline-flex items-center rounded-md border border-rose-500/20 bg-rose-50 dark:bg-rose-500/10 px-2 py-0.5 text-[11px] font-medium text-rose-800 dark:text-rose-300 font-mono"
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium">
                        All tier requirements met
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
