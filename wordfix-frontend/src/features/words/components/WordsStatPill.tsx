import type { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface WordsStatPillProps {
  label: string;
  value: number;
  color: string;
  icon: LucideIcon;
}

const colorMap: Record<string, { bg: string; text: string }> = {
  primary: { bg: 'bg-primary/10', text: 'text-primary' },
  success: { bg: 'bg-success/10', text: 'text-success' },
  warning: { bg: 'bg-warning/10', text: 'text-warning' },
  secondary: { bg: 'bg-secondary/10', text: 'text-secondary' },
};

export default function WordsStatPill({ label, value, color, icon: Icon }: WordsStatPillProps) {
  const colors = colorMap[color] ?? colorMap.primary;
  return (
    <div className="inline-flex shrink-0 items-center gap-2 rounded-xl border border-border/50 bg-card px-4 py-2.5 shadow-sm transition-shadow hover:shadow-card">
      <div className={cn('flex h-6 w-6 items-center justify-center rounded-md', colors.bg)}>
        <Icon className={cn('h-3.5 w-3.5', colors.text)} />
      </div>
      <div>
        <p className="font-heading text-sm font-bold">{value}</p>
        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">{label}</p>
      </div>
    </div>
  );
}
