import type { DifficultyLevel } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  difficulty: DifficultyLevel;
  partOfSpeech?: string;
  category?: string;
}

const difficultyStyles: Record<DifficultyLevel, string> = {
  easy: 'bg-success/10 text-success border-success/20',
  medium: 'bg-accent/10 text-accent border-accent/20',
  hard: 'bg-destructive/10 text-destructive border-destructive/20',
};

export default function WordCardBadges({ difficulty, partOfSpeech, category }: Props) {
  return (
    <div className="mt-3 flex flex-wrap gap-1.5 border-t border-border/30 pt-3">
      <span className={cn('rounded-full border px-2.5 py-1 text-[10px] font-semibold', difficultyStyles[difficulty])}>
        {difficulty}
      </span>
      {partOfSpeech && (
        <span className="rounded-full border border-border/30 px-2 py-0.5 text-[10px] font-medium text-muted-foreground">
          {partOfSpeech}
        </span>
      )}
      {category && (
        <span className="rounded-full border border-border/30 px-2 py-0.5 text-[10px] font-medium text-muted-foreground">
          <span className="mr-1 inline-block h-1 w-1 rounded-full bg-primary/50" />
          {category}
        </span>
      )}
    </div>
  );
}
