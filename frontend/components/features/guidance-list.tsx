import type { GuidanceItem } from "@/lib/api-client";

type GuidanceListProps = {
  guidance: GuidanceItem[];
};

// Renders prioritized encouraging recommendations for next actions.
export function GuidanceList({ guidance }: GuidanceListProps) {
  if (guidance.length === 0) return null;

  return (
    <section className="space-y-3 rounded-xl border bg-white p-4">
      <h2 className="text-lg font-semibold">What to fix first</h2>
      <ol className="space-y-2">
        {guidance
          .slice()
          .sort((a, b) => a.priorityRank - b.priorityRank)
          .map((item) => (
            <li key={item.priorityRank} className="rounded-lg bg-slate-50 p-3">
              <p className="font-medium">{item.priorityRank}. {item.title}</p>
              <p className="text-sm text-slate-600">{item.detail}</p>
            </li>
          ))}
      </ol>
    </section>
  );
}
