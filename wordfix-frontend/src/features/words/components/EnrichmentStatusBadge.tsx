import { Sparkles, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { EnrichmentStatus } from '@/types';

const config: Record<EnrichmentStatus, { icon: typeof Sparkles; label: string; className: string }> = {
  pending: { icon: Loader2, label: 'Pending...', className: 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950 dark:text-blue-400 dark:border-blue-800' },
  processing: { icon: Loader2, label: 'Enriching...', className: 'bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-950 dark:text-blue-400 dark:border-blue-800' },
  enriched: { icon: CheckCircle, label: 'Enriched', className: 'bg-success/10 text-success border-success/20' },
  failed: { icon: AlertCircle, label: 'Failed', className: 'bg-destructive/10 text-destructive border-destructive/20' },
};

const defaultConfig = { icon: Sparkles, label: 'Not enriched', className: 'bg-muted text-muted-foreground border-border/30' };

interface EnrichmentStatusBadgeProps {
  status: EnrichmentStatus;
  className?: string;
  showLabel?: boolean;
}

export function EnrichmentStatusBadge({ status, className, showLabel = true }: EnrichmentStatusBadgeProps) {
  const cfg = config[status] || defaultConfig;
  const Icon = cfg.icon;
  const isAnimating = status === 'pending' || status === 'processing';

  return (
    <span className={cn(
      'inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] font-medium',
      cfg.className,
      className,
    )}>
      <Icon className={cn('h-3 w-3', isAnimating && 'animate-spin')} />
      {showLabel && cfg.label}
    </span>
  );
}
