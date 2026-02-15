import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { BookOpen } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { EmptyState } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useDashboardData } from '../hooks/useDashboardData';
import RecentWordItem from './RecentWordItem';

export default function RecentWordsList() {
  const { recentWords, isLoading } = useDashboardData();

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 shadow-card">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <Skeleton key={i} className="h-12 rounded-lg" />)}
        </div>
      </div>
    );
  }

  const words = Array.isArray(recentWords) ? recentWords : (recentWords as any)?.results ?? [];

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center justify-between px-5 lg:px-6 pt-5">
        <div className="flex items-center gap-2">
          <BookOpen className="h-[18px] w-[18px] text-primary" />
          <h3 className="text-base font-heading font-semibold">Recent Words</h3>
        </div>
        <Link to="/words" className="text-xs font-medium text-primary hover:underline">
          View All →
        </Link>
      </div>

      {words.length === 0 ? (
        <div className="px-5 pb-5">
          <EmptyState
            icon={BookOpen}
            title="No words yet"
            description="Add your first word to get started"
            action={{ label: 'Add Words', href: '/words' }}
          />
        </div>
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="divide-y divide-border/30 px-5 lg:px-6 py-4"
        >
          {words.slice(0, 5).map((word: any) => (
            <RecentWordItem key={word.id} word={word} />
          ))}
        </motion.div>
      )}
    </div>
  );
}
