import { motion, AnimatePresence } from 'framer-motion';
import { Flame } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ComboIndicatorProps {
  combo: number;
  multiplier: number;
  isActive: boolean;
}

function getComboStyle(multiplier: number) {
  if (multiplier >= 5) {
    return {
      text: 'text-purple-500 dark:text-purple-400',
      bg: 'bg-purple-500/15',
      border: 'border-purple-500/30',
      glow: 'shadow-purple-500/25',
      pulse: true,
    };
  }
  if (multiplier >= 3) {
    return {
      text: 'text-red-500 dark:text-red-400',
      bg: 'bg-red-500/10',
      border: 'border-red-500/30',
      glow: 'shadow-red-500/20',
      pulse: false,
    };
  }
  if (multiplier >= 2) {
    return {
      text: 'text-orange-500 dark:text-orange-400',
      bg: 'bg-orange-500/10',
      border: 'border-orange-500/30',
      glow: '',
      pulse: false,
    };
  }
  return {
    text: 'text-yellow-500 dark:text-yellow-400',
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/30',
    glow: '',
    pulse: false,
  };
}

export function ComboIndicator({ combo, multiplier, isActive }: ComboIndicatorProps) {
  if (combo < 2 || !isActive) return null;

  const style = getComboStyle(multiplier);

  return (
    <AnimatePresence>
      <motion.div
        key={`combo-${combo}`}
        className={cn(
          'flex items-center justify-center gap-2 rounded-xl border px-4 py-2',
          style.bg,
          style.border,
          style.glow && `shadow-lg ${style.glow}`,
        )}
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{
          scale: [1.2, 1],
          opacity: 1,
        }}
        transition={{ type: 'spring', stiffness: 400, damping: 15, duration: 0.3 }}
        aria-live="polite"
        aria-label={`${combo} combo, ${multiplier}x XP multiplier`}
      >
        <motion.div
          animate={style.pulse ? { scale: [1, 1.2, 1] } : { scale: [1, 1.1, 1] }}
          transition={{ repeat: Infinity, duration: style.pulse ? 1.5 : 2 }}
        >
          <Flame className={cn('h-5 w-5', style.text)} />
        </motion.div>
        <div className="flex items-baseline gap-1.5">
          <motion.span
            key={`combo-num-${combo}`}
            className={cn('font-heading text-lg font-bold', style.text)}
            initial={{ scale: 1.3 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            x{combo}
          </motion.span>
          <span className={cn('text-xs font-semibold uppercase tracking-wider', style.text)}>
            Combo!
          </span>
        </div>
        <motion.div
          className={cn(
            'rounded-md px-2 py-0.5 text-xs font-bold',
            style.bg,
            style.text,
          )}
          key={`mult-${multiplier}`}
          initial={{ scale: 1.4 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 300, delay: 0.1 }}
        >
          {multiplier}x XP
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
