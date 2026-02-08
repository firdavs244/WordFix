import { useState } from 'react';
import { motion } from 'framer-motion';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { useUserBadges } from '../hooks/useProgress';
import { BadgeCard } from './BadgeCard';
import type { BadgeCategory } from '@/types';
import { listContainerVariants, listItemVariants } from '@/components/animations/PageTransition';

const categories: { value: BadgeCategory | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'words', label: 'Words' },
  { value: 'streak', label: 'Streak' },
  { value: 'review', label: 'Review' },
  { value: 'test', label: 'Tests' },
  { value: 'game', label: 'Games' },
  { value: 'mastery', label: 'Mastery' },
  { value: 'level', label: 'Level' },
];

export function BadgeGrid() {
  const { data, isLoading } = useUserBadges();
  const [filter, setFilter] = useState<BadgeCategory | 'all'>('all');

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-40 rounded-xl" />
        ))}
      </div>
    );
  }

  const badges = data?.data?.badges ?? [];
  const filtered = filter === 'all' ? badges : badges.filter((b) => b.category === filter);
  const earnedCount = data?.data?.earned_count ?? 0;
  const totalCount = data?.data?.total_count ?? 0;

  return (
    <div className="space-y-4">
      {/* Counter */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          <span className="font-semibold text-foreground">{earnedCount}</span> / {totalCount} badges earned
        </p>
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <Badge
            key={cat.value}
            variant={filter === cat.value ? 'default' : 'outline'}
            className="cursor-pointer"
            onClick={() => setFilter(cat.value)}
          >
            {cat.label}
          </Badge>
        ))}
      </div>

      {/* Grid */}
      <motion.div
        className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4"
        variants={listContainerVariants}
        initial="hidden"
        animate="show"
        key={filter}
      >
        {filtered.map((badge) => (
          <motion.div key={badge.code} variants={listItemVariants}>
            <BadgeCard badge={badge} />
          </motion.div>
        ))}
      </motion.div>

      {filtered.length === 0 && (
        <p className="py-8 text-center text-muted-foreground">No badges in this category.</p>
      )}
    </div>
  );
}
