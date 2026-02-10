import { AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { DifficultWord } from '@/types';

// ─── Difficult Words List ──────────────────────────────────────────────────────

export function DifficultWordsList({ words }: { words: DifficultWord[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <AlertTriangle className="h-4 w-4 text-yellow-500" />
          Most Difficult Words
        </CardTitle>
      </CardHeader>
      <CardContent>
        {words.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">
            No difficult words yet. Keep studying!
          </p>
        ) : (
          <div className="space-y-3">
            {words.slice(0, 10).map((word) => (
              <div key={word.id} className="flex items-center justify-between">
                <div>
                  <span className="font-medium text-foreground">{word.original_word}</span>
                  <span className="ml-2 text-sm text-muted-foreground">{word.translation}</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-24">
                    <Progress value={word.accuracy_rate} className="h-2" />
                  </div>
                  <span className="w-12 text-right text-sm font-medium text-foreground">
                    {word.accuracy_rate.toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
