import { Card, CardContent } from "@/components/ui/card";
import { statusToColorClass, type ScoreStatus } from "@/lib/score-color";

type ScoreCardProps = {
  score: number;
  status: ScoreStatus;
};

// Renders the core score summary card using shadcn-style card primitives.
export function ScoreCard({ score, status }: ScoreCardProps) {
  return (
    <Card className="w-full">
      <CardContent className="space-y-2">
        <p className="text-sm font-medium text-slate-500">Password Health Score</p>
        <p className={`text-4xl font-bold ${statusToColorClass(status)}`}>{score}</p>
        <p className={`text-lg font-semibold ${statusToColorClass(status)}`}>{status}</p>
      </CardContent>
    </Card>
  );
}
