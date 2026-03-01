"use client";

import Link from "next/link";
import { Telemetry } from "@/types";
import { formatDate } from "@/utils/formatDate";

interface Props {
    data: Telemetry[];
    showDeviceId?: boolean;
}

export default function TelemetryTable({
    data,
    showDeviceId = true,
}: Props) {
    if (!data || data.length === 0) {
        return (
            <div className="text-center border border-gray-600 p-6 bg-[#1E293B] rounded text-gray-400">
                No telemetry data
            </div>
        );
    }

    return (
        <table className="enterprise-table text-sm mt-4 text-center">
            <thead>
                <tr>
                    <th>Time</th>

                    {showDeviceId && <th>Device ID</th>}

                    <th>Speed</th>
                    <th>Fuel (%)</th>
                    <th>Latitude</th>
                    <th>Longitude</th>
                </tr>
            </thead>

            <tbody>
                {data.map((t) => (
                    <tr key={t.id}>
                        <td>
                            {t.created_at
                                ? formatDate(t.created_at)
                                : "-"}
                        </td>

                        {showDeviceId && (
                            <td>
                                {t.device_id ? (
                                    <Link
                                        href={`/devices/${t.device_id}`}
                                        className="
                                            text-blue-400
                                            visited:text-purple-400
                                            hover:underline
                                            transition-colors
                                            duration-200
                                        "
                                    >
                                        {t.device_id}
                                    </Link>
                                ) : (
                                    "-"
                                )}
                            </td>
                        )}

                        <td>
                            {t.speed?.toFixed(2) ?? "-"}
                        </td>

                        <td>
                            {t.fuel_level != null
                                ? t.fuel_level.toFixed(2)
                                : "-"}
                        </td>

                        <td>{t.latitude ?? "-"}</td>
                        <td>{t.longitude ?? "-"}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}