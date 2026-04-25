import { cn } from "@/lib/utils";

type ProgressProps = {
  value: number;
  className?: string;
  indicatorClassName?: string;
};

// Renders a shadcn-style progress bar used for score display.
export function Progress({ value, className, indicatorClassName }: ProgressProps) {
  const safe = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("h-3 w-full overflow-hidden rounded-full bg-slate-200", className)}>
      <div
        className={cn("h-full transition-all", indicatorClassName)}
        style={{ width: `${safe}%` }}
      />
    </div>
  );
}
