import React from "react";
import { Scale, Users, Target, CheckCircle2 } from "lucide-react";
import { Badge } from "./ui/Badge";

interface BenchmarkComparisonBannerProps {
  role: string;
  benchmarkStandard?: {
    standard_name?: string;
    sample_size?: string;
    comparison_source?: string;
    percentile_threshold?: number;
  };
  overallMatch: number;
  deficitDelta: number;
}

export const BenchmarkComparisonBanner: React.FC<BenchmarkComparisonBannerProps> = ({
  role,
  benchmarkStandard,
  overallMatch,
  deficitDelta,
}) => {
  const standardName = benchmarkStandard?.standard_name || `Tier-1 Tech Mid-Level ${role} Industry Baseline`;
  const sampleSize = benchmarkStandard?.sample_size || "Aggregated from 5,420+ Tier-1 Tech Job Descriptions";

  return (
    <div className="rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-50/80 via-slate-50/70 to-indigo-50/60 dark:from-[#0071e3]/10 dark:via-[#1e293b]/60 dark:to-indigo-950/20 p-5 shadow-sm">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <span className="flex items-center text-xs font-semibold uppercase tracking-wider text-[#0071e3] dark:text-[#3898ec]">
              <Scale size={14} className="mr-1.5" />
              Benchmark Standard
            </span>
            <Badge variant="default" className="text-[10px] font-mono">
              Tier-1 Tech Baseline
            </Badge>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            {standardName}
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-300 flex items-center">
            <Users size={13} className="mr-1.5 text-slate-400 shrink-0" />
            <span>Compared with: <strong className="font-medium text-slate-800 dark:text-slate-200">{sampleSize}</strong></span>
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0 pt-2 lg:pt-0 border-t lg:border-t-0 border-slate-200 dark:border-slate-800">
          <div className="rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white/80 dark:bg-[#0f172a]/80 px-3.5 py-2 text-center">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block">Your Match Score</span>
            <span className="text-xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
              {overallMatch}%
            </span>
          </div>
          <div className="rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white/80 dark:bg-[#0f172a]/80 px-3.5 py-2 text-center">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block">Skill Gap</span>
            <span className="text-xl font-bold font-mono text-amber-600 dark:text-amber-400">
              {typeof deficitDelta === "number" ? deficitDelta.toFixed(1) : "0.0"}%
            </span>
          </div>
          <div className="rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white/80 dark:bg-[#0f172a]/80 px-3.5 py-2 text-center hidden sm:block">
            <span className="text-[10px] uppercase font-semibold text-slate-400 block">Target Benchmark</span>
            <span className="text-xl font-bold font-mono text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <Target size={14} className="mr-1 inline text-blue-500" />
              80%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
