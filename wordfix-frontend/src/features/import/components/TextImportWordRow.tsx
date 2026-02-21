import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { WordSuggestion } from '@/types';

interface TextImportWordRowProps {
  word: WordSuggestion;
  isSelected: boolean;
  onToggle: () => void;
}

const diffColors: Record<string, string> = {
  easy: 'bg-success/10 text-success',
  medium: 'bg-warning/10 text-warning',
  hard: 'bg-destructive/10 text-destructive',
};

export default function TextImportWordRow({ word, isSelected, onToggle }: TextImportWordRowProps) {
  return (
    <button
      onClick={onToggle}
      className={cn(
        'flex w-full items-center gap-3 px-5 py-3 text-left transition-colors hover:bg-muted/20',
        isSelected && 'bg-primary/[0.03]',
      )}
    >
      <div
        className={cn(
          'flex h-[18px] w-[18px] shrink-0 items-center justify-center rounded-md border-2 transition-all',
          isSelected ? 'border-primary bg-primary' : 'border-border/50',
        )}
      >
        {isSelected && <Check className="h-3 w-3 text-white" />}
      </div>
      <div className="min-w-0 flex-1">
        <span className="font-heading text-sm font-semibold">{word.word}</span>
        <span className="ml-2 text-xs text-muted-foreground">{word.translation}</span>
        {word.context_sentence && (
          <p className="mt-0.5 line-clamp-1 text-[10px] italic text-muted-foreground/50">{word.context_sentence}</p>
        )}
      </div>
      <span className={cn('rounded-full px-2 py-0.5 text-[10px] font-medium', diffColors[word.difficulty] || diffColors.medium)}>
        {word.difficulty}
      </span>
    </button>
  );
}
