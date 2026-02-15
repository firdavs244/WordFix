import { cn } from '@/lib/utils';

interface Props {
  word: string;
  translation: string;
  className?: string;
}

export function FloatingWordCard({ word, translation, className }: Props) {
  return (
    <div className={cn('animate-float rounded-xl border border-border/20 bg-card/60 px-4 py-2.5 opacity-50 shadow-md backdrop-blur-sm dark:opacity-25', className)}>
      <p className="font-heading text-xs font-semibold">{word}</p>
      <p className="text-[10px] text-muted-foreground">{translation}</p>
    </div>
  );
}
