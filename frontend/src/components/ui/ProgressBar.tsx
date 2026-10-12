import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  value: number; // 0 to 100
  max?: number;
  className?: string;
  indicatorClassName?: string;
}

export function ProgressBar({ value, max = 100, className, indicatorClassName }: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div
      className={cn(
        'h-2 w-full overflow-hidden rounded-full bg-slate-800',
        className
      )}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
    >
      <div
        className={cn(
          'h-full bg-blue-500 transition-all duration-500 ease-in-out',
          indicatorClassName
        )}
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
}
