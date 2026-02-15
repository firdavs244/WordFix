import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';
import type { Word } from '@/types';

const difficultyStyles: Record<string, string> = {
  easy: 'bg-success/10 text-success border-success/20',
  medium: 'bg-accent/10 text-accent border-accent/20',
  hard: 'bg-destructive/10 text-destructive border-destructive/20',
};

export default function RecentWordItem({ word }: { word: Word }) {
  return (
    <motion.div
      variants={staggerItem}
      className="group -mx-2 flex items-center gap-3 rounded-lg px-2 py-3 transition-colors hover:bg-muted/20"
    >
      <div className="flex-1 min-w-0">
        <p className="text-sm font-heading font-semibold truncate">{word.original_word}</p>
        <p className="text-xs text-muted-foreground truncate">{word.translation}</p>
      </div>
      <span
        className={cn(
          'shrink-0 rounded-full border px-2.5 py-1 text-[10px] font-medium',
          difficultyStyles[word.difficulty_level] ?? difficultyStyles.medium,
        )}
      >
        {word.difficulty_level}
      </span>
    </motion.div>
  );
}
