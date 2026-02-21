import ChatTargetWord from './ChatTargetWord';
import { cn } from '@/lib/utils';

interface ChatTargetWordsBarProps {
  words: string[];
  usedWords: string[];
}

export default function ChatTargetWordsBar({ words, usedWords }: ChatTargetWordsBarProps) {
  if (!words.length) return null;

  const usedSet = new Set(usedWords.map((w) => w.toLowerCase()));
  const usedCount = words.filter((w) => usedSet.has(w.toLowerCase())).length;
  const allUsed = usedCount === words.length;

  return (
    <div className="sticky top-14 z-20 flex items-center gap-2 overflow-x-auto border-b border-border/10 bg-background/60 px-4 py-2 backdrop-blur-md scrollbar-none">
      <span className="shrink-0 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground/40">
        Use these words:
      </span>
      <div className="flex gap-1.5">
        {words.map((w) => (
          <ChatTargetWord key={w} word={w} isUsed={usedSet.has(w.toLowerCase())} />
        ))}
      </div>
      <span className={cn('ml-auto shrink-0 text-[10px] font-medium', allUsed ? 'text-success' : 'text-muted-foreground')}>
        {usedCount}/{words.length}
      </span>
    </div>
  );
}
