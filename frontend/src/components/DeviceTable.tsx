"use client";

import Link from "next/link";
import { Device } from "@/types";

interface Props {
    devices: Device[];
}

export default function DeviceTable({ devices }: Props) {
    if (!devices || devices.length === 0) {
        return (
            <div className="text-center border border-gray-600 p-6 bg-[#1E293B] rounded text-gray-400">
                No devices available
            </div>
        );
    }

    return (
        <table className="enterprise-table text-sm">
            <thead>
                <tr>
                    <th style={{ width: "45%" }}>ID</th>
                    <th style={{ width: "35%" }}>Name</th>
                    <th style={{ width: "20%" }}>Status</th>
                </tr>
            </thead>
            <tbody>
                {devices.map((d) => (
                    <tr key={d.id}>
                        <td className="break-all">
                            <Link
                                href={`/devices/${d.id}`}
                                className="device-link"
                            >
                                {d.id}
                            </Link>
                        </td>
                        <td className="text-gray-200">
                            {d.name}
                        </td>
                        <td>
                            <span
                                className={`status-badge ${
                                    d.status === "online"
                                        ? "status-online"
                                        : "status-offline"
                                }`}
                            >
                                {d.status}
                            </span>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}