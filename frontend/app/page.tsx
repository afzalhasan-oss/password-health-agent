"use client";

import Link from "next/link";
import { useState } from "react";

import { GuidanceList } from "@/components/features/guidance-list";
import { ScoreCard } from "@/components/features/score-card";
import { ScoreProgress } from "@/components/features/score-progress";
import { createHealthCheck, type HealthCheckResponse } from "@/lib/api-client";
import { healthInputSchema } from "@/lib/validation";

// Renders the main chat-like form and score result workflow.
export default function HomePage() {
  const [passwordCount, setPasswordCount] = useState("20");
  const [oldestPasswordAgeDays, setOldestPasswordAgeDays] = useState("180");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [result, setResult] = useState<HealthCheckResponse | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Submits validated form data to API and updates UI with result or friendly errors.
  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);

    const parsed = healthInputSchema.safeParse({
      passwordCount: Number(passwordCount),
      oldestPasswordAgeDays: Number(oldestPasswordAgeDays),
    });

    if (!parsed.success) {
      setErrorMessage(parsed.error.issues[0]?.message ?? "Please review your input values.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await createHealthCheck(parsed.data);
      setResult(response);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to complete check right now.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-3xl space-y-6 px-4 py-8 sm:px-6">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold">Password Management Health Checker</h1>
        <p className="text-slate-600">
          Share two details and get an encouraging, prioritized plan to improve your score.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-4 rounded-xl border bg-white p-4 sm:p-6">
        <label className="block space-y-2">
          <span className="text-sm font-medium">How many passwords do you currently manage?</span>
          <input
            className="w-full rounded-lg border p-2"
            inputMode="numeric"
            value={passwordCount}
            onChange={(event) => setPasswordCount(event.target.value)}
          />
        </label>

        <label className="block space-y-2">
          <span className="text-sm font-medium">How old is your oldest password (days)?</span>
          <input
            className="w-full rounded-lg border p-2"
            inputMode="numeric"
            value={oldestPasswordAgeDays}
            onChange={(event) => setOldestPasswordAgeDays(event.target.value)}
          />
        </label>

        {errorMessage ? (
          <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{errorMessage}</p>
        ) : null}

        <button
          className="w-full rounded-lg bg-slate-900 px-4 py-2 font-semibold text-white disabled:opacity-50"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Checking..." : "Check My Password Health"}
        </button>
      </form>

      {result ? (
        <section className="space-y-4">
          <ScoreCard score={result.score} status={result.status} />
          <ScoreProgress score={result.score} status={result.status} />
          <GuidanceList guidance={result.guidance} />
        </section>
      ) : null}

      <Link href="/history" className="inline-flex rounded-lg border bg-white px-4 py-2 text-sm font-medium">
        View Score History
      </Link>
    </main>
  );
}
