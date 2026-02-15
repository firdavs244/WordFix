import { useState } from 'react';
import { History } from 'lucide-react';
import { EmptyState } from '@/components/shared';
import ReviewHistoryItem from './ReviewHistoryItem';
import { useReviewHistory } from '../hooks/useReview';

export default function ReviewHistoryList() {
  const [page] = useState(1);
  const { data, isLoading } = useReviewHistory(page, 10);
  const sessions = data?.data ?? [];

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => <div key={i} className="h-20 animate-pulse rounded-xl bg-muted" />)}
      </div>
    );
  }

  if (sessions.length === 0) {
    return <EmptyState icon={History} title="No review history" description="Start reviewing to see your history" action={{ label: 'Start Reviewing', href: '/review' }} />;
  }

  return (
    <div className="divide-y divide-border/30 rounded-2xl border border-border/50 bg-card shadow-card">
      {sessions.map((s) => <ReviewHistoryItem key={s.id} session={s} />)}
    </div>
  );
}
