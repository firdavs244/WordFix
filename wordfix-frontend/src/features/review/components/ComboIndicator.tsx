import { motion, AnimatePresence } from 'framer-motion';
import { Flame } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Props {
  combo: number;
  multiplier: number;
}

function getStyle(combo: number) {
  if (combo >= 20) return 'bg-primary/10 border-primary/20 text-primary shadow-glow-primary';
  if (combo >= 10) return 'bg-red-500/10 border-red-500/20 text-red-600';
  if (combo >= 5) return 'bg-orange-500/10 border-orange-500/20 text-orange-600';
  return 'bg-yellow-500/10 border-yellow-500/20 text-yellow-600';
}

export default function ComboIndicator({ combo, multiplier }: Props) {
  return (
    <AnimatePresence>
      {combo > 1 && (
        <motion.div
          key={combo}
          initial={{ scale: 0.3, opacity: 0 }}
          animate={{ scale: [1.2, 1], opacity: 1 }}
          exit={{ scale: 0.3, opacity: 0 }}
          className={cn('fixed right-4 top-20 z-20 rounded-2xl border px-4 py-2.5 shadow-lg lg:right-8', getStyle(combo))}
          data-testid="combo-indicator"
        >
          <div className="flex items-center gap-1.5">
            <Flame className="h-4 w-4" />
            <span className="font-heading text-lg font-bold">{combo}</span>
          </div>
          <p className="text-xs font-semibold">×{multiplier}</p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
