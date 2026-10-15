import React from "react";
import {
  CheckCircle2,
  XCircle,
  Code2,
  Layers,
  Database,
  Wrench,
  Cloud,
  Server,
  Terminal,
  Activity,
  Palette,
  Cpu,
  Shield,
  Smartphone,
  Sparkles,
  Info
} from "lucide-react";
import { Badge } from "./ui/Badge";
import { ProgressBar } from "./ui/ProgressBar";

export interface DimensionData {
  id: string;
  label: string;
  icon?: string;
  weight: number;
  percentage: number;
  matched: string[];
  missing: string[];
  total_required: number;
  deficit?: number;
}

export interface CategoryData {
  tier_label?: string;
  label?: string;
  icon?: string;
  dimension_id?: string;
  matched: string[];
  missing: string[];
  percentage: number;
  total_required: number;
  weight?: number;
  is_omitted?: boolean;
  rationale?: string;
}

export interface ArchetypeMetadata {
  id: string;
  name: string;
  rationale: string;
  omitted_metrics: string[];
}

interface GranularCapabilityGridProps {
  dimensions?: DimensionData[];
  breakdown?: Record<string, CategoryData>;
  archetypeMetadata?: ArchetypeMetadata;
}

const getDimensionIcon = (iconName?: string, id?: string) => {
  const key = `${iconName || ""} ${id || ""}`.toLowerCase();
  if (key.includes("cloud") || key.includes("iac")) return Cloud;
  if (key.includes("server") || key.includes("container") || key.includes("orchestr")) return Server;
  if (key.includes("terminal") || key.includes("cicd") || key.includes("script")) return Terminal;
  if (key.includes("activity") || key.includes("observ") || key.includes("sre") || key.includes("telemetry")) return Activity;
  if (key.includes("palette") || key.includes("styling") || key.includes("design") || key.includes("css")) return Palette;
  if (key.includes("cpu") || key.includes("manipulation") || key.includes("ml") || key.includes("compute")) return Cpu;
  if (key.includes("shield") || key.includes("security") || key.includes("cyber")) return Shield;
  if (key.includes("phone") || key.includes("mobile") || key.includes("ios") || key.includes("android")) return Smartphone;
  if (key.includes("database") || key.includes("warehouse") || key.includes("sql") || key.includes("store")) return Database;
  if (key.includes("layer") || key.includes("frame") || key.includes("ui")) return Layers;
  if (key.includes("wrench") || key.includes("tool") || key.includes("infra")) return Wrench;
  return Code2;
};

export const GranularCapabilityGrid: React.FC<GranularCapabilityGridProps> = ({
  dimensions,
  breakdown = {},
  archetypeMetadata
}) => {
  // Normalize dimensions from explicit dimensions prop or derive from non-omitted breakdown entries
  const activeDimensions: DimensionData[] = React.useMemo(() => {
    if (dimensions && dimensions.length > 0) {
      return dimensions;
    }

    const items: DimensionData[] = [];
    for (const [key, val] of Object.entries(breakdown)) {
      if (val.is_omitted) continue;
      // Skip duplicate alias keys (languages, frameworks, etc.) if custom dimension keys already captured
      const dimId = val.dimension_id || key;
      if (items.some(d => d.id === dimId)) continue;

      items.push({
        id: dimId,
        label: val.tier_label || val.label || key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
        icon: val.icon,
        weight: val.weight ?? 0.25,
        percentage: val.percentage ?? 0,
        matched: val.matched || [],
        missing: val.missing || [],
        total_required: val.total_required || ((val.matched?.length || 0) + (val.missing?.length || 0)),
        deficit: typeof val.percentage === "number" ? Math.round((val.weight ?? 0.25) * Math.max(0, 100 - val.percentage)) : 0
      });
    }

    if (items.length > 0) {
      return items;
    }

    // Default 4 canonical fallback if completely empty
    return [
      { id: "languages", label: "Languages", weight: 0.40, percentage: 100, matched: [], missing: [], total_required: 0 },
      { id: "frameworks", label: "Frameworks", weight: 0.30, percentage: 100, matched: [], missing: [], total_required: 0 },
      { id: "databases", label: "Databases", weight: 0.20, percentage: 100, matched: [], missing: [], total_required: 0 },
      { id: "tools", label: "Tools & Infrastructure", weight: 0.10, percentage: 100, matched: [], missing: [], total_required: 0 }
    ];
  }, [dimensions, breakdown]);

  const omittedList = archetypeMetadata?.omitted_metrics || [];

  return (
    <div className="space-y-4">
      {/* Dynamic Header & Archetype Discipline Callout */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1 border-b border-slate-200/60 dark:border-slate-800">
        <div>
          <h4 className="text-sm font-bold text-slate-900 dark:text-white tracking-tight">
            Competency Breakdown
          </h4>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
            Required technical skills and category distributions for this role.
          </p>
        </div>

        <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400 shrink-0">
          {activeDimensions.length} Categories (Total = 100%)
        </span>
      </div>

      {/* Omitted Metrics Fair Assessment Notice */}
      {omittedList.length > 0 && (
        <div className="flex items-start space-x-2.5 rounded-xl border border-emerald-500/20 bg-emerald-50/50 dark:bg-emerald-950/20 px-3.5 py-2.5 text-xs text-emerald-900 dark:text-emerald-200">
          <Info size={15} className="text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span className="font-semibold block leading-tight">
              Fair Assessment: Non-Essential Skills Excluded
            </span>
            <p className="text-[11px] text-emerald-800/90 dark:text-emerald-300/90">
              The following domains are not required for this role and have <strong className="font-semibold">0% weight</strong>:{" "}
              {omittedList.map((m, idx) => (
                <span key={m} className="font-mono bg-emerald-100/70 dark:bg-emerald-900/50 px-1.5 py-0.2 rounded text-[10px] mx-0.5">
                  {m}{idx < omittedList.length - 1 ? "" : ""}
                </span>
              ))}
              . Candidates are not evaluated or penalized on these.
            </p>
          </div>
        </div>
      )}

      {/* Dynamic Dimensions Grid */}
      <div className={`grid grid-cols-1 md:grid-cols-2 ${activeDimensions.length > 3 ? "lg:grid-cols-4" : "lg:grid-cols-3"} gap-4`}>
        {activeDimensions.map((dim) => {
          const matchedList = dim.matched || [];
          const missingList = dim.missing || [];
          const Icon = getDimensionIcon(dim.icon, dim.id);
          const percentage = dim.percentage ?? 100;
          const weightPct = Math.round((dim.weight || 0.25) * 100);

          return (
            <div
              key={dim.id}
              className="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/70 p-4 flex flex-col justify-between shadow-[0_1px_3px_rgba(0,0,0,0.02)] space-y-3.5 hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
            >
              {/* Header */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center space-x-2">
                    <div className="rounded-lg bg-slate-100 dark:bg-[#1e293b] p-1.5 text-slate-700 dark:text-slate-300 shrink-0">
                      <Icon size={14} />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-900 dark:text-white block leading-tight">
                        {dim.label}
                      </span>
                      <span className="text-[10px] text-blue-600 dark:text-blue-400 font-mono font-medium">
                        {weightPct}% weight
                      </span>
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
