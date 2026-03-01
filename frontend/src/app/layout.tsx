import "./globals.css";
import Navbar from "@/components/Navbar";

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className="min-h-screen bg-[#0F172A] text-white">
                <div className="flex flex-col min-h-screen">

                    <Navbar />

                    <main className="flex-1 flex justify-center">
                        <div className="w-full max-w-6xl px-6 py-10">
                            {children}
                        </div>
                    </main>

                </div>
            </body>
        </html>
    );
}