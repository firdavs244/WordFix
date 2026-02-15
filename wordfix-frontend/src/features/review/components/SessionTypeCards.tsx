import { Brain, Sparkles, Shuffle } from 'lucide-react';
import SessionTypeCard from './SessionTypeCard';
import { useReviewWords } from '../hooks/useReview';

export default function SessionTypeCards() {
  const { data } = useReviewWords('review');
  const dueCount = data?.data?.length ?? 0;

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-3 lg:gap-6">
      <SessionTypeCard
        type="review"
        title="Review Due"
        description="Practice words scheduled for today"
        icon={Brain}
        gradient="from-primary/10 to-violet-500/5"
        iconGradient="from-primary to-violet-500"
        count={dueCount}
        disabled={dueCount === 0}
      />
      <SessionTypeCard
        type="learn"
        title="Learn New"
        description="Start learning fresh words"
        icon={Sparkles}
        gradient="from-secondary/10 to-cyan-400/5"
        iconGradient="from-secondary to-cyan-400"
      />
      <SessionTypeCard
        type="mixed"
        title="Mixed Practice"
        description="Blend of due and new words"
        icon={Shuffle}
        gradient="from-accent/10 to-orange-400/5"
        iconGradient="from-accent to-orange-400"
      />
    </div>
  );
}
