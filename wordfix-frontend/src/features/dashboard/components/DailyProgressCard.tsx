import { motion } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';
import { staggerItem, bounceIn } from '@/lib/motion';
import { CircularProgress } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useDailyProgress } from '@/features/review/hooks/useReview';
import { useAuthStore } from '@/stores/useAuthStore';
import GlowingBorder from './GlowingBorder';

export default function DailyProgressCard() {
  const { data, isLoading } = useDailyProgress();
  const dailyGoal = useAuthStore((s) => s.user?.daily_goal ?? 10);
  const daily = data?.data;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 lg:p-6 shadow-card">
        <Skeleton className="h-20 w-full rounded-xl" />
      </div>
    );
  }

  const done = daily?.words_reviewed ?? 0;
  const pct = Math.min(Math.round((done / dailyGoal) * 100), 100);
  const isComplete = pct >= 100;
  const remaining = Math.max(dailyGoal - done, 0);

  const card = (
    <motion.div
      variants={staggerItem}
      className="relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br from-success/[0.03] to-emerald-400/[0.02] p-5 lg:p-6 shadow-card"
    >
      <div className="flex flex-col items-center gap-3 text-center">
        <p className="text-[10px] font-semibold uppercase tracking-[0.1em] text-muted-foreground/50">
          TODAY'S GOAL
        </p>
        <CircularProgress value={pct} size={80} strokeWidth={5} color="hsl(var(--success))">
          {isComplete ? (
            <motion.div variants={bounceIn} initial="initial" animate="animate">
              <CheckCircle2 className="h-7 w-7 text-success" />
            </motion.div>
          ) : (
            <span className="text-lg font-heading font-bold">
              {done}/{dailyGoal}
            </span>
          )}
        </CircularProgress>
        {isComplete ? (
          <p className="text-xs font-medium text-success">Goal achieved! 🎉</p>
        ) : (
          <p className="text-xs text-muted-foreground">{remaining} more to go</p>
        )}
        <p className="text-[10px] text-muted-foreground/40">Daily Goal: {dailyGoal} words</p>
      </div>
    </motion.div>
  );

  return isComplete ? (
    <GlowingBorder color="success" active>{card}</GlowingBorder>
  ) : card;
}
