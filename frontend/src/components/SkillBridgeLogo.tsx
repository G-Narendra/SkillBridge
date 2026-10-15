import React from "react";

interface SkillBridgeLogoProps {
  size?: number;
  className?: string;
  showText?: boolean;
}

export const SkillBridgeLogo: React.FC<SkillBridgeLogoProps> = ({
  size = 36,
  className = "",
  showText = false,
}) => {
  return (
    <div className={`flex items-center space-x-2.5 ${className}`}>
      <div
        className="relative flex items-center justify-center rounded-xl bg-gradient-to-br from-[#0071e3] via-[#0284c7] to-[#4f46e5] p-2 text-white shadow-sm ring-1 ring-white/20 select-none"
        style={{ width: size, height: size }}
      >
        <svg
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full"
        >
          {/* Bridge baseline deck */}
          <path
            d="M5 25.5H27"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            className="opacity-70"
          />
          {/* Main primary arch spanning across */}
          <path
            d="M6 25C6 16.5 10.5 11 16 11C21.5 11 26 16.5 26 25"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          {/* Inner pathway arch */}
          <path
            d="M10.5 25C10.5 19 13 15 16 15C19 15 21.5 19 21.5 25"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            className="opacity-80"
          />
          {/* Milestone beacon star / focal node bridging potential to outcome */}
          <circle cx="16" cy="6.5" r="2.2" fill="currentColor" />
          <path
            d="M16 10.5V12"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            className="opacity-75"
          />
        </svg>
      </div>

      {showText && (
        <div>
          <span className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
            SkillBridge
          </span>
          <span className="block text-[11px] text-slate-500 dark:text-slate-400">
            Career Project Builder
          </span>
        </div>
      )}
    </div>
  );
};
