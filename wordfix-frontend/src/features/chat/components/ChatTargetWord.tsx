import { CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatTargetWordProps {
  word: string;
  isUsed: boolean;
}

export default function ChatTargetWord({ word, isUsed }: ChatTargetWordProps) {
  return (
    <span
      className={cn(
        'inline-flex shrink-0 items-center gap-1 rounded-full px-2.5 py-1 text-[11px] font-medium transition-all duration-300',
        isUsed
          ? 'border border-success/20 bg-success/10 text-success line-through opacity-60'
          : 'border border-primary/20 bg-primary/10 text-primary',
      )}
    >
      {isUsed && <CheckCircle2 className="h-2.5 w-2.5" />}
      {word}
    </span>
  );
}
