import { motion } from 'framer-motion';
import { CheckCircle2, BookOpen, Brain, Clock, Star } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useDailyProgress } from '../hooks/useReview';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuthStore } from '@/stores/useAuthStore';

export function DailyProgressWidget() {
  const { data, isLoading } = useDailyProgress();
  const user = useAuthStore((s) => s.user);
  const progress = data?.data;
  const dailyGoal = user?.daily_goal ?? 10;

  if (isLoading) {
    return (
      <Card className="border-border/50">
        <CardContent className="p-4">
          <Skeleton className="h-24 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!progress) return null;

  const goalPercent = Math.min((progress.words_reviewed / dailyGoal) * 100, 100);
  const accuracy =
    progress.correct_answers + progress.incorrect_answers > 0
      ? Math.round(
          (progress.correct_answers /
            (progress.correct_answers + progress.incorrect_answers)) *
            100,
        )
      : 0;

  const minutes = Math.round(progress.total_time_seconds / 60);

  return (
    <Card className="border-border/50 overflow-hidden">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-lg">
          <Star className="h-5 w-5 text-amber-500" />
          Today's Progress
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Goal Progress Bar */}
        <div>
          <div className="mb-1 flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Daily Goal</span>
            <span className="font-medium">
              {progress.words_reviewed}/{dailyGoal} words
            </span>
          </div>
          <div className="h-3 overflow-hidden rounded-full bg-muted">
            <motion.div
              className={`h-full rounded-full ${
                progress.goal_completed ? 'bg-success' : 'bg-primary'
              }`}
              initial={{ width: 0 }}
              animate={{ width: `${goalPercent}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          </div>
          {progress.goal_completed && (
            <motion.div
              className="mt-1 flex items-center gap-1 text-xs text-success"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <CheckCircle2 className="h-3 w-3" />
              Goal completed!
            </motion.div>
          )}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3">
          <div className="flex items-center gap-2 rounded-lg bg-muted/50 p-2">
            <BookOpen className="h-4 w-4 text-primary" />
            <div>
              <p className="text-xs text-muted-foreground">Reviewed</p>
              <p className="font-heading text-sm font-bold">{progress.words_reviewed}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-lg bg-muted/50 p-2">
            <Brain className="h-4 w-4 text-purple-500" />
            <div>
              <p className="text-xs text-muted-foreground">Accuracy</p>
              <p className="font-heading text-sm font-bold">{accuracy}%</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-lg bg-muted/50 p-2">
            <CheckCircle2 className="h-4 w-4 text-success" />
            <div>
              <p className="text-xs text-muted-foreground">Mastered</p>
              <p className="font-heading text-sm font-bold">{progress.words_mastered}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-lg bg-muted/50 p-2">
            <Clock className="h-4 w-4 text-blue-500" />
            <div>
              <p className="text-xs text-muted-foreground">Time</p>
              <p className="font-heading text-sm font-bold">{minutes}m</p>
            </div>
          </div>
        </div>

        {/* XP */}
        {progress.xp_earned > 0 && (
          <div className="text-center text-sm text-muted-foreground">
            <span className="font-bold text-amber-500">+{progress.xp_earned} XP</span> earned today
          </div>
        )}
      </CardContent>
    </Card>
  );
}
