import { useState } from 'react';
import { Award } from 'lucide-react';
import PageHeader from '@/components/shared/PageHeader';
import PageTransition from '@/components/shared/PageTransition';
import BadgesProgress from './components/BadgesProgress';
import BadgesCategoryFilter from './components/BadgesCategoryFilter';
import BadgesGrid from './components/BadgesGrid';

export function BadgesPage() {
  const [category, setCategory] = useState('all');

  return (
    <PageTransition>
      <PageHeader title="Badges & Achievements" description="Your learning accomplishments" icon={Award} />
      <div className="space-y-6 mt-6">
        <BadgesProgress />
        <BadgesCategoryFilter activeCategory={category} onChange={setCategory} />
        <BadgesGrid category={category} />
      </div>
    </PageTransition>
  );
}

export default BadgesPage;
