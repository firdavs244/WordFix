import { cn } from '@/lib/utils';

interface Props {
  total: number;
  remaining: number;
}

export default function AttemptIndicator({ total, remaining }: Props) {
  return (
    <div className="flex items-center gap-1.5" data-testid="attempt-indicator">
      {Array.from({ length: total }, (_, i) => (
        <div
          key={i}
          className={cn(
            'h-2.5 w-2.5 rounded-full transition-all',
            i < remaining ? 'bg-primary shadow-sm' : 'bg-muted',
          )}
        />
      ))}
      <span className="ml-1 text-xs text-muted-foreground">{remaining} left</span>
    </div>
  );
}
