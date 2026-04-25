import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Password Health Checker",
  description: "Track and improve your password health over time.",
};

// Renders the shared root layout for all pages.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
