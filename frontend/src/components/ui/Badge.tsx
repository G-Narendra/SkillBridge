import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "warning" | "destructive" | "outline";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants = {
    default:
      "border-slate-200 dark:border-slate-700/80 bg-slate-100 dark:bg-slate-800/80 text-slate-800 dark:text-slate-100",
    success:
      "border-emerald-200 dark:border-emerald-500/20 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 font-medium",
    warning:
      "border-amber-200 dark:border-amber-500/20 bg-amber-50 dark:bg-amber-500/10 text-amber-700 dark:text-amber-400 font-medium",
    destructive:
      "border-rose-200 dark:border-rose-500/20 bg-rose-50 dark:bg-rose-500/10 text-rose-700 dark:text-rose-400 font-medium",
    outline:
      "border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 bg-white/70 dark:bg-[#1e293b]/40",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-medium transition-colors select-none",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
