import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { reasonConfig, sectionVariants } from './learningProfileHelpers';

// ─── Props ─────────────────────────────────────────────────────────────────────

interface Recommendation {
  id: string;
  word: string;
  translation: string;
  reason: string;
  reason_type: string;
}

interface LearningRecommendationsProps {
  recommendations: Recommendation[];
  isLoading: boolean;
  onAccept: (id: string) => void;
  acceptIsPending: boolean;
}

// ─── Component ─────────────────────────────────────────────────────────────────

export function LearningRecommendations({
  recommendations,
  isLoading,
  onAccept,
  acceptIsPending,
}: LearningRecommendationsProps) {
  return (
    <motion.div variants={sectionVariants}>
      <Card className="border-border/50">
        <CardHeader>
          <CardTitle className="text-xl">📝 Sizga tavsiya qilingan so&apos;zlar</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : recommendations.length === 0 ? (
            <p className="py-6 text-center text-muted-foreground">
              Hozircha tavsiyalar yo&apos;q. Profilni tahlil qiling!
            </p>
          ) : (
            <div className="space-y-3">
              {recommendations.map((rec) => {
                const cfg = reasonConfig[rec.reason_type] ?? reasonConfig.level_appropriate;
                return (
                  <motion.div
                    key={rec.id}
                    layout
                    exit={{ opacity: 0, x: 100 }}
                    transition={{ duration: 0.3 }}
                    className="flex items-center gap-4 rounded-lg border border-border/50 p-4"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-heading text-lg font-semibold">{rec.word}</p>
                        <span
                          className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${cfg.bgColor} ${cfg.color}`}
                        >
                          {cfg.label}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">{rec.translation}</p>
                      <p className="mt-0.5 text-xs text-muted-foreground">{rec.reason}</p>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => onAccept(rec.id)}
                      disabled={acceptIsPending}
                      className="shrink-0 gap-1"
                    >
                      <Plus className="h-4 w-4" />
                      Qo&apos;shish
                    </Button>
                  </motion.div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
