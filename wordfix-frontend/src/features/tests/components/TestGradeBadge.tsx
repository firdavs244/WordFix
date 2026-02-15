import { useEffect } from 'react';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import { bounceIn } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface Props {
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  score: number;
}

const COLORS: Record<string, string> = {
  A: 'text-accent drop-shadow-[0_0_12px_rgba(245,158,11,0.4)]',
  B: 'text-primary drop-shadow-[0_0_12px_rgba(var(--primary),0.3)]',
  C: 'text-secondary',
  D: 'text-muted-foreground',
  F: 'text-destructive',
};

export default function TestGradeBadge({ grade, score }: Props) {
  useEffect(() => {
    if (grade === 'A' || grade === 'B') {
      confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
    }
  }, [grade]);

  return (
    <motion.div variants={bounceIn} initial="initial" animate="animate" className="text-center" data-testid="grade-badge">
      <span className={cn('font-heading text-6xl font-bold lg:text-7xl', COLORS[grade])} data-testid="grade-letter">
        {grade}
      </span>
      <p className="mt-2 text-xl text-muted-foreground" data-testid="grade-score">{score}%</p>
    </motion.div>
  );
}
