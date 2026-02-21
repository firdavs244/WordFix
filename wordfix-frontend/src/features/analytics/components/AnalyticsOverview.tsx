import { motion } from 'framer-motion';
import { BookOpen, Flame, Target, Zap, Clock, ClipboardCheck, Gamepad2, TrendingUp } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import AnalyticsStatCard from './AnalyticsStatCard';
import type { AnalyticsOverview as OverviewType } from '@/types';

interface AnalyticsOverviewProps {
  data: OverviewType;
}

export default function AnalyticsOverview({ data }: AnalyticsOverviewProps) {
  const cards = [
    { label: 'Total Words', value: data.total_words, icon: BookOpen },
    { label: 'Current Streak', value: `${data.current_streak}d`, icon: Flame, variant: 'warning' },
    { label: 'Accuracy', value: `${data.overall_accuracy}%`, icon: Target, variant: 'success' },
    { label: 'Total XP', value: data.total_xp.toLocaleString(), icon: Zap, variant: 'accent' },
    { label: 'Study Time', value: data.total_study_time_formatted, icon: Clock },
    { label: 'Tests Completed', value: data.tests_completed, icon: ClipboardCheck },
    { label: 'Games Played', value: data.games_played, icon: Gamepad2 },
    { label: 'Daily Average', value: `${data.avg_daily_words}w/d`, icon: TrendingUp, variant: 'primary' },
  ];

  return (
    <motion.div variants={staggerContainer} initial="initial" animate="animate" className="grid grid-cols-2 gap-3 md:grid-cols-4 lg:gap-4">
      {cards.map((c) => (
        <AnalyticsStatCard key={c.label} label={c.label} value={c.value} icon={c.icon} variant={c.variant} />
      ))}
    </motion.div>
  );
}
