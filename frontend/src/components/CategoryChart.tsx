"use client";

import React, { useState, useEffect } from "react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from "recharts";

export interface DimensionItem {
  id: string;
  label: string;
  icon?: string;
  weight: number;
  percentage: number;
  matched?: string[];
  missing?: string[];
  total_required?: number;
}

export interface CategoryBreakdownItem {
  tier_label?: string;
  label?: string;
  percentage: number;
  weight?: number;
  matched?: string[];
  missing?: string[];
  is_omitted?: boolean;
}

interface CategoryChartProps {
  dimensions?: DimensionItem[];
  breakdown?: Record<string, CategoryBreakdownItem>;
  isDark?: boolean;
}

export function CategoryChart({ dimensions, breakdown = {}, isDark = true }: CategoryChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const data = React.useMemo(() => {
    if (dimensions && dimensions.length > 0) {
      return dimensions.map((d) => ({
        category: d.label,
        percentage: d.percentage ?? 0,
        weight: `${Math.round((d.weight || 0.25) * 100)}%`,
        matched: d.matched?.length ?? 0,
        missing: d.missing?.length ?? 0,
      }));
    }

    const items = Object.entries(breakdown)
      .filter(([_, item]) => !item?.is_omitted)
      .map(([key, item]) => ({
        category: item.tier_label || item.label || key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
        percentage: item.percentage ?? 0,
        weight: item.weight ? `${Math.round(item.weight * 100)}%` : "25%",
        matched: item.matched?.length ?? 0,
        missing: item.missing?.length ?? 0,
      }));

    if (items.length > 0) {
      return items;
    }

    return [
      { category: "Languages", percentage: 0, weight: "40%", matched: 0, missing: 0 },
      { category: "Frameworks", percentage: 0, weight: "30%", matched: 0, missing: 0 },
      { category: "Databases", percentage: 0, weight: "20%", matched: 0, missing: 0 },
      { category: "Tools", percentage: 0, weight: "10%", matched: 0, missing: 0 },
    ];
  }, [dimensions, breakdown]);

  if (!mounted) {
    return (
      <div className="h-44 w-full flex items-center justify-center text-xs text-slate-400">
        Initializing competency matrix...
      </div>
    );
  }

  return (
    <div className="h-44 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <XAxis type="number" domain={[0, 100]} hide />
          <YAxis
            type="category"
            dataKey="category"
            stroke={isDark ? "#94a3b8" : "#64748b"}
            fontSize={11}
            tickLine={false}
            axisLine={false}
            width={85}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] p-3 text-xs shadow-xl">
                    <p className="font-semibold text-slate-900 dark:text-white">
                      {item.category} ({item.weight} weight)
                    </p>
                    <p className="text-slate-600 dark:text-slate-300 mt-1 font-mono tabular-nums">
                      Coverage: {item.percentage}%
                    </p>
                    <p className="text-emerald-600 dark:text-emerald-400 font-mono tabular-nums">
                      Verified: {item.matched}
                    </p>
                    <p className="text-rose-600 dark:text-rose-400 font-mono tabular-nums">
                      Gaps: {item.missing}
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="percentage" radius={[0, 6, 6, 0]} barSize={16}>
            {data.map((entry, index) => {
              let fill = "#ff3b30";
              if (entry.percentage >= 70) fill = "#28cd41";
              else if (entry.percentage >= 40) fill = "#ff9f0a";
              return <Cell key={`cell-${index}`} fill={fill} />;
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
