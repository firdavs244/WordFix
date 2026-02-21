import { motion } from 'framer-motion';
import { staggerContainer } from '@/lib/motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Lightbulb } from 'lucide-react';
import EmptyState from '@/components/shared/EmptyState';
import { LearningRecommendationItem } from './LearningRecommendationItem';
import type { WordRecommendation } from '@/types/learning';

interface Props {
  recommendations: WordRecommendation[];
  isLoading: boolean;
  onAccept: (id: string) => void;
  isPending: boolean;
}

export function LearningRecommendations({
  recommendations,
  isLoading,
  onAccept,
  isPending,
}: Props) {
  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Lightbulb className="h-5 w-5 text-muted-foreground" />
          Word Recommendations
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-16 w-full" />
            ))}
          </div>
        ) : recommendations.length === 0 ? (
          <EmptyState
            icon={Lightbulb}
            title="No recommendations"
            description="Analyze your profile for personalized word recommendations"
          />
        ) : (
          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            className="space-y-2"
          >
            {recommendations.map((r) => (
              <LearningRecommendationItem
                key={r.id}
                recommendation={r}
                onAccept={onAccept}
                isPending={isPending}
              />
            ))}
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
}
