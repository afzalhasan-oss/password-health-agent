import { Progress } from "@/components/ui/progress";
import { statusToProgressClass, type ScoreStatus } from "@/lib/score-color";

type ScoreProgressProps = {
  score: number;
  status: ScoreStatus;
};

// Renders a color-coded progress bar tied to score and status.
export function ScoreProgress({ score, status }: ScoreProgressProps) {
  return (
    <div className="space-y-2">
      <p className="text-sm text-slate-600">Score Progress</p>
      <Progress value={score} indicatorClassName={statusToProgressClass(status)} />
    </div>
  );
}
