import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Star } from 'lucide-react';
import confetti from 'canvas-confetti';
import { cn } from '@/lib/utils';

interface Props {
  score: number;
}

export default function GameResultStars({ score }: Props) {
  const stars = score >= 90 ? 3 : score >= 66 ? 2 : score >= 33 ? 1 : 0;

  useEffect(() => {
    if (stars === 3) confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
  }, [stars]);

  return (
    <div className="flex items-center justify-center gap-3" data-testid="result-stars">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, scale: 0.3 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 12, delay: i * 0.2 }}
        >
          <Star
            className={cn(
              'h-10 w-10',
              i < stars
                ? 'fill-accent text-accent drop-shadow-[0_0_8px_rgba(245,158,11,0.4)]'
                : 'text-muted-foreground/20',
            )}
            data-testid={i < stars ? 'star-filled' : 'star-empty'}
          />
        </motion.div>
      ))}
    </div>
  );
}
