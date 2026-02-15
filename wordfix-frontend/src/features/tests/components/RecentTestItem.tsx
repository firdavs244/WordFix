import { cn } from '@/lib/utils';
import type { TestSession } from '@/types';

interface Props {
  test: TestSession;
}

export default function RecentTestItem({ test }: Props) {
  const pct = test.score_percentage;
  const color = pct >= 80 ? 'text-success stroke-success' : pct >= 60 ? 'text-yellow-500 stroke-yellow-500' : 'text-destructive stroke-destructive';
  const date = new Date(test.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  const r = 14;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;

  return (
    <div className="flex items-center justify-between rounded-lg px-3 py-2 transition-colors hover:bg-muted/30">
      <div className="flex items-center gap-3">
        <span className="text-xs text-muted-foreground">{date}</span>
        <span className="text-sm font-medium capitalize">{test.test_type.replace('_', ' ')}</span>
        <span className="text-xs text-muted-foreground">{test.total_questions} questions</span>
      </div>
      <div className="relative h-9 w-9">
        <svg className="h-9 w-9 -rotate-90" viewBox="0 0 36 36">
          <circle cx="18" cy="18" r={r} fill="none" strokeWidth="3" className="stroke-muted" />
          <circle
            cx="18" cy="18" r={r} fill="none" strokeWidth="3"
            strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
            className={cn(color)}
          />
        </svg>
        <span className={cn('absolute inset-0 flex items-center justify-center text-[9px] font-bold', color)}>
          {pct}
        </span>
      </div>
    </div>
  );
}
