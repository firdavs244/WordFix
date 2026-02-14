import { motion } from 'framer-motion';
import { CheckCircle2, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { patternConfig, sectionVariants } from './learningProfileHelpers';

// ─── Props ─────────────────────────────────────────────────────────────────────

interface MistakePattern {
  id: string;
  type: string;
  description: string;
  occurrence_count: number;
  is_resolved: boolean;
  examples: { wrong: string; correct: string }[];
}

interface LearningMistakesProps {
  mistakes: MistakePattern[];
  isLoading: boolean;
}

// ─── Component ─────────────────────────────────────────────────────────────────

export function LearningMistakes({ mistakes, isLoading }: LearningMistakesProps) {
  return (
    <motion.div variants={sectionVariants}>
      <Card className="border-border/50">
        <CardHeader>
          <CardTitle className="text-xl">⚠️ Takroriy xatolaringiz</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full" />
              ))}
            </div>
          ) : mistakes.length === 0 ? (
            <p className="py-6 text-center text-muted-foreground">
              Hozircha pattern topilmadi. Test va review davom eting!
            </p>
          ) : (
            <div className="space-y-4">
              {mistakes.map((pattern) => {
                const cfg = patternConfig[pattern.type] ?? patternConfig.spelling;
                return (
                  <motion.div
                    key={pattern.id}
                    layout
                    className="rounded-lg border border-border/50 p-4"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span
                            className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${cfg.bgColor} ${cfg.color}`}
                          >
                            {cfg.label}
                          </span>
                          <Badge variant="outline" className="text-xs">
                            {pattern.occurrence_count} marta
                          </Badge>
                          {pattern.is_resolved && (
                            <Badge
                              variant="outline"
                              className="border-green-300 bg-green-50 text-green-700 dark:border-green-800 dark:bg-green-950 dark:text-green-300"
                            >
                              <CheckCircle2 className="mr-1 h-3 w-3" />
                              Hal qilingan
                            </Badge>
                          )}
                        </div>
                        <p className="mt-2 text-sm">{pattern.description}</p>
                      </div>
                      <AlertTriangle
                        className={`h-5 w-5 shrink-0 ${pattern.is_resolved ? 'text-green-500' : 'text-yellow-500'}`}
                      />
                    </div>

                    {/* Example */}
                    {pattern.examples.length > 0 && (
                      <div className="mt-3 rounded-md bg-muted/50 p-3 text-sm">
                        <span className="text-red-500 line-through">
                          {pattern.examples[0].wrong}
                        </span>
                        <span className="mx-2">→</span>
                        <span className="font-medium text-green-600 dark:text-green-400">
                          {pattern.examples[0].correct}
                        </span>
                      </div>
                    )}
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
