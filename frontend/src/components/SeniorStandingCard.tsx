"use client";

import React, { useState } from "react";
import {
  Award,
  CheckCircle2,
  HelpCircle,
  Sparkles,
  ChevronDown,
  ChevronUp,
  FileCheck2,
  ShieldCheck,
  Cpu,
  Layers,
  ArrowRight
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface DefenseTopic {
  topic: string;
  focus: string;
  sample_question: string;
}

interface SeniorStandingProps {
  seniorStanding: {
    is_senior_qualified: boolean;
    readiness_status: string;
    match_percentage: number;
    senior_summary: string;
    interview_defense_topics?: DefenseTopic[];
    portfolio_polish_recommendations?: string[];
  };
  targetRole: string;
  onOpenPortfolioCard?: () => void;
  onExportReport?: () => void;
}

export function SeniorStandingCard({
  seniorStanding,
  targetRole,
  onOpenPortfolioCard,
  onExportReport
}: SeniorStandingProps) {
  const [expandedTopic, setExpandedTopic] = useState<number | null>(0);

  const topics = seniorStanding.interview_defense_topics || [];
  const polishRecs = seniorStanding.portfolio_polish_recommendations || [];

  return (
    <Card className="border-emerald-300/80 dark:border-emerald-600/40 bg-gradient-to-br from-emerald-50/50 via-white to-emerald-50/20 dark:from-emerald-950/20 dark:via-[#0f172a] dark:to-emerald-950/10 shadow-[0_4px_24px_rgba(16,185,129,0.06)] overflow-hidden">
      <CardHeader className="pb-4 border-b border-emerald-100 dark:border-emerald-900/30">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex items-center space-x-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-500 text-white shadow-md shadow-emerald-500/20">
              <Award size={24} />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <CardTitle className="text-lg font-bold text-slate-900 dark:text-white">
                  Portfolio Calibrated: Senior Standing
                </CardTitle>
                <Badge variant="success" className="text-[11px] font-semibold bg-emerald-600 text-white border-0">
                  {seniorStanding.readiness_status || "Interview Ready"}
                </Badge>
              </div>
              <CardDescription className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                Target Role: <strong className="font-semibold text-slate-800 dark:text-slate-200">{targetRole}</strong> &bull; Match: <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{seniorStanding.match_percentage}%</span>
              </CardDescription>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto">
            {onOpenPortfolioCard && (
              <Button
                variant="primary"
                size="sm"
                onClick={onOpenPortfolioCard}
                className="text-xs bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm"
              >
                <ShieldCheck size={14} className="mr-1.5" />
                15s Portfolio Card
              </Button>
            )}
            {onExportReport && (
              <Button variant="outline" size="sm" onClick={onExportReport} className="text-xs">
                Export Audit
              </Button>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-5 space-y-6">
        {/* Core Senior Verdict Banner */}
        <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-emerald-50/70 dark:bg-emerald-950/30 p-4">
          <div className="flex items-start space-x-3">
            <CheckCircle2 size={18} className="text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <p className="font-semibold text-emerald-900 dark:text-emerald-200">
                Zero Bridging Projects Required
              </p>
              <p className="text-emerald-800/90 dark:text-emerald-300/80 leading-relaxed">
                {seniorStanding.senior_summary ||
                  `Outstanding technical match (${seniorStanding.match_percentage}%). Candidate demonstrates comprehensive mastery of core competencies for ${targetRole}. Standard starter projects are suppressed; focus is shifted to staff-level interview defense and architecture polish.`}
              </p>
            </div>
          </div>
        </div>

        {/* 2-Column Senior Preparation Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Column 1: Staff-Level Interview Defense */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Cpu size={16} className="text-[#0071e3]" />
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                Senior Technical Defense Questions ({topics.length})
              </h4>
            </div>

            <div className="space-y-2.5">
              {topics.map((t, idx) => {
                const isExpanded = expandedTopic === idx;
                return (
                  <div
                    key={idx}
                    className="rounded-xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/70 transition-all overflow-hidden"
                  >
                    <button
                      type="button"
                      onClick={() => setExpandedTopic(isExpanded ? null : idx)}
                      className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-50 dark:hover:bg-[#1e293b]/50 transition-colors"
                    >
                      <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                        {idx + 1}. {t.topic}
                      </span>
                      {isExpanded ? (
                        <ChevronUp size={14} className="text-slate-400" />
                      ) : (
                        <ChevronDown size={14} className="text-slate-400" />
                      )}
                    </button>
                    {isExpanded && (
                      <div className="px-3 pb-3 pt-1 space-y-2 text-xs border-t border-slate-100 dark:border-slate-800/70 bg-slate-50/50 dark:bg-[#1e293b]/20">
                        <div>
                          <span className="text-[10px] font-bold uppercase text-slate-400 block mb-0.5">
                            Key Architectural Focus
                          </span>
                          <p className="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                            {t.focus}
                          </p>
                        </div>
                        <div className="rounded-lg bg-white dark:bg-[#090d16] p-2.5 border border-slate-200/60 dark:border-slate-800">
                          <span className="text-[10px] font-bold uppercase text-amber-600 dark:text-amber-400 block mb-0.5">
                            Expected Interview Defense Prompt
                          </span>
                          <p className="text-[11px] font-mono text-slate-700 dark:text-slate-300 leading-snug">
                            &ldquo;{t.sample_question}&rdquo;
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Column 2: Portfolio Polish Recommendations */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Sparkles size={16} className="text-amber-500" />
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                Staff Portfolio Polish Checklist ({polishRecs.length})
              </h4>
            </div>

            <div className="rounded-xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/70 p-3.5 space-y-2.5">
              {polishRecs.map((rec, idx) => (
                <div key={idx} className="flex items-start space-x-2.5 text-xs text-slate-600 dark:text-slate-300">
                  <FileCheck2 size={15} className="text-emerald-500 shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{rec}</span>
                </div>
              ))}
            </div>

            <div className="rounded-xl border border-blue-200/80 dark:border-blue-900/40 bg-blue-50/60 dark:bg-blue-950/20 p-3 flex items-center justify-between text-xs">
              <span className="text-blue-900 dark:text-blue-300 font-medium">
                Ready for verified hiring review?
              </span>
              {onOpenPortfolioCard && (
                <button
                  type="button"
                  onClick={onOpenPortfolioCard}
                  className="inline-flex items-center text-xs font-semibold text-[#0071e3] hover:underline"
                >
                  View Digital Card <ArrowRight size={12} className="ml-1" />
                </button>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
