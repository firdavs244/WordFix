import { motion } from 'framer-motion';
import { Award } from 'lucide-react';
import AnimatedCounter from '@/components/shared/AnimatedCounter';
import { useBadges } from '../hooks/useBadges';

export default function BadgesProgress() {
  const { earnedCount, totalCount, isLoading } = useBadges();

  if (isLoading) return null;

  const percentage = totalCount > 0 ? Math.round((earnedCount / totalCount) * 100) : 0;

  return (
    <div className="rounded-2xl shadow-card border border-border/50 p-5 bg-card">
      <div className="flex items-center gap-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-accent/10">
          <Award className="h-5 w-5 text-accent" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-heading font-semibold">
            {earnedCount} / {totalCount} badges earned
          </p>
          <div className="h-2.5 rounded-full bg-muted overflow-hidden mt-2">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-accent to-amber-400"
              initial={{ width: 0 }}
              animate={{ width: `${percentage}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          </div>
        </div>
        <div className="text-xl font-heading font-bold text-accent">
          <AnimatedCounter value={percentage} />%
        </div>
      </div>
    </div>
  );
}
