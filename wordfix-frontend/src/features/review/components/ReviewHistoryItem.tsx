import type { ReviewSession } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  session: ReviewSession;
}

export default function ReviewHistoryItem({ session }: Props) {
  const accuracy = session.total_words > 0 ? Math.round((session.correct_count / session.total_words) * 100) : 0;
  const date = new Date(session.started_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  return (
    <div className="flex items-center gap-4 px-5 py-4">
      <div className={cn('h-2.5 w-2.5 shrink-0 rounded-full', session.is_completed ? 'bg-success' : 'bg-warning')} />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium">{date}</p>
        <p className="text-xs text-muted-foreground">{session.total_words} words reviewed</p>
      </div>
      <span className={cn(
        'rounded-full px-2.5 py-1 text-xs font-semibold',
        accuracy >= 70 ? 'bg-success/10 text-success' : accuracy >= 50 ? 'bg-warning/10 text-warning' : 'bg-destructive/10 text-destructive',
      )}>
        {accuracy}%
      </span>
    </div>
  );
}
