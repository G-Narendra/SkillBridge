import React from "react";
import { AlertCircle, Target, ArrowRight } from "lucide-react";
import { Badge } from "./ui/Badge";

export interface CompetencyGapItem {
  skill: string;
  tier: string;
  tier_label?: string;
  current_proficiency: number;
  required_benchmark: number;
  deficit_delta: number;
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | string;
  pedagogical_reasoning: string;
  actionable_recommendation?: string;
}

interface GapDiagnosticTableProps {
  gaps: CompetencyGapItem[];
  targetRole: string;
}

export const GapDiagnosticTable: React.FC<GapDiagnosticTableProps> = ({ gaps, targetRole }) => {
  if (!gaps || gaps.length === 0) {
    return (
      <div className="rounded-2xl border border-emerald-500/20 bg-emerald-50/50 dark:bg-emerald-500/10 p-5 text-center text-xs text-emerald-800 dark:text-emerald-300">
        <h4 className="font-semibold text-sm mb-1">All Required Skills Matched</h4>
        <p>Your technical qualifications cover all evaluated competencies for {targetRole}.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-1.5">
            <AlertCircle size={15} className="text-amber-500 inline" />
            <span>Identified Skill Gaps</span>
          </h4>
          <span className="text-[11px] text-slate-500 dark:text-slate-400">
            Prioritized skills for this role with clear engineering rationale
          </span>
        </div>
        <span className="text-xs font-mono font-medium text-slate-600 dark:text-slate-300">
          {gaps.length} Skill {gaps.length === 1 ? "Gap" : "Gaps"}
        </span>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a]/80 shadow-sm">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/60 text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
              <th className="py-3 px-4">Skill Requirement</th>
              <th className="py-3 px-3">Category</th>
              <th className="py-3 px-3 text-center">Target Benchmark</th>
              <th className="py-3 px-3 text-center">Priority</th>
              <th className="py-3 px-4">Why This Skill Matters</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">
            {gaps.map((gap, idx) => {
              const priority = gap.priority?.toUpperCase() || "MEDIUM";
              const priorityVariant =
                priority === "CRITICAL"
                  ? "destructive"
                  : priority === "HIGH"
                  ? "outline"
                  : "secondary";

              return (
                <tr
                  key={`${gap.skill}-${idx}`}
                  className="hover:bg-slate-50/50 dark:hover:bg-[#1e293b]/30 transition-colors"
                >
                  <td className="py-3 px-4 font-mono font-semibold text-slate-900 dark:text-slate-100">
                    {gap.skill}
                  </td>
                  <td className="py-3 px-3">
                    <span className="inline-block rounded-md bg-slate-100 dark:bg-[#1e293b] px-2 py-0.5 text-[10px] font-medium text-slate-700 dark:text-slate-300 capitalize">
                      {gap.tier_label || gap.tier}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-center font-mono font-bold text-amber-600 dark:text-amber-400">
                    +{gap.deficit_delta ? gap.deficit_delta.toFixed(0) : "85"}%
                  </td>
                  <td className="py-3 px-3 text-center">
                    <Badge variant={priorityVariant as any} className="text-[10px] uppercase font-mono px-2 py-0.5">
                      {priority}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                    {gap.pedagogical_reasoning}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
