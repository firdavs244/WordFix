import type { Word, DifficultyLevel } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  word: Word;
}

const badgeColors: Record<DifficultyLevel, string> = {
  easy: 'bg-success/10 text-success',
  medium: 'bg-accent/10 text-accent',
  hard: 'bg-destructive/10 text-destructive',
};

export default function DueWordItem({ word }: Props) {
  return (
    <div className="flex items-center gap-3 px-5 py-3">
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">{word.original_word}</p>
        <p className="truncate text-xs text-muted-foreground">{word.translation}</p>
      </div>
      <span className={cn('shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold', badgeColors[word.difficulty_level])}>
        {word.difficulty_level}
      </span>
    </div>
  );
}
