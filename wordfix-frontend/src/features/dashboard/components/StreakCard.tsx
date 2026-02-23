import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { AnimatedCounter } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useStreak } from '@/features/review/hooks/useReview';
import GlowingBorder from './GlowingBorder';
import StreakFlame from './StreakFlame';
import StreakWeekDots from './StreakWeekDots';

export default function StreakCard() {
  const { data, isLoading, isError, refetch } = useStreak();
  const streak = data?.data;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 lg:p-6 shadow-card">
        <Skeleton className="h-20 w-full rounded-xl" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 lg:p-6 shadow-card flex flex-col items-center justify-center gap-2 text-center">
        <p className="text-xs text-muted-foreground">Could not load streak</p>
        <button onClick={() => refetch()} className="text-xs text-primary hover:underline">Retry</button>
      </div>
    );
  }

  const current = streak?.current_streak ?? 0;
  const best = streak?.longest_streak ?? 0;
  const isHotStreak = current > 7;

  // Build last 7 days active array from streak data
  const today = new Date().getDay();
  const currentIndex = today === 0 ? 6 : today - 1; // Mon=0
  const activeDays = Array.from({ length: 7 }, (_, i) => i <= currentIndex && current > currentIndex - i);

  const card = (
    <motion.div
      variants={staggerItem}
      className="relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br from-orange-500/[0.04] via-amber-500/[0.02] to-transparent p-5 lg:p-6 shadow-card"
    >
      <div className="flex flex-col items-center gap-2 text-center">
        <p className="text-[10px] font-semibold uppercase tracking-[0.1em] text-muted-foreground/50">
          STREAK
        </p>
        <StreakFlame active={current > 0} />
        <p className={`text-3xl font-heading font-bold ${current > 0 ? 'text-orange-500' : 'text-muted-foreground'}`}>
          <AnimatedCounter value={current} />
        </p>
        <p className="text-sm text-muted-foreground">days</p>
        <p className="text-[10px] text-muted-foreground/50">Best: {best} days</p>
        <StreakWeekDots activeDays={activeDays} currentDayIndex={currentIndex} />
      </div>
    </motion.div>
  );

  return isHotStreak ? (
    <GlowingBorder color="accent" active>{card}</GlowingBorder>
  ) : card;
}
