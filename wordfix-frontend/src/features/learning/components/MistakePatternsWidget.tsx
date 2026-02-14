import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, PartyPopper } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useMistakePatterns } from '../hooks/useLearning';

// ─── Pattern Config ────────────────────────────────────────────────────────────

const patternBadge: Record<string, { bg: string; text: string; label: string }> = {
  l1_interference: { bg: 'bg-red-100 dark:bg-red-900', text: 'text-red-700 dark:text-red-300', label: 'Ona tili' },
  morphological: { bg: 'bg-orange-100 dark:bg-orange-900', text: 'text-orange-700 dark:text-orange-300', label: 'Shakl' },
  semantic: { bg: 'bg-yellow-100 dark:bg-yellow-900', text: 'text-yellow-700 dark:text-yellow-300', label: 'Ma\'no' },
  spelling: { bg: 'bg-blue-100 dark:bg-blue-900', text: 'text-blue-700 dark:text-blue-300', label: 'Imlo' },
  phonological: { bg: 'bg-violet-100 dark:bg-violet-900', text: 'text-violet-700 dark:text-violet-300', label: 'Talaffuz' },
};

// ─── Component ─────────────────────────────────────────────────────────────────

export function MistakePatternsWidget() {
  const { data, isLoading } = useMistakePatterns();
  const patterns = (data?.data ?? [])
    .filter((p) => !p.is_resolved)
    .sort((a, b) => b.occurrence_count - a.occurrence_count)
    .slice(0, 3);

  return (
    <Card className="border-border/50">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2 text-lg">
          ⚠️ E&apos;tibor bering
        </CardTitle>
        <Link to="/learning-profile">
          <Button variant="ghost" size="sm" className="gap-1 text-primary">
            Batafsil
            <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-12 w-full" />
            ))}
          </div>
        ) : patterns.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-4 text-center">
            <PartyPopper className="h-8 w-8 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">
              Ajoyib! Takroriy xatolar topilmadi 🎉
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {patterns.map((pattern, i) => {
              const cfg = patternBadge[pattern.type] ?? patternBadge.spelling;
              return (
                <motion.div
                  key={pattern.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: i * 0.05 }}
                  className="flex items-center gap-3 rounded-lg border border-border/50 px-3 py-2"
                >
                  <span className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium ${cfg.bg} ${cfg.text}`}>
                    {cfg.label}
                  </span>
                  <p className="flex-1 min-w-0 text-sm truncate">{pattern.description}</p>
                  <Badge variant="outline" className="shrink-0 text-xs">
                    {pattern.occurrence_count} marta
                  </Badge>
                </motion.div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
