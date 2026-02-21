import { motion } from 'framer-motion';
import { type LucideIcon, ArrowUp, ArrowDown } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface AnalyticsStatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  variant?: string;
  trend?: { value: number; positive: boolean };
}

const variants: Record<string, { bg: string; text: string }> = {
  default: { bg: 'bg-muted/50', text: 'text-muted-foreground' },
  primary: { bg: 'bg-primary/10', text: 'text-primary' },
  success: { bg: 'bg-success/10', text: 'text-success' },
  warning: { bg: 'bg-warning/10', text: 'text-warning' },
  accent: { bg: 'bg-accent/10', text: 'text-accent' },
  destructive: { bg: 'bg-destructive/10', text: 'text-destructive' },
};

export default function AnalyticsStatCard({ label, value, icon: Icon, variant = 'default', trend }: AnalyticsStatCardProps) {
  const v = variants[variant] || variants.default;

  return (
    <motion.div variants={staggerItem} className="rounded-xl border border-border/50 p-4 shadow-card transition-shadow hover:shadow-card-hover">
      <div className={cn('flex h-8 w-8 items-center justify-center rounded-lg', v.bg)}>
        <Icon className={cn('h-4 w-4', v.text)} />
      </div>
      <p className="mt-2 font-heading text-xl font-bold">{value}</p>
      <p className="mt-0.5 text-[10px] font-medium uppercase tracking-wide text-muted-foreground/60">{label}</p>
      {trend && (
        <span className={cn('mt-1 flex items-center gap-0.5 text-[10px]', trend.positive ? 'text-success' : 'text-destructive')}>
          {trend.positive ? <ArrowUp className="h-2.5 w-2.5" /> : <ArrowDown className="h-2.5 w-2.5" />}
          {trend.value}%
        </span>
      )}
    </motion.div>
  );
}
