import { cn } from '@/lib/utils';

interface Props {
  size?: 'sm' | 'md' | 'lg';
}

const dims = { sm: 'h-16 w-16', md: 'h-[84px] w-[84px]', lg: 'h-[108px] w-[108px]' };

export function LevelBadgeGlow({ size = 'md' }: Props) {
  return (
    <div
      className={cn(
        'absolute rounded-full bg-primary/10 opacity-50 blur-[20px]',
        dims[size],
      )}
      style={{ animation: 'pulse 3s ease-in-out infinite' }}
    />
  );
}
