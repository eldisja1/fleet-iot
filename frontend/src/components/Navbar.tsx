"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
    const router = useRouter();

    const handleLogout = () => {
        localStorage.clear();
        router.push("/");
    };

    return (
        <div className="w-full flex justify-center mt-6">
            <div
                className="relative w-full max-w-6xl rounded-xl shadow-lg"
                style={{
                    background: "rgba(255,255,255,0.1)",
                    padding: "20px 40px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                }}
            >
                {/* LEFT - LOGO */}
                <div
                    style={{
                        fontWeight: 800,
                        fontSize: "20px",
                        color: "white",
                    }}
                >
                    FLEETIOT
                </div>

                {/* CENTER - MENU */}
                <div
                    style={{
                        position: "absolute",
                        left: "50%",
                        transform: "translateX(-50%)",
                        display: "flex",
                        gap: "60px",
                    }}
                >
                    <Link href="/" style={{ color: "white", fontWeight: 600 }}>
                        Dashboard
                    </Link>

                    <Link href="/devices" style={{ color: "white", fontWeight: 600 }}>
                        Devices
                    </Link>

                    <Link href="/telemetry" style={{ color: "white", fontWeight: 600 }}>
                        Telemetry
                    </Link>
                </div>

                {/* RIGHT - LOGOUT */}
                <button
                    onClick={handleLogout}
                    style={{
                        color: "white",
                        fontWeight: 600,
                        background: "transparent",
                        border: "none",
                        cursor: "pointer",
                    }}
                >
                    Logout
                </button>
            </div>
        </div>
    );
}