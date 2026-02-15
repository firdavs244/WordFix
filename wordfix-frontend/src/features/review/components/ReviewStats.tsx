import { motion } from 'framer-motion';
import { Brain, CalendarCheck, Target, BarChart3 } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { StatCard } from '@/components/shared';
import { useReviewSummary } from '../hooks/useReview';

export default function ReviewStats() {
  const { data } = useReviewSummary();
  const s = data?.data;

  return (
    <motion.div variants={staggerContainer} initial="initial" animate="animate" className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      <StatCard label="Words Due" value={s?.words_due ?? 0} icon={Brain} variant="primary" />
      <StatCard label="Today" value={s?.reviews_today ?? 0} icon={CalendarCheck} variant="success" />
      <StatCard label="Accuracy" value={`${s?.average_accuracy ?? 0}%`} icon={Target} variant="warning" />
      <StatCard label="Total Reviews" value={s?.total_reviews ?? 0} icon={BarChart3} variant="accent" />
    </motion.div>
  );
}
