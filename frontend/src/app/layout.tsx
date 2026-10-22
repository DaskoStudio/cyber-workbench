import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cyber Workbench",
  description: "Vitrine technique : code de base et architecture.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="fr"><body>{children}</body></html>;
}
