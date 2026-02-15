import { motion } from 'framer-motion';
import { ArrowDown, ArrowUp, type LucideIcon } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: { value: number; positive: boolean };
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'destructive' | 'accent';
  compact?: boolean;
}

const variantStyles: Record<string, string> = {
  default: 'bg-muted text-muted-foreground',
  primary: 'bg-primary/10 text-primary',
  success: 'bg-success/10 text-success',
  warning: 'bg-warning/10 text-warning',
  destructive: 'bg-destructive/10 text-destructive',
  accent: 'bg-accent/10 text-accent',
};

export default function StatCard({ label, value, icon: Icon, trend, variant = 'default', compact }: StatCardProps) {
  return (
    <motion.div
      variants={staggerItem}
      className="rounded-xl border border-border/50 bg-card p-4 shadow-card transition-shadow hover:shadow-card-hover"
    >
      <div className="flex items-start justify-between">
        <div className={cn('flex h-9 w-9 items-center justify-center rounded-lg', variantStyles[variant])}>
          <Icon className="h-[18px] w-[18px]" />
        </div>
        {trend && (
          <span className={cn('flex items-center gap-0.5 text-xs font-medium', trend.positive ? 'text-success' : 'text-destructive')}>
            {trend.positive ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />}
            {trend.value}%
          </span>
        )}
      </div>
      <p className={cn('mt-3 font-heading font-bold', compact ? 'text-xl' : 'text-2xl')}>{value}</p>
      <p className="mt-0.5 text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</p>
    </motion.div>
  );
}
