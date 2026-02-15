import { PageTransition, PageHeader } from '@/components/shared';
import { Brain } from 'lucide-react';
import ReviewStats from './components/ReviewStats';
import SessionTypeCards from './components/SessionTypeCards';
import DueWordsPreview from './components/DueWordsPreview';

export default function ReviewPage() {
  return (
    <PageTransition>
      <div className="space-y-8">
        <PageHeader title="Review" description="Master your vocabulary with spaced repetition" icon={Brain} />
        <ReviewStats />
        <SessionTypeCards />
        <DueWordsPreview />
      </div>
    </PageTransition>
  );
}
