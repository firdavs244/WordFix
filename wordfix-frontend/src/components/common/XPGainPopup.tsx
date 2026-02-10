import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Star } from 'lucide-react';
import { cn } from '@/lib/utils';

interface XPGainPopupProps {
  xp: number;
  multiplier?: number;
  combo?: number;
  onComplete?: () => void;
}

function getMultiplierColor(multiplier: number) {
  if (multiplier >= 5) return 'text-purple-400';
  if (multiplier >= 3) return 'text-red-400';
  if (multiplier >= 2) return 'text-orange-400';
  return 'text-yellow-400';
}

export function XPGainPopup({ xp, multiplier, onComplete }: XPGainPopupProps) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (xp > 0) {
      setShow(true);
      const timer = setTimeout(() => {
        setShow(false);
        onComplete?.();
      }, 1800);
      return () => clearTimeout(timer);
    }
  }, [xp, onComplete]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="pointer-events-none fixed left-1/2 top-24 z-50 -translate-x-1/2"
          initial={{ opacity: 0, y: 10, scale: 0.8 }}
          animate={{ opacity: 1, y: -20, scale: 1 }}
          exit={{ opacity: 0, y: -60 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
          <div className="flex items-center gap-1.5 rounded-full bg-primary/90 px-4 py-2 text-white shadow-xl shadow-primary/30">
            <Star className="h-4 w-4 fill-white" />
            <span className="font-heading text-base font-bold">
              +{xp} XP
            </span>
            {multiplier && multiplier > 1 && (
              <span className={cn('text-sm font-semibold', getMultiplierColor(multiplier))}>
                ({multiplier}x)
              </span>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
