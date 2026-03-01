"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer,
} from "recharts";

export default function Charts({ data }: { data: any[] }) {
    if (!data || data.length === 0) {
        return <div className="text-center text-gray-400">No data</div>;
    }

    return (
        <div className="bg-[#1E293B] p-4 rounded-xl border border-gray-700 h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <CartesianGrid stroke="#334155" />
                    <XAxis dataKey="created_at" stroke="#94A3B8" />
                    <YAxis stroke="#94A3B8" />
                    <Tooltip />
                    <Line type="monotone" dataKey="speed" stroke="#3B82F6" />
                    <Line type="monotone" dataKey="fuel" stroke="#22C55E" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}