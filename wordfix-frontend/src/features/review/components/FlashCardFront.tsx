import { Volume2, Sparkles } from 'lucide-react';
import type { Word, DifficultyLevel } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  word: Word;
}

const badgeColors: Record<DifficultyLevel, string> = {
  easy: 'bg-success/10 text-success border-success/20',
  medium: 'bg-accent/10 text-accent border-accent/20',
  hard: 'bg-destructive/10 text-destructive border-destructive/20',
};

export default function FlashCardFront({ word }: Props) {
  return (
    <div
      className="absolute inset-0 flex flex-col items-center justify-center rounded-3xl border border-border/30 bg-card p-6 text-center shadow-xl lg:p-8"
      style={{ backfaceVisibility: 'hidden' }}
    >
      <span className={cn('absolute left-4 top-4 rounded-full border px-2.5 py-1 text-[10px] font-semibold', badgeColors[word.difficulty_level])}>
        {word.difficulty_level}
      </span>

      <h2 className="font-heading text-2xl font-bold tracking-tight lg:text-3xl">{word.original_word}</h2>
      {word.pronunciation && <p className="mt-2 text-sm italic text-muted-foreground/60">/{word.pronunciation}/</p>}

      {word.audio_url && (
        <button
          onClick={(e) => { e.stopPropagation(); new Audio(word.audio_url).play(); }}
          className="mt-4 flex h-10 w-10 items-center justify-center rounded-full border border-border/50 bg-muted/30 transition-colors hover:border-primary/30 hover:bg-primary/10"
          aria-label="Play pronunciation"
        >
          <Volume2 className="h-[18px] w-[18px] text-muted-foreground" />
        </button>
      )}

      <div className="mt-6 flex animate-pulse items-center gap-1.5 text-xs text-muted-foreground/40">
        <Sparkles className="h-3 w-3" />
        <span>Tap to reveal</span>
      </div>
    </div>
  );
}
