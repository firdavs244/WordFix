import { motion } from 'framer-motion';
import { Plus, Loader2 } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';
import { useAcceptRecommendation } from '@/features/learning-profile/hooks/useLearning';
import type { WordRecommendation } from '@/types';

const REASON_STYLES: Record<string, { label: string; className: string }> = {
  domain_gap: { label: 'Soha', className: 'bg-blue-500/10 text-blue-500 border-blue-500/20' },
  confusion_fix: { label: 'Tuzatish', className: 'bg-orange-500/10 text-orange-500 border-orange-500/20' },
  high_frequency: { label: 'Tez-tez', className: 'bg-green-500/10 text-green-500 border-green-500/20' },
  level_appropriate: { label: 'Daraja', className: 'bg-violet-500/10 text-violet-500 border-violet-500/20' },
};

export default function RecommendationItem({ recommendation }: { recommendation: WordRecommendation }) {
  const accept = useAcceptRecommendation();
  const reason = REASON_STYLES[recommendation.reason_type] ?? REASON_STYLES.domain_gap;

  return (
    <motion.div
      variants={staggerItem}
      className="flex items-center gap-3 rounded-xl p-3 transition-colors hover:bg-muted/20"
    >
      <div className="flex-1 min-w-0">
        <p className="text-sm font-heading font-semibold truncate">{recommendation.word}</p>
        <p className="text-xs text-muted-foreground truncate">{recommendation.translation}</p>
      </div>
      <span className={cn('shrink-0 rounded-full border px-2 py-0.5 text-[10px]', reason.className)}>
        {reason.label}
      </span>
      <button
        onClick={() => accept.mutate(recommendation.id)}
        disabled={accept.isPending}
        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-primary/10 transition-colors hover:bg-primary/20 disabled:opacity-50"
      >
        {accept.isPending ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin text-primary" />
        ) : (
          <Plus className="h-3.5 w-3.5 text-primary" />
        )}
      </button>
    </motion.div>
  );
}
