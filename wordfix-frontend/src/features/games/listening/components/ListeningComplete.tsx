import { CheckCircle2, XCircle } from 'lucide-react';
import type { ListeningCompleteResponse } from '@/types';

interface Props {
  data: ListeningCompleteResponse;
}

export default function ListeningComplete({ data }: Props) {
  return (
    <div className="space-y-4" data-testid="listening-complete">
      <div className="text-center">
        <p className="font-heading text-3xl font-bold">{data.accuracy_pct}%</p>
        <p className="text-sm text-muted-foreground">
          {data.total_score}/{data.max_score} points
        </p>
      </div>
      <div className="space-y-2">
        {data.rounds.map((r, i) => (
          <div key={i} className="flex items-center gap-3 rounded-lg border border-border/30 p-3">
            {r.is_correct ? (
              <CheckCircle2 className="h-4 w-4 text-success" />
            ) : (
              <XCircle className="h-4 w-4 text-destructive" />
            )}
            <span className="flex-1 text-sm font-medium">{r.word}</span>
            <span className="text-xs text-muted-foreground">{r.attempts_used} attempt(s)</span>
          </div>
        ))}
      </div>
    </div>
  );
}
