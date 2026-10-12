"use client";

import React, { useState, useEffect } from "react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from "recharts";

interface CategoryBreakdownItem {
  percentage: number;
  matched?: string[];
  missing?: string[];
}

interface CategoryChartProps {
  breakdown?: {
    languages?: CategoryBreakdownItem;
    frameworks?: CategoryBreakdownItem;
    databases?: CategoryBreakdownItem;
    tools?: CategoryBreakdownItem;
  };
  isDark?: boolean;
}

export function CategoryChart({ breakdown = {}, isDark = true }: CategoryChartProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const data = [
    {
      category: "Languages",
      percentage: breakdown?.languages?.percentage ?? 0,
      weight: "40%",
      matched: breakdown?.languages?.matched?.length ?? 0,
      missing: breakdown?.languages?.missing?.length ?? 0,
    },
    {
      category: "Frameworks",
      percentage: breakdown?.frameworks?.percentage ?? 0,
      weight: "30%",
      matched: breakdown?.frameworks?.matched?.length ?? 0,
      missing: breakdown?.frameworks?.missing?.length ?? 0,
    },
    {
      category: "Databases",
      percentage: breakdown?.databases?.percentage ?? 0,
      weight: "20%",
      matched: breakdown?.databases?.matched?.length ?? 0,
      missing: breakdown?.databases?.missing?.length ?? 0,
    },
    {
      category: "Tools",
      percentage: breakdown?.tools?.percentage ?? 0,
      weight: "10%",
      matched: breakdown?.tools?.matched?.length ?? 0,
      missing: breakdown?.tools?.missing?.length ?? 0,
    },
  ];

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
            width={75}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] p-3 text-xs shadow-xl">
                    <p className="font-semibold text-slate-900 dark:text-white">{item.category} ({item.weight} weight)</p>
                    <p className="text-slate-600 dark:text-slate-300 mt-1 font-mono tabular-nums">Coverage: {item.percentage}%</p>
                    <p className="text-emerald-600 dark:text-emerald-400 font-mono tabular-nums">Verified: {item.matched}</p>
                    <p className="text-rose-600 dark:text-rose-400 font-mono tabular-nums">Gaps: {item.missing}</p>
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
