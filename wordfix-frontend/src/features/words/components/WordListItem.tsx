import { motion } from 'framer-motion';
import { Trash2 } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import type { Word, DifficultyLevel } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  word: Word;
  onDelete: (id: string) => void;
}

const badgeColors: Record<DifficultyLevel, string> = {
  easy: 'bg-success/10 text-success',
  medium: 'bg-accent/10 text-accent',
  hard: 'bg-destructive/10 text-destructive',
};

export default function WordListItem({ word, onDelete }: Props) {
  return (
    <motion.div
      variants={staggerItem}
      className="grid grid-cols-12 items-center px-5 py-3.5 transition-colors hover:bg-muted/20"
    >
      <span className="col-span-4 font-heading text-sm font-semibold">{word.original_word}</span>
      <span className="col-span-3 text-sm text-muted-foreground">{word.translation}</span>
      <span className="col-span-2">
        <span className={cn('rounded-full px-2 py-0.5 text-[10px] font-semibold', badgeColors[word.difficulty_level])}>
          {word.difficulty_level}
        </span>
      </span>
      <span className="col-span-2 text-xs text-muted-foreground">{word.category?.name ?? '—'}</span>
      <span className="col-span-1">
        <button
          onClick={() => onDelete(word.id)}
          className="flex h-7 w-7 items-center justify-center rounded-lg transition-colors hover:bg-destructive/10"
          aria-label={`Delete ${word.original_word}`}
        >
          <Trash2 className="h-3.5 w-3.5 text-muted-foreground hover:text-destructive" />
        </button>
      </span>
    </motion.div>
  );
}
