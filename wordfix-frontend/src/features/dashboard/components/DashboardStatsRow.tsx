import { motion } from 'framer-motion';
import { BookOpen, Brain, Target } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { StatCard } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useDashboardData } from '../hooks/useDashboardData';

export default function DashboardStatsRow() {
  const { stats, daily, isLoading } = useDashboardData();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
      </div>
    );
  }

  const total = stats?.total ?? 0;
  const learning = stats?.learning ?? 0;
  const dailyGoal = daily?.goal_completed ? 100 : Math.round(((daily?.words_reviewed ?? 0) / Math.max(1, 10)) * 100);

  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="grid grid-cols-1 sm:grid-cols-3 gap-4"
    >
      <StatCard label="Total Words" value={total} icon={BookOpen} />
      <StatCard label="Learning" value={learning} icon={Brain} variant="warning" />
      <StatCard label="Daily Goal" value={`${Math.min(dailyGoal, 100)}%`} icon={Target} variant="success" />
    </motion.div>
  );
}
