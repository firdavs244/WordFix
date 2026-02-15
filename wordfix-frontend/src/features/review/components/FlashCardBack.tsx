import { Quote, Sparkles } from 'lucide-react';
import type { Word } from '@/types';

interface Props {
  word: Word;
}

export default function FlashCardBack({ word }: Props) {
  return (
    <div
      className="absolute inset-0 flex flex-col gap-4 overflow-y-auto rounded-3xl border border-border/30 bg-card p-6 shadow-xl scrollbar-thin lg:p-8"
      style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
    >
      <h3 className="text-center font-heading text-xl font-bold">{word.translation}</h3>
      <div className="mx-auto h-px w-16 bg-border/30" />

      {word.definition && (
        <p className="text-sm leading-relaxed text-muted-foreground">{word.definition}</p>
      )}

      {word.example_sentence && (
        <div className="rounded-xl border-l-2 border-primary/30 bg-muted/30 p-3">
          <Quote className="mb-1 h-3 w-3 text-primary/30" />
          <p className="text-sm italic">{word.example_sentence}</p>
          {word.example_translation && (
            <p className="mt-1 text-xs text-muted-foreground">{word.example_translation}</p>
          )}
        </div>
      )}

      {word.mnemonic && (
        <div className="rounded-xl border border-accent/10 bg-accent/[0.06] p-3">
          <div className="mb-1 flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-accent" />
            <span className="text-[10px] font-semibold uppercase text-accent">Memory tip</span>
          </div>
          <p className="text-sm">{word.mnemonic}</p>
        </div>
      )}

      {word.synonyms?.length > 0 && (
        <div>
          <span className="text-[10px] uppercase text-muted-foreground/50">Synonyms:</span>
          <div className="mt-1 flex flex-wrap gap-1.5">
            {word.synonyms.map((s) => (
              <span key={s} className="rounded-full border border-success/20 bg-success/10 px-2 py-0.5 text-xs text-success">{s}</span>
            ))}
          </div>
        </div>
      )}

      {word.antonyms?.length > 0 && (
        <div>
          <span className="text-[10px] uppercase text-muted-foreground/50">Antonyms:</span>
          <div className="mt-1 flex flex-wrap gap-1.5">
            {word.antonyms.map((a) => (
              <span key={a} className="rounded-full border border-destructive/20 bg-destructive/10 px-2 py-0.5 text-xs text-destructive">{a}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
