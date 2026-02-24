import { Check, Library, Wrench, Bot, CheckCircle } from 'lucide-react';
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
  A1: 'bg-sky-100 text-sky-600 dark:bg-sky-900/30 dark:text-sky-400',
  A2: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
  B1: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400',
  B2: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400',
  C1: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
  C2: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
};

const posColors: Record<string, string> = {
  noun: 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400',
  verb: 'bg-rose-100 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400',
  adjective: 'bg-teal-100 text-teal-600 dark:bg-teal-900/30 dark:text-teal-400',
  adverb: 'bg-cyan-100 text-cyan-600 dark:bg-cyan-900/30 dark:text-cyan-400',
  phrase: 'bg-violet-100 text-violet-600 dark:bg-violet-900/30 dark:text-violet-400',
  idiom: 'bg-pink-100 text-pink-600 dark:bg-pink-900/30 dark:text-pink-400',
};

export default function TextImportWordRow({ word, isSelected, onToggle }: TextImportWordRowProps) {
  const exampleSentence = word.example_sentence || word.context_sentence;
  return (
    <button
      onClick={onToggle}
      className={cn(
        'flex w-full items-center gap-3 px-5 py-3 text-left transition-colors hover:bg-muted/20',
        isSelected && 'bg-primary/[0.03]',
        word.in_user_library && 'opacity-60',
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
        <div className="flex items-center gap-2">
          <span className="font-heading text-sm font-semibold">{word.word}</span>
          {word.pronunciation && (
            <span className="text-[10px] text-muted-foreground/60">{word.pronunciation}</span>
          )}
          {word.part_of_speech && (
            <span className={cn('rounded-full px-1.5 py-0.5 text-[9px] font-medium', posColors[word.part_of_speech.toLowerCase()] || 'bg-muted text-muted-foreground')}>
              {word.part_of_speech}
            </span>
          )}
          {word.in_user_library && (
            <span className="flex items-center gap-0.5 rounded-full bg-amber-100 px-1.5 py-0.5 text-[9px] font-medium text-amber-600 dark:bg-amber-900/30 dark:text-amber-400">
              <Library className="h-2.5 w-2.5" />
              In library
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {word.translation ? (
            <span className={cn(
              'text-xs text-muted-foreground',
              word.translation_source === 'corrected' && 'text-emerald-600 dark:text-emerald-400 font-medium',
            )}>
              {word.translation}
            </span>
          ) : (
            <span className="text-xs text-muted-foreground/40">No translation</span>
          )}
          {word.translation_source === 'corrected' && (
            <span
              className="flex items-center gap-0.5 text-[9px] text-emerald-600 dark:text-emerald-400"
              title={`AI tuzatdi. Asl tarjima: ${word.original_user_translation || '?'}`}
            >
              <Wrench className="h-2.5 w-2.5" />
            </span>
          )}
          {word.translation_source === 'user' && (
            <span
              className="flex items-center gap-0.5 text-[9px] text-blue-500 dark:text-blue-400"
              title="Foydalanuvchi tarjimasi saqlandi"
            >
              <CheckCircle className="h-2.5 w-2.5" />
            </span>
          )}
          {word.translation_source === 'ai' && (
            <span
              className="flex items-center gap-0.5 text-[9px] text-violet-500 dark:text-violet-400"
              title="AI tarjima qildi"
            >
              <Bot className="h-2.5 w-2.5" />
            </span>
          )}
          {word.definition && (
            <span className="text-[10px] text-muted-foreground/50">— {word.definition}</span>
          )}
        </div>
        {exampleSentence && (
          <p className="mt-0.5 line-clamp-1 text-[10px] italic text-muted-foreground/50">{exampleSentence}</p>
        )}
      </div>
      <span className={cn('rounded-full px-2 py-0.5 text-[10px] font-medium', diffColors[word.difficulty] || diffColors.medium)}>
        {word.difficulty}
      </span>
    </button>
  );
}
