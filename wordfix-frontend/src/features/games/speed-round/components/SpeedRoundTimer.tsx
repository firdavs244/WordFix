import { cn } from '@/lib/utils';

interface Props {
  remaining: number;
  total: number;
}

export default function SpeedRoundTimer({ remaining, total }: Props) {
  const pct = remaining / total;
  const r = 32;
  const circ = 2 * Math.PI * r;
  const offset = circ - pct * circ;

  const color =
    remaining > 30 ? 'stroke-success text-success'
    : remaining > 15 ? 'stroke-yellow-500 text-yellow-500'
    : 'stroke-destructive text-destructive';

  const pulse = remaining < 10;

  return (
    <div className={cn('relative h-20 w-20', pulse && 'animate-pulse')} data-testid="speed-timer">
      <svg className="-rotate-90" viewBox="0 0 80 80" width="80" height="80">
        <circle cx="40" cy="40" r={r} fill="none" strokeWidth="5" className="stroke-muted" />
        <circle
          cx="40" cy="40" r={r} fill="none" strokeWidth="5"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          className={cn(color, 'transition-all duration-1000')}
        />
      </svg>
      <span className={cn('absolute inset-0 flex items-center justify-center font-heading text-2xl font-bold', color)}>
        {remaining}
      </span>
    </div>
  );
}
