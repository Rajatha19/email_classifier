import type { Metadata } from "next";
import { Inter } from "next/font/google"; // 👈 importa Inter
import { Toaster } from "sonner";
import "./globals.css";

// 👇 configura Inter como a única fonte
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Email Classifier",
  description: "Classify emails as productive or unproductive",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} antialiased font-sans`}
        suppressHydrationWarning
      >
        <Toaster
          position="top-center"
          expand={true}
          richColors
          closeButton
          theme="dark"
          duration={3000}
        />
        {children}
      </body>
    </html>
  );
}
