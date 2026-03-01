"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Charts = dynamic(() => import("@/components/Charts"), {
    ssr: false,
});

const MapView = dynamic(() => import("@/components/MapView"), {
    ssr: false,
});

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

export default function Dashboard() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!API_URL) return;

        const fetchData = async () => {
            const res = await fetch(
                `${API_URL}/telemetry?page=1&limit=20`,
                {
                    headers: {
                        Authorization:
                            "Basic " +
                            btoa(
                                `${process.env.NEXT_PUBLIC_API_USERNAME}:${process.env.NEXT_PUBLIC_API_PASSWORD}`
                            ),
                    },
                }
            );

            const result = await res.json();
            setData(result.data);
            setLoading(false);
        };

        fetchData();
    }, []);

    const latest = data.length > 0 ? data[0] : null;

    return (
        <div className="max-w-6xl mx-auto mt-12 px-6">
            <div className="enterprise-card">
                <h1 className="text-3xl font-bold text-white text-center mb-10">
                    Fleet IoT Dashboard
                </h1>

                {loading ? (
                    <div className="text-center text-gray-400">
                        Loading dashboard...
                    </div>
                ) : (
                    <div className="grid md:grid-cols-2 gap-8">
                        <div>
                            <h2 className="text-xl font-semibold text-white mb-4 text-center">
                                Telemetry Overview
                            </h2>
                            <Charts data={data} />
                        </div>

                        <div>
                            <h2 className="text-xl font-semibold text-white mb-4 text-center">
                                Latest Device Location
                            </h2>

                            {latest?.latitude && latest?.longitude ? (
                                <MapView
                                    lat={latest.latitude}
                                    lng={latest.longitude}
                                />
                            ) : (
                                <div className="p-6 border border-gray-600 bg-[#1E293B] rounded text-center text-gray-400">
                                    No location data available
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}