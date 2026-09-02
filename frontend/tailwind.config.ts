import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        mist: "#F8FAF9",
        soil: "#4B3621",
        primary: "#3E5C5A",
        secondary: "#E2EDE9",
        growth: "#709A85",
        wither: "#D1C2A5",
      },
      fontFamily: {
        display: ["var(--font-display)", '"Noto Serif SC"', "Songti SC", "serif"],
        sans: ["var(--font-sans)", '"Noto Sans SC"', "PingFang SC", "Microsoft YaHei", "sans-serif"],
      },
      backgroundImage: {
        mistfield:
          "radial-gradient(ellipse at 20% 0%, rgba(226,237,233,0.9), transparent 55%), radial-gradient(ellipse at 80% 20%, rgba(112,154,133,0.18), transparent 45%), linear-gradient(180deg, #F8FAF9 0%, #EEF4F1 100%)",
        soilbed:
          "linear-gradient(180deg, #5A4330 0%, #4B3621 45%, #3A2918 100%)",
      },
      boxShadow: {
        soft: "0 12px 40px rgba(75, 54, 33, 0.08)",
      },
    },
  },
  plugins: [],
};
export default config;
