import { motion } from 'framer-motion';
import { Flame, Trophy, Snowflake } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { useStreak } from '../hooks/useReview';
import { Skeleton } from '@/components/ui/skeleton';

interface StreakWidgetProps {
  compact?: boolean;
}

export function StreakWidget({ compact = false }: StreakWidgetProps) {
  const { data, isLoading } = useStreak();
  const streak = data?.data;

  if (isLoading) {
    return compact ? (
      <Skeleton className="h-8 w-20" />
    ) : (
      <Card className="border-border/50">
        <CardContent className="p-4">
          <Skeleton className="h-16 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!streak) return null;

  const isFrozen = streak.streak_frozen_until !== null;

  if (compact) {
    return (
      <div className="flex items-center gap-1.5">
        <motion.div
          animate={streak.current_streak > 0 ? { scale: [1, 1.2, 1] } : {}}
          transition={{ repeat: Infinity, duration: 2 }}
        >
          {isFrozen ? (
            <Snowflake className="h-5 w-5 text-blue-400" />
          ) : (
            <Flame className={`h-5 w-5 ${streak.current_streak > 0 ? 'text-orange-500' : 'text-muted-foreground'}`} />
          )}
        </motion.div>
        <span className="font-heading text-sm font-bold">
          {streak.current_streak}
        </span>
      </div>
    );
  }

  return (
    <Card className="border-border/50 overflow-hidden">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          <motion.div
            className="flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-500/10"
            animate={streak.current_streak > 0 ? { scale: [1, 1.05, 1] } : {}}
            transition={{ repeat: Infinity, duration: 2 }}
          >
            {isFrozen ? (
              <Snowflake className="h-7 w-7 text-blue-400" />
            ) : (
              <Flame className={`h-7 w-7 ${streak.current_streak > 0 ? 'text-orange-500' : 'text-muted-foreground'}`} />
            )}
          </motion.div>
          <div className="flex-1">
            <p className="text-sm text-muted-foreground">Current Streak</p>
            <p className="font-heading text-2xl font-bold">
              {streak.current_streak} <span className="text-sm font-normal text-muted-foreground">days</span>
            </p>
          </div>
          <div className="text-right">
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Trophy className="h-4 w-4 text-amber-500" />
              <span>Best: {streak.longest_streak}</span>
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              {streak.total_review_days} total days
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
