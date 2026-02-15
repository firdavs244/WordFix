import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface GlowingBorderProps {
  children: ReactNode;
  className?: string;
  active?: boolean;
  color?: 'primary' | 'success' | 'accent' | 'rainbow';
}

const gradients: Record<string, string> = {
  primary: 'from-primary/60 via-primary/20 via-transparent to-primary/60',
  success: 'from-success/60 via-success/20 via-transparent to-success/60',
  accent: 'from-accent/60 via-amber-400/20 via-transparent to-accent/60',
  rainbow: 'from-primary via-secondary via-accent via-success to-primary',
};

export default function GlowingBorder({
  children,
  className,
  active = false,
  color = 'primary',
}: GlowingBorderProps) {
  if (!active) {
    return <div className={cn('rounded-2xl border border-border/50', className)}>{children}</div>;
  }

  return (
    <div className={cn('relative rounded-2xl p-[1px]', className)}>
      <div
        className={cn(
          'absolute inset-0 rounded-2xl bg-conic-gradient opacity-80',
          'animate-[spin_4s_linear_infinite]',
          `bg-gradient-to-r ${gradients[color]}`,
        )}
      />
      <div
        className={cn(
          'absolute inset-0 rounded-2xl blur-xl opacity-30',
          `bg-gradient-to-r ${gradients[color]}`,
        )}
      />
      <div className="relative rounded-2xl bg-card">{children}</div>
    </div>
  );
}
