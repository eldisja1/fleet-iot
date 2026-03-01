"use client";

import { useEffect, useState } from "react";
import TelemetryTable from "@/components/TelemetryTable";
import Charts from "@/components/Charts";
import {
  Telemetry,
  TelemetryListResponse,
} from "@/types";
import PageTitle from "@/components/PageTitle";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const limit = 50;

export default function TelemetryPage() {
  const [data, setData] = useState<Telemetry[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(
        `${API_URL}/telemetry?page=${page}&limit=${limit}`,
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

      const result: TelemetryListResponse = await res.json();

      setData(result.data);
      setTotal(result.total);
    };

    fetchData();
  }, [page]);

  const totalPages = Math.max(1, Math.ceil(total / limit));

  return (
    <div className="max-w-6xl mx-auto mt-12 px-6">
      <div className="enterprise-card">

        {/* TITLE */}
        <PageTitle title="Telemetry" />

        {/* CHART SECTION */}
        <div className="mt-6">
          <Charts data={data} />
        </div>

        {/* TABLE SECTION */}
        <div className="mt-6 pt-4 border-t border-gray-700">
          <TelemetryTable data={data} />
        </div>

        {/* PAGINATION */}
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