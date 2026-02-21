import { cn } from '@/lib/utils';

interface CalendarCellProps {
  date: string;
  wordCount: number;
  goalCompleted: boolean;
}

function getIntensity(count: number): string {
  if (count === 0) return 'bg-muted/50';
  if (count <= 2) return 'bg-emerald-200/60 dark:bg-emerald-900/40';
  if (count <= 5) return 'bg-emerald-300/70 dark:bg-emerald-800/50';
  if (count <= 10) return 'bg-emerald-400/80 dark:bg-emerald-700/60';
  return 'bg-emerald-500 dark:bg-emerald-600';
}

export default function CalendarCell({ date, wordCount, goalCompleted }: CalendarCellProps) {
  return (
    <div
      title={`${date}: ${wordCount} words reviewed`}
      className={cn(
        'h-3.5 w-3.5 rounded-sm transition-all hover:ring-2 hover:ring-foreground/10 md:h-4 md:w-4',
        getIntensity(wordCount),
        goalCompleted && 'ring-1 ring-emerald-600/30',
      )}
    />
  );
}
