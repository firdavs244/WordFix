import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Plus, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useWordRecommendations, useAcceptRecommendation } from '../hooks/useLearning';

// ─── Reason Config ─────────────────────────────────────────────────────────────

const reasonBadge: Record<string, { bg: string; text: string }> = {
  domain_gap: { bg: 'bg-green-100 dark:bg-green-900', text: 'text-green-700 dark:text-green-300' },
  confusion_fix: { bg: 'bg-yellow-100 dark:bg-yellow-900', text: 'text-yellow-700 dark:text-yellow-300' },
  level_appropriate: { bg: 'bg-blue-100 dark:bg-blue-900', text: 'text-blue-700 dark:text-blue-300' },
  high_frequency: { bg: 'bg-violet-100 dark:bg-violet-900', text: 'text-violet-700 dark:text-violet-300' },
};

// ─── Component ─────────────────────────────────────────────────────────────────

export function RecommendationsWidget() {
  const { data, isLoading } = useWordRecommendations();
  const acceptRec = useAcceptRecommendation();
  const recommendations = (data?.data ?? []).slice(0, 3);

  return (
    <Card className="border-border/50">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2 text-lg">
          💡 Tavsiya qilingan so&apos;zlar
        </CardTitle>
        <Link to="/learning-profile">
          <Button variant="ghost" size="sm" className="gap-1 text-primary">
            Barchasini ko&apos;rish
            <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-14 w-full" />
            ))}
          </div>
        ) : recommendations.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-4 text-center">
            <Sparkles className="h-8 w-8 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">
              Profilni tahlil qiling — AI so&apos;z tavsiya qiladi
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {recommendations.map((rec, i) => {
              const badge = reasonBadge[rec.reason_type] ?? reasonBadge.level_appropriate;
              return (
                <motion.div
                  key={rec.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: i * 0.05 }}
                  className="flex items-center gap-3 rounded-lg border border-border/50 px-3 py-2"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium truncate">{rec.word}</span>
                      <span className={`shrink-0 rounded-full px-1.5 py-0.5 text-[10px] font-medium ${badge.bg} ${badge.text}`}>
                        {rec.reason_type === 'domain_gap' ? 'Soha' :
                         rec.reason_type === 'confusion_fix' ? 'Tuzatish' :
                         rec.reason_type === 'high_frequency' ? 'Tez-tez' : 'Daraja'}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground truncate">{rec.translation}</p>
                  </div>
                  <Button
                    size="icon"
                    variant="ghost"
                    className="h-8 w-8 shrink-0"
                    onClick={() => acceptRec.mutate(rec.id)}
                    disabled={acceptRec.isPending}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </motion.div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
