import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { AnimatedCounter } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useUserProgress } from '@/features/progress/hooks/useProgress';
import LevelRing from './LevelRing';

export default function LevelCard() {
  const { data, isLoading } = useUserProgress();
  const progress = data?.data;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 lg:p-6 shadow-card">
        <Skeleton className="h-20 w-full rounded-xl" />
      </div>
    );
  }

  const level = progress?.level ?? 1;
  const pct = progress?.progress_pct ?? 0;
  const xpCurrent = progress?.xp_progress ?? 0;
  const xpNeeded = progress?.xp_needed ?? 100;

  return (
    <motion.div
      variants={staggerItem}
      className="relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br from-primary/[0.04] via-transparent to-primary/[0.02] p-5 lg:p-6 shadow-card"
    >
      {/* Decorative blurred circles */}
      <div className="pointer-events-none absolute -right-8 -top-8 h-24 w-24 rounded-full bg-primary opacity-[0.03] blur-2xl" />
      <div className="pointer-events-none absolute -bottom-6 -left-6 h-20 w-20 rounded-full bg-primary opacity-[0.03] blur-2xl" />

      <div className="relative z-10 flex flex-col items-center gap-3 sm:flex-row sm:gap-4">
        <LevelRing level={level} progress={pct} size={88} />

        <div className="text-center sm:text-left">
          <p className="text-[10px] font-semibold uppercase tracking-[0.1em] text-muted-foreground/50">
            LEVEL
          </p>
          <p className="text-3xl font-heading font-bold text-primary">
            <AnimatedCounter value={level} />
          </p>
          <p className="text-xs text-muted-foreground">
            {xpCurrent} / {xpNeeded} XP
          </p>
          <p className="text-[10px] font-medium text-primary/60">→ Level {level + 1}</p>
        </div>
      </div>
    </motion.div>
  );
}
