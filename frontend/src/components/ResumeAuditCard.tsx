import React from "react";
import { CheckCircle, Lightbulb, FileCheck, Download } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface ResumeAuditCardProps {
  audit: {
    impact_score?: number;
    metrics_detected?: number;
    strengths?: string[];
    actionable_recommendations?: string[];
    readiness_rating?: string;
  };
  onExportReport: () => void;
}

export function ResumeAuditCard({ audit, onExportReport }: ResumeAuditCardProps) {
  if (!audit || !audit.impact_score) return null;

  return (
    <div className="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a] p-5 shadow-[0_2px_12px_rgba(0,0,0,0.02)] space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <FileCheck size={18} className="text-[#0071e3]" />
          <div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white">
              Resume Feedback
            </h4>
            <span className="text-[11px] text-slate-500 dark:text-slate-400">
              Review of what is strong and what can be improved.
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Badge
            variant={audit.readiness_rating === "Competitive" ? "success" : "warning"}
            className="text-[10px]"
          >
            {audit.readiness_rating}
          </Badge>
          <Button variant="outline" size="sm" onClick={onExportReport} className="text-[11px]">
            <Download size={13} className="mr-1" />
            Export report
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        {/* Strengths */}
        <div className="space-y-2 rounded-xl border border-emerald-500/15 bg-emerald-50/40 dark:bg-emerald-500/5 p-3.5">
          <div className="flex items-center space-x-1.5 text-emerald-700 dark:text-emerald-400 font-semibold">
            <CheckCircle size={14} />
            <span>What looks good</span>
          </div>
          <ul className="space-y-1.5 text-slate-700 dark:text-slate-300">
            {audit.strengths?.map((str, idx) => (
              <li key={idx} className="flex items-start space-x-1.5 leading-relaxed">
                <span className="text-emerald-500 font-bold">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div className="space-y-2 rounded-xl border border-amber-500/15 bg-amber-50/40 dark:bg-amber-500/5 p-3.5">
          <div className="flex items-center space-x-1.5 text-amber-700 dark:text-amber-400 font-semibold">
            <Lightbulb size={14} />
            <span>Suggestions to improve</span>
          </div>
          <ul className="space-y-1.5 text-slate-700 dark:text-slate-300">
            {audit.actionable_recommendations?.map((rec, idx) => (
              <li key={idx} className="flex items-start space-x-1.5 leading-relaxed">
                <span className="text-amber-500 font-bold">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
