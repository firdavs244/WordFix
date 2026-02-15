import { motion } from 'framer-motion';
import { bounceIn } from '@/lib/motion';

interface Props {
  accuracy: number;
}

function getTier(acc: number) {
  if (acc >= 90) return { emoji: '🏆', message: 'Outstanding!', color: 'text-accent' };
  if (acc >= 70) return { emoji: '🌟', message: 'Great job!', color: 'text-success' };
  if (acc >= 50) return { emoji: '💪', message: 'Good effort!', color: 'text-secondary' };
  return { emoji: '📚', message: 'Keep practicing!', color: 'text-primary' };
}

export default function PerformanceTier({ accuracy }: Props) {
  const tier = getTier(accuracy);
  return (
    <div className="text-center">
      <motion.p variants={bounceIn} initial="initial" animate="animate" className="text-5xl">{tier.emoji}</motion.p>
      <h2 className={`mt-3 font-heading text-xl font-bold ${tier.color}`}>{tier.message}</h2>
    </div>
  );
}
