import type { ScoreStatus } from "@/lib/score-color";

export type GuidanceItem = {
  priorityRank: number;
  title: string;
  detail: string;
};

export type HealthCheckResponse = {
  assessmentId: string;
  score: number;
  status: ScoreStatus;
  color: "green" | "yellow" | "red";
  guidance: GuidanceItem[];
};

export type HistoryResponse = {
  items: Array<{
    assessmentId: string;
    score: number;
    status: ScoreStatus;
    createdAt: string;
  }>;
  trend: {
    direction: "IMPROVING" | "STABLE" | "DECLINING";
    deltaFromPrevious: number;
  };
};

// Returns API base URL from environment with localhost fallback.
function apiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
}

// Parses a friendly message from API error response payload.
async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    if (typeof data?.message === "string") return data.message;
    if (typeof data?.detail?.message === "string") return data.detail.message;
  } catch {
    // Keeps fallback message when response is not JSON.
  }
  return "Something went wrong. Please try again.";
}

// Calls POST endpoint to create a new health check and returns typed result.
export async function createHealthCheck(payload: {
  passwordCount: number;
  oldestPasswordAgeDays: number;
}): Promise<HealthCheckResponse> {
  const response = await fetch(`${apiBase()}/v1/health-checks`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response));
  }

  return (await response.json()) as HealthCheckResponse;
}

// Calls GET endpoint for historical assessments of current session.
export async function getHistory(): Promise<HistoryResponse> {
  const response = await fetch(`${apiBase()}/v1/health-checks/history`, {
    method: "GET",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    throw new Error(await parseErrorMessage(response));
  }

  return (await response.json()) as HistoryResponse;
}
