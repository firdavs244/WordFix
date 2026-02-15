import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface DomainBarProps {
  domain: { key: string; total: number; coverage: number; mastered: number };
  color: string;
}

export default function DomainBar({ domain, color }: DomainBarProps) {
  const coveragePct = Math.round(domain.coverage * 100);
  const masteredPct = domain.total > 0 ? Math.round((domain.mastered / domain.total) * 100) : 0;
  const name = domain.key.replace(/_/g, ' ');

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={cn('h-1.5 w-1.5 rounded-full', color)} />
          <span className="text-xs font-medium capitalize">{name}</span>
        </div>
        <span className="text-[10px] font-medium text-muted-foreground">{coveragePct}%</span>
      </div>
      <div className="relative h-2 overflow-hidden rounded-full bg-muted">
        <motion.div
          className={cn('absolute inset-y-0 left-0 rounded-full opacity-40', color)}
          initial={{ width: 0 }}
          animate={{ width: `${coveragePct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.1 }}
        />
        <motion.div
          className={cn('absolute inset-y-0 left-0 z-10 rounded-full', color)}
          initial={{ width: 0 }}
          animate={{ width: `${masteredPct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.2 }}
        />
      </div>
    </div>
  );
}
