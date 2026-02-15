import { PageTransition, PageHeader } from '@/components/shared';
import { History } from 'lucide-react';
import ReviewHistoryList from './components/ReviewHistoryList';

export default function ReviewHistoryPage() {
  return (
    <PageTransition>
      <div className="mx-auto max-w-3xl space-y-6">
        <PageHeader title="Review History" icon={History} backLink="/review" />
        <ReviewHistoryList />
      </div>
    </PageTransition>
  );
}
