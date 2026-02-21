import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import { PageTransition } from '@/components/animations/PageTransition';
import { listContainerVariants, listItemVariants } from '@/components/animations/PageTransition';
import { ConfusingPairCard } from '../components/ConfusingPairCard';
import { DrillModal } from '../components/DrillModal';
import ResolvedPairsSection from '../components/ResolvedPairsSection';
import { useConfusingPairs, useResolvePair } from '../hooks/useConfusingPairs';

export function ConfusingPairsPage() {
  const { data, isLoading } = useConfusingPairs();
  const resolvePair = useResolvePair();
  const [drillPairId, setDrillPairId] = useState<string | null>(null);

  const pairs = data?.data ?? [];

  const { unresolved, resolved } = useMemo(() => {
    const u = pairs
      .filter((p) => !p.is_resolved)
      .sort((a, b) => b.confusion_count - a.confusion_count);
    const r = pairs.filter((p) => p.is_resolved);
    return { unresolved: u, resolved: r };
  }, [pairs]);

  const handleDrill = (id: string) => setDrillPairId(id);
  const handleResolve = (id: string) => resolvePair.mutate(id);

  if (isLoading) {
    return (
      <PageTransition>
        <div className="mx-auto max-w-3xl space-y-6">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-32 w-full" />
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="mx-auto max-w-3xl space-y-6">
        {/* Header */}
        <motion.div
          className="flex items-center justify-between"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
            </div>
            <div>
              <h1 className="font-heading text-2xl font-bold">Confusing Pairs</h1>
              <p className="text-sm text-muted-foreground">
                {unresolved.length > 0
                  ? `${unresolved.length} pair${unresolved.length !== 1 ? 's' : ''} to practice`
                  : 'All pairs resolved!'}
              </p>
            </div>
          </div>
          {unresolved.length > 0 && (
            <span className="rounded-full bg-amber-500/10 px-3 py-1 text-sm font-medium text-amber-600 dark:text-amber-400">
              {unresolved.length} pair{unresolved.length !== 1 ? 's' : ''}
            </span>
          )}
        </motion.div>

        {/* Description */}
        <p className="text-muted-foreground">
          These are words you often mix up. Practice drills to master the difference.
        </p>

        {/* Empty state */}
        {pairs.length === 0 && (
          <motion.div
            className="flex flex-col items-center gap-4 py-16 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-green-500/10">
              <CheckCircle2 className="h-8 w-8 text-green-500" />
            </div>
            <h2 className="font-heading text-xl font-bold">No confusing pairs yet! 🎉</h2>
            <p className="max-w-md text-muted-foreground">
              Keep practicing — we&apos;ll track any words you mix up.
            </p>
          </motion.div>
        )}

        {/* Unresolved pairs */}
        {unresolved.length > 0 && (
          <motion.div
            className="space-y-3"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {unresolved.map((pair) => (
              <motion.div key={pair.id} variants={listItemVariants}>
                <ConfusingPairCard
                  pair={pair}
                  onDrill={handleDrill}
                  onResolve={handleResolve}
                />
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Resolved pairs */}
        <ResolvedPairsSection pairs={resolved} onDrill={handleDrill} onResolve={handleResolve} />

        {/* Drill Modal */}
        <DrillModal
          pairId={drillPairId ?? ''}
          isOpen={!!drillPairId}
          onClose={() => setDrillPairId(null)}
        />
      </div>
    </PageTransition>
  );
}
