import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { DifficultWord } from '@/types';

interface DifficultWordItemProps {
  word: DifficultWord;
  rank: number;
}

export default function DifficultWordItem({ word, rank }: DifficultWordItemProps) {
  const accuracy = Math.round(word.accuracy_rate);

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: rank * 0.05 }}
      className="flex items-center gap-3 rounded-lg border border-border/30 px-3 py-2"
    >
      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-muted text-[10px] font-bold">
        {rank + 1}
      </span>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-semibold">{word.original_word}</p>
        <p className="truncate text-xs text-muted-foreground">{word.translation}</p>
      </div>
      <div className="flex items-center gap-2">
        <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted/50">
          <div
            className={cn(
              'h-full rounded-full transition-all',
              accuracy >= 70 ? 'bg-amber-400' : 'bg-red-400',
            )}
            style={{ width: `${accuracy}%` }}
          />
        </div>
        <span className="text-xs font-medium text-muted-foreground">{accuracy}%</span>
      </div>
    </motion.div>
  );
}
