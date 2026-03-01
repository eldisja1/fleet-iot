"use client";

import { useEffect, useState } from "react";
import DeviceTable from "@/components/DeviceTable";
import { Device, DeviceListResponse } from "@/types";
import PageTitle from "@/components/PageTitle";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const limit = 20;

export default function DevicesPage() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const res = await fetch(
          `${API_URL}/devices?page=${page}&limit=${limit}`,
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

        const data: DeviceListResponse = await res.json();
        setDevices(data.data);
        setTotal(data.total);
      } catch (err) {
        console.error("Failed to fetch devices:", err);
        setError("Failed to load devices");
      }
    };

    fetchDevices();
  }, [page]);

  const totalPages = Math.max(1, Math.ceil(total / limit));

  if (error) {
    return (
      <div className="max-w-6xl mx-auto mt-10 text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto mt-12 px-6">
      <div className="enterprise-card">
        <PageTitle title="Devices" />

        <div className="text-sm text-gray-400 text-center mb-6">
          Total: {total}
        </div>

        <DeviceTable devices={devices} />

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
      </div>
    </div>
  );
}