import { Link } from 'react-router-dom';
import { Clock, CheckCircle2 } from 'lucide-react';
import DueWordItem from './DueWordItem';
import { useReviewWords } from '../hooks/useReview';

export default function DueWordsPreview() {
  const { data } = useReviewWords('review', 5);
  const words = data?.data ?? [];

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center gap-2 px-5 pt-5">
        <Clock className="h-4 w-4 text-muted-foreground" />
        <h3 className="font-heading text-sm font-semibold">Upcoming Reviews</h3>
      </div>

      {words.length === 0 ? (
        <div className="flex flex-col items-center gap-2 px-5 py-8 text-center">
          <CheckCircle2 className="h-8 w-8 text-success" />
          <p className="text-sm text-muted-foreground">No words due for review</p>
        </div>
      ) : (
        <div className="divide-y divide-border/30">
          {words.slice(0, 5).map((word) => (
            <DueWordItem key={word.id} word={word} />
          ))}
        </div>
      )}

      <div className="px-5 pb-4 pt-2">
        <Link to="/review/history" className="text-xs font-medium text-primary hover:underline">
          View History →
        </Link>
      </div>
    </div>
  );
}
