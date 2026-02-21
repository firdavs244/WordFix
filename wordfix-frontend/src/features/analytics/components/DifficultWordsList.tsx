import { AlertCircle } from 'lucide-react';
import DifficultWordItem from './DifficultWordItem';
import type { DifficultWord } from '@/types';

interface DifficultWordsListProps {
  words: DifficultWord[];
}

export default function DifficultWordsList({ words }: DifficultWordsListProps) {
  if (words.length === 0) return null;

  return (
    <div className="rounded-2xl border border-border/50 p-5 shadow-card">
      <div className="flex items-center gap-2">
        <AlertCircle className="h-4 w-4 text-destructive/70" />
        <span className="font-heading text-sm font-semibold">Needs Attention</span>
        <span className="rounded-full bg-destructive/10 px-2 py-0.5 text-[10px] font-medium text-destructive">
          {words.length}
        </span>
      </div>
      <div className="mt-4 space-y-2">
        {words.slice(0, 10).map((w, i) => (
          <DifficultWordItem key={w.id} word={w} rank={i} />
        ))}
      </div>
    </div>
  );
}
