import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { bounceIn } from '@/lib/motion';

interface Props {
  onComplete: () => void;
}

const NUMS = [3, 2, 1, 'GO!'] as const;

export default function SpeedRoundCountdown({ onComplete }: Props) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index >= NUMS.length) { onComplete(); return; }
    const t = setTimeout(() => setIndex((i) => i + 1), 1000);
    return () => clearTimeout(t);
  }, [index, onComplete]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background">
      <AnimatePresence mode="wait">
        {index < NUMS.length && (
          <motion.span
            key={index}
            variants={bounceIn}
            initial="initial"
            animate="animate"
            exit={{ opacity: 0, scale: 1.5 }}
            className={`font-heading text-8xl font-bold ${
              NUMS[index] === 'GO!' ? 'text-accent' : 'text-primary'
            }`}
          >
            {NUMS[index]}
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  );
}
