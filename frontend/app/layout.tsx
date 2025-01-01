import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import Sidebar from "@/components/sidebar";
import StoreProvider from "./StoreProvider"

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "My Journalist",
  description: "LIMS news",
};

export default function RootLayout({
  auth,
  children,
}: {
  auth: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
      <StoreProvider>
          <div className="py-5 grid min-h-screen w-full overflow-hidden lg:grid-cols-[auto_1fr]">
            <Sidebar />
            <div className="flex flex-col">
              <Header />
              <div>{auth}</div>
              <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6">
                <div className="border shadow-sm rounded-lg p-2">
                  {children}
                </div>
              </main>
            </div>
          </div>
        </StoreProvider>
      </body>
    </html>
  );
}
