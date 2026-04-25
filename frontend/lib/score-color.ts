export type ScoreStatus = "HEALTHY" | "OKAY" | "CRITICAL";

// Maps score status to semantic color classes for consistent frontend styling.
export function statusToColorClass(status: ScoreStatus): string {
  if (status === "HEALTHY") return "text-healthy";
  if (status === "OKAY") return "text-okay";
  return "text-critical";
}

// Maps score status to progress indicator classes.
export function statusToProgressClass(status: ScoreStatus): string {
  if (status === "HEALTHY") return "bg-healthy";
  if (status === "OKAY") return "bg-okay";
  return "bg-critical";
}
