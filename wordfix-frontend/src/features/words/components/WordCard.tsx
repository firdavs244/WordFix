import { Trash2 } from 'lucide-react';
import MouseTiltCard from '@/features/dashboard/components/MouseTiltCard';
import WordCardBadges from './WordCardBadges';
import type { Word } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  word: Word;
  onDelete: (id: string) => void;
}

const borderColors = {
  easy: 'border-l-success',
  medium: 'border-l-accent',
  hard: 'border-l-destructive',
};

export default function WordCard({ word, onDelete }: Props) {
  return (
    <MouseTiltCard tiltAmount={2}>
      <div
        className={cn(
          'group relative overflow-hidden rounded-2xl border border-border/50 border-l-4 bg-card p-5 shadow-card transition-all hover:border-border hover:shadow-card-hover',
          borderColors[word.difficulty_level],
        )}
        role="article"
        aria-label={`Word: ${word.original_word}`}
      >
        {/* Delete button */}
        <button
          onClick={() => onDelete(word.id)}
          className="absolute right-3 top-3 flex h-7 w-7 items-center justify-center rounded-lg opacity-0 transition-opacity hover:bg-destructive/10 group-hover:opacity-100"
          aria-label={`Delete ${word.original_word}`}
        >
          <Trash2 className="h-3.5 w-3.5 text-muted-foreground hover:text-destructive" />
        </button>

        <h3 className="font-heading text-lg font-bold tracking-tight">{word.original_word}</h3>
        <p className="mt-1 text-sm text-muted-foreground">{word.translation}</p>
        {word.definition && (
          <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-muted-foreground/70">{word.definition}</p>
        )}

        <WordCardBadges difficulty={word.difficulty_level} partOfSpeech={word.part_of_speech} category={word.category?.name} />
      </div>
    </MouseTiltCard>
  );
}
