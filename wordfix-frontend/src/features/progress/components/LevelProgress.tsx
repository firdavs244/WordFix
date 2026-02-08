import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useUserProgress } from '../hooks/useProgress';

interface LevelProgressProps {
  compact?: boolean;
}

export function LevelProgress({ compact = false }: LevelProgressProps) {
  const { data, isLoading } = useUserProgress();
  const progress = data?.data;

  if (isLoading) {
    return compact ? (
      <Skeleton className="h-8 w-24" />
    ) : (
      <Card className="border-border/50">
        <CardContent className="p-4">
          <Skeleton className="h-16 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!progress) return null;

  if (compact) {
    return (
      <div className="flex items-center gap-2">
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary/10">
          <span className="text-xs font-bold text-primary">{progress.level}</span>
        </div>
        <div className="flex flex-col">
          <div className="h-1.5 w-16 rounded-full bg-muted overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-primary"
              initial={{ width: 0 }}
              animate={{ width: `${progress.progress_pct}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <span className="text-[10px] text-muted-foreground">
            {progress.total_xp} XP
          </span>
        </div>
      </div>
    );
  }

  return (
    <Card className="border-border/50 overflow-hidden">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          <motion.div
            className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10"
            whileHover={{ scale: 1.05 }}
          >
            <div className="text-center">
              <TrendingUp className="mx-auto h-5 w-5 text-primary" />
              <span className="text-xs font-bold text-primary">Lv.{progress.level}</span>
            </div>
          </motion.div>
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">Level {progress.level}</p>
              <p className="text-sm font-medium text-primary">{progress.total_xp} XP</p>
            </div>
            <div className="mt-1.5 h-3 rounded-full bg-muted overflow-hidden">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary to-primary/70"
                initial={{ width: 0 }}
                animate={{ width: `${progress.progress_pct}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
            <div className="mt-1 flex justify-between text-xs text-muted-foreground">
              <span>{progress.xp_progress} / {progress.xp_needed} XP</span>
              <span>Level {progress.level + 1}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
