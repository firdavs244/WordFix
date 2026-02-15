import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { Skeleton } from '@/components/ui/skeleton';
import { useMistakePatterns } from '@/features/learning/hooks/useLearning';
import MistakePatternItem from './MistakePatternItem';

export default function MistakePatternsWidget() {
  const { data, isLoading } = useMistakePatterns();
  const patterns = data?.data ?? [];

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 shadow-card">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <Skeleton key={i} className="h-14 rounded-xl" />)}
        </div>
      </div>
    );
  }

  const items = Array.isArray(patterns)
    ? [...patterns].sort((a: any, b: any) => b.occurrence_count - a.occurrence_count).slice(0, 3)
    : [];

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center gap-2 px-5 pt-5">
        <AlertTriangle className="h-[18px] w-[18px] text-warning" />
        <h3 className="text-base font-heading font-semibold">E'tibor bering</h3>
      </div>

      {items.length === 0 ? (
        <p className="px-5 py-8 text-center text-sm text-muted-foreground">
          Xatolar topilmadi
        </p>
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="space-y-1.5 px-5 py-4"
        >
          {items.map((pattern: any) => (
            <MistakePatternItem key={pattern.id} pattern={pattern} />
          ))}
        </motion.div>
      )}
    </div>
  );
}
