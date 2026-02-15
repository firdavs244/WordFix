import { cn } from '@/lib/utils';

interface Props {
  text: string;
  targetWords: string[];
}

export default function StoryDisplay({ text, targetWords }: Props) {
  if (!text) return null;

  const regex = new RegExp(`\\b(${targetWords.join('|')})\\b`, 'gi');
  const parts = text.split(regex);

  return (
    <div className="rounded-xl border border-border/50 bg-muted/20 p-5" data-testid="story-display">
      <p className="text-sm leading-relaxed">
        {parts.map((part, i) => (
          <span
            key={i}
            className={cn(
              targetWords.some((w) => w.toLowerCase() === part.toLowerCase()) &&
              'rounded bg-primary/15 px-1 py-0.5 font-semibold text-primary',
            )}
          >
            {part}
          </span>
        ))}
      </p>
    </div>
  );
}
