"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import TelemetryTable from "@/components/TelemetryTable";
import {
  Telemetry,
  TelemetryListResponse,
  Device,
} from "@/types";
import PageTitle from "@/components/PageTitle";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const limit = 50;

export default function DeviceDetailPage() {
  const params = useParams();
  const deviceId = params.id as string;

  const [data, setData] = useState<Telemetry[]>([]);
  const [device, setDevice] = useState<Device | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!deviceId) return;

    const fetchAll = async () => {
      setLoading(true);

      const authHeader =
        "Basic " +
        btoa(
          `${process.env.NEXT_PUBLIC_API_USERNAME}:${process.env.NEXT_PUBLIC_API_PASSWORD}`
        );

      const deviceRes = await fetch(
        `${API_URL}/devices/${deviceId}`,
        { headers: { Authorization: authHeader } }
      );

      const deviceData = await deviceRes.json();
      setDevice(deviceData);

      const telemetryRes = await fetch(
        `${API_URL}/telemetry?device_id=${deviceId}&page=${page}&limit=${limit}`,
        { headers: { Authorization: authHeader } }
      );

      const telemetryData: TelemetryListResponse =
        await telemetryRes.json();

      setData(telemetryData.data);
      setTotal(telemetryData.total);
      setLoading(false);
    };

    fetchAll();
  }, [deviceId, page]);

  const totalPages = Math.max(1, Math.ceil(total / limit));

  return (
    <div className="max-w-6xl mx-auto mt-12 px-6">
      <div className="enterprise-card">
        <PageTitle title="Telemetry for Device" />

        {device && (
          <div className="text-center mb-6">
            <h2 className="text-xl font-semibold text-white">
              {device.name}
            </h2>
            <p className="text-gray-400 break-all">
              ID: {device.id}
            </p>
            <p className="text-gray-400">
              Status: {device.status}
            </p>
          </div>
        )}

        {loading ? (
          <div className="text-center p-6 border border-gray-600 bg-[#1E293B] rounded text-gray-400">
            Loading...
          </div>
        ) : (
          <>
            <TelemetryTable data={data} showDeviceId={false} />

            {/* ENTERPRISE PAGINATION */}
            <div className="mt-8 pt-6 border-t border-gray-700 flex items-center">
              <div className="flex-1">
                <button
                  disabled={page === 1}
                  onClick={() => setPage(page - 1)}
                  className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded disabled:opacity-40"
                >
                  Previous
                </button>
              </div>

              <div className="flex-1 text-center font-medium">
                Page {page} of {totalPages}
              </div>

              <div className="flex-1 text-right">
                <button
                  disabled={page === totalPages}
                  onClick={() => setPage(page + 1)}
                  className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}