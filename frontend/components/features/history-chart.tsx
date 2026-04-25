type HistoryPoint = {
  assessmentId: string;
  score: number;
  status: "HEALTHY" | "OKAY" | "CRITICAL";
  createdAt: string;
};

type HistoryChartProps = {
  items: HistoryPoint[];
};

// Renders a lightweight history list and mini trend bars for mobile-friendly tracking.
export function HistoryChart({ items }: HistoryChartProps) {
  if (items.length === 0) {
    return <p className="text-slate-600">No checks yet. Your first score will appear here.</p>;
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <div key={item.assessmentId} className="rounded-lg border bg-white p-3">
          <div className="mb-2 flex items-center justify-between">
            <p className="font-medium">{item.status}</p>
            <p className="text-sm text-slate-500">{new Date(item.createdAt).toLocaleString()}</p>
          </div>
          <div className="h-2 w-full rounded-full bg-slate-200">
            <div className="h-full rounded-full bg-slate-700" style={{ width: `${item.score}%` }} />
          </div>
          <p className="mt-2 text-sm text-slate-600">Score: {item.score}</p>
        </div>
      ))}
    </div>
  );
}
