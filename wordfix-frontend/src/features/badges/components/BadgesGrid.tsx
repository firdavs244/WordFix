import { motion } from 'framer-motion';
import { Award } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import EmptyState from '@/components/shared/EmptyState';
import { staggerContainer, staggerItem } from '@/lib/motion';
import { useBadges } from '../hooks/useBadges';
import BadgeCard from './BadgeCard';

interface BadgesGridProps {
  category?: string;
}

export default function BadgesGrid({ category = 'all' }: BadgesGridProps) {
  const { badges, isLoading } = useBadges();

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 lg:gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-44 rounded-2xl" />
        ))}
      </div>
    );
  }

  const filtered = category === 'all' ? badges : badges.filter((b) => b.category === category);

  if (filtered.length === 0) {
    return <EmptyState icon={Award} title="No badges in this category" description="Try a different category filter" />;
  }

  return (
    <motion.div
      className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 lg:gap-4"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
    >
      {filtered.map((badge) => (
        <motion.div key={badge.id} variants={staggerItem}>
          <BadgeCard badge={badge} />
        </motion.div>
      ))}
    </motion.div>
  );
}
