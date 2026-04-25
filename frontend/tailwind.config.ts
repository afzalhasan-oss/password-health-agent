import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        healthy: "#15803d",
        okay: "#ca8a04",
        critical: "#b91c1c",
      },
    },
  },
  plugins: [],
};

export default config;
