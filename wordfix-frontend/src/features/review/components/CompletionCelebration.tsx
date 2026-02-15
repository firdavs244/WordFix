import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { bounceIn } from '@/lib/motion';
import PerformanceTier from './PerformanceTier';
import { useConfetti } from '@/components/shared';

interface Props {
  accuracy: number;
}

export default function CompletionCelebration({ accuracy }: Props) {
  const { fireConfetti } = useConfetti();

  useEffect(() => {
    if (accuracy >= 70) fireConfetti({ particleCount: 120, spread: 80 });
  }, [accuracy, fireConfetti]);

  return (
    <motion.div variants={bounceIn} initial="initial" animate="animate" className="text-center">
      <PerformanceTier accuracy={accuracy} />
    </motion.div>
  );
}
