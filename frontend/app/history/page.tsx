"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { HistoryChart } from "@/components/features/history-chart";
import { getHistory, type HistoryResponse } from "@/lib/api-client";

// Renders historical score tracking and trend direction for current session.
export default function HistoryPage() {
  const [data, setData] = useState<HistoryResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    // Loads score history when the page mounts and displays friendly fetch errors.
    async function load() {
      try {
        const response = await getHistory();
        setData(response);
      } catch (error) {
        setErrorMessage(error instanceof Error ? error.message : "Could not load history yet.");
      }
    }
    void load();
  }, []);

  return (
    <main className="mx-auto min-h-screen w-full max-w-3xl space-y-6 px-4 py-8 sm:px-6">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold">Your Password Health History</h1>
        <p className="text-slate-600">Track progress over time and keep improving steadily.</p>
      </header>

      {errorMessage ? <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{errorMessage}</p> : null}

      {data ? (
        <section className="space-y-4">
          <p className="rounded-lg border bg-white p-3 text-sm">
            Trend: <strong>{data.trend.direction}</strong> ({data.trend.deltaFromPrevious >= 0 ? "+" : ""}
            {data.trend.deltaFromPrevious})
          </p>
          <HistoryChart items={data.items} />
        </section>
      ) : (
        <p className="text-slate-600">Loading your history...</p>
      )}

      <Link href="/" className="inline-flex rounded-lg border bg-white px-4 py-2 text-sm font-medium">
        Back to Health Check
      </Link>
    </main>
  );
}
