import { motion } from 'framer-motion';
import { staggerContainer } from '@/lib/motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertTriangle } from 'lucide-react';
import EmptyState from '@/components/shared/EmptyState';
import { LearningMistakeItem } from './LearningMistakeItem';
import type { MistakePattern } from '@/types/learning';

interface Props {
  mistakes: MistakePattern[];
  isLoading: boolean;
}

export function LearningMistakes({ mistakes, isLoading }: Props) {
  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <AlertTriangle className="h-5 w-5 text-muted-foreground" />
          Mistake Patterns
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-20 w-full" />
            ))}
          </div>
        ) : mistakes.length === 0 ? (
          <EmptyState
            icon={AlertTriangle}
            title="No mistake patterns"
            description="Keep learning to build your mistake analysis"
          />
        ) : (
          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            className="space-y-2"
          >
            {mistakes.map((m) => (
              <LearningMistakeItem key={m.id} mistake={m} />
            ))}
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
}
