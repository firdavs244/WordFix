import { LearningStyleBar } from './LearningStyleBar';
import { Badge } from '@/components/ui/badge';

interface Props {
  name: string;
  label: string;
  score: number;
  isStrong: boolean;
  isWeak: boolean;
  delay?: number;
}

export function SkillBar({
  label,
  score,
  isStrong,
  isWeak,
  delay = 0,
}: Props) {
  const barColor = isStrong
    ? 'bg-green-500'
    : isWeak
      ? 'bg-red-400'
      : 'bg-primary';

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">
            {Math.round(score)}%
          </span>
          {isStrong && (
            <Badge variant="outline" className="border-green-300 bg-green-50 text-green-700 dark:border-green-800 dark:bg-green-950 dark:text-green-300">
              Strong
            </Badge>
          )}
          {isWeak && (
            <Badge variant="outline" className="border-red-300 bg-red-50 text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
              Needs work
            </Badge>
          )}
        </div>
      </div>
      <LearningStyleBar value={score} color={barColor} delay={delay} />
    </div>
  );
}
