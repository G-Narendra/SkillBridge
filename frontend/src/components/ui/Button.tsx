import React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    const variants = {
      primary:
        "bg-[#0071e3] text-white hover:bg-[#0077ed] active:bg-[#0062c4] shadow-sm font-medium",
      secondary:
        "bg-slate-100 dark:bg-[#1e293b] text-slate-800 dark:text-slate-100 border border-slate-200/80 dark:border-slate-800 hover:bg-slate-200/70 dark:hover:bg-slate-700/80 font-medium",
      outline:
        "border border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-transparent text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 font-medium",
      ghost:
        "bg-transparent text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100",
    };

    const sizes = {
      sm: "px-3 py-1.5 text-xs rounded-lg",
      md: "px-4 py-2 text-xs sm:text-sm rounded-xl",
      lg: "px-5 py-2.5 text-sm sm:text-base rounded-xl",
    };

    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0071e3] disabled:pointer-events-none disabled:opacity-50 select-none",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
