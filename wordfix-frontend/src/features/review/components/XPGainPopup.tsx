import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Star } from 'lucide-react';
import { floatUp } from '@/lib/motion';

interface Props {
  xp: number;
  multiplier?: number;
  onDone?: () => void;
}

export default function XPGainPopup({ xp, multiplier, onDone }: Props) {
  useEffect(() => {
    const t = setTimeout(() => onDone?.(), 1800);
    return () => clearTimeout(t);
  }, [onDone]);

  return (
    <motion.div
      variants={floatUp}
      initial="initial"
      animate="animate"
      exit="exit"
      className="pointer-events-none fixed bottom-1/3 left-1/2 z-30 -translate-x-1/2"
    >
      <div className="flex items-center gap-1.5 text-accent">
        <Star className="h-3.5 w-3.5" />
        <span className="font-heading text-lg font-bold">+{xp} XP</span>
      </div>
      {multiplier && multiplier > 1 && (
        <p className="text-center text-xs text-accent/70">×{multiplier} combo!</p>
      )}
    </motion.div>
  );
}
