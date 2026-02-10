import { motion } from 'framer-motion';
import { AlertTriangle, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { ConfusingPair } from '../types';

interface ConfusingPairCardProps {
  pair: ConfusingPair;
  onDrill: (id: string) => void;
  onResolve: (id: string) => void;
}

export function ConfusingPairCard({ pair, onDrill, onResolve }: ConfusingPairCardProps) {
  const isResolved = pair.is_resolved;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={!isResolved ? { scale: 1.01 } : undefined}
      transition={{ duration: 0.3 }}
    >
      <Card
        className={cn(
          'border-border/50 transition-shadow',
          isResolved ? 'opacity-60' : 'hover:shadow-md',
        )}
      >
        <CardContent className="p-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            {/* Word 1 */}
            <div className="flex-1 text-center sm:text-right">
              <p className="font-heading text-lg font-bold">{pair.word_1.original_word}</p>
              <p className="text-sm text-muted-foreground">{pair.word_1.translation}</p>
            </div>

            {/* Separator */}
            <div className="flex items-center justify-center">
              <motion.div
                animate={!isResolved ? { rotate: [0, 10, -10, 0] } : undefined}
                transition={{ repeat: Infinity, duration: 3 }}
              >
                {isResolved ? (
                  <span className="text-xl">✅</span>
                ) : (
                  <Zap className="h-6 w-6 text-amber-500" />
                )}
              </motion.div>
            </div>

            {/* Word 2 */}
            <div className="flex-1 text-center sm:text-left">
              <p className="font-heading text-lg font-bold">{pair.word_2.original_word}</p>
              <p className="text-sm text-muted-foreground">{pair.word_2.translation}</p>
            </div>
          </div>

          {/* Bottom info */}
          <div className="mt-4 flex flex-col items-center justify-between gap-3 sm:flex-row">
            <div className="flex items-center gap-2">
              {isResolved ? (
                <Badge variant="outline" className="bg-green-500/10 text-green-600 dark:text-green-400">
                  ✅ Resolved
                </Badge>
              ) : (
                <Badge
                  variant={pair.confusion_count >= 5 ? 'destructive' : 'outline'}
                  className="flex items-center gap-1"
                >
                  <AlertTriangle className="h-3 w-3" />
                  Confused {pair.confusion_count} time{pair.confusion_count !== 1 ? 's' : ''}
                </Badge>
              )}
            </div>

            {!isResolved && (
              <div className="flex gap-2">
                <Button
                  variant="default"
                  size="sm"
                  onClick={() => onDrill(pair.id)}
                  className="gap-1.5"
                >
                  🧠 Practice Drill
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onResolve(pair.id)}
                  className="gap-1.5"
                >
                  Mark Resolved ✓
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
