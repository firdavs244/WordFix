import { cn } from '@/lib/utils';
import { LevelBadgeGlow } from './LevelBadgeGlow';

interface Props {
  level: string;
  size?: 'sm' | 'md' | 'lg';
}

const dims = { sm: 'h-11 w-11', md: 'h-16 w-16', lg: 'h-[88px] w-[88px]' };
const text = { sm: 'text-sm', md: 'text-xl', lg: 'text-3xl' };

export function LevelBadge({ level, size = 'md' }: Props) {
  return (
    <div className="relative inline-flex items-center justify-center">
      <LevelBadgeGlow size={size} />
      <div
        className={cn(
          'relative z-10 flex items-center justify-center rounded-full border-2 border-primary bg-gradient-to-br from-primary/20 via-primary/10 to-secondary/20 shadow-glow-primary ring-4 ring-primary/10',
          dims[size],
        )}
      >
        <span className={cn('font-heading font-bold text-primary', text[size])}>{level}</span>
      </div>
    </div>
  );
}
