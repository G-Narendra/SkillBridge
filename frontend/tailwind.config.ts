import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#090d16",
        surface: {
          100: "#0f172a",
          200: "#1e293b",
        },
        apple: {
          canvas: "#f5f5f7",
          surface: "#ffffff",
          subtle: "#fbfbfd",
          border: "#e5e5ea",
          text: "#1d1d1f",
          subtext: "#6e6e73",
          muted: "#86868b",
          blue: "#0071e3",
          blueHover: "#0077ed",
          emerald: "#28cd41",
          amber: "#ff9f0a",
          rose: "#ff3b30",
        },
        cobalt: "#3b82f6",
        emerald: "#10b981",
        amber: "#f59e0b",
        rose: "#f43f5e",
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "SF Pro Text",
          "SF Pro Display",
          "Inter",
          "Segoe UI",
          "sans-serif",
        ],
        mono: [
          "SF Mono",
          "ui-monospace",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
      },
    },
  },
  plugins: [],
};
export default config;
