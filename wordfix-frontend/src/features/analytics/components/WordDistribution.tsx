import { BarChart3 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// ─── Word Distribution ─────────────────────────────────────────────────────────

export function WordDistribution({ byConfidence, byDifficulty }: {
  byConfidence: Record<string, number>;
  byDifficulty: Record<string, number>;
}) {
  const confidenceLabels: Record<string, string> = {
    mastered: 'Mastered',
    confident: 'Confident',
    learning: 'Learning',
    new: 'New',
  };

  const difficultyColors: Record<string, string> = {
    easy: 'bg-green-500',
    medium: 'bg-yellow-500',
    hard: 'bg-red-500',
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <BarChart3 className="h-4 w-4 text-primary" />
          Word Distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* By confidence */}
        <div>
          <h4 className="mb-2 text-sm font-medium text-muted-foreground">By Confidence</h4>
          <div className="space-y-2">
            {Object.entries(byConfidence).map(([key, count]) => (
              <div key={key} className="flex items-center gap-2">
                <span className="w-20 text-sm text-muted-foreground">
                  {confidenceLabels[key] || key}
                </span>
                <div className="flex-1">
                  <div
                    className="h-4 rounded bg-primary/70 transition-all"
                    style={{
                      width: `${Math.max(
                        (count / Math.max(Object.values(byConfidence).reduce((a, b) => a + b, 0), 1)) * 100,
                        2
                      )}%`,
                    }}
                  />
                </div>
                <span className="w-8 text-right text-sm font-medium">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* By difficulty */}
        <div>
          <h4 className="mb-2 text-sm font-medium text-muted-foreground">By Difficulty</h4>
          <div className="flex gap-4">
            {Object.entries(byDifficulty).map(([key, count]) => (
              <div key={key} className="flex items-center gap-2">
                <div className={`h-3 w-3 rounded-full ${difficultyColors[key] || 'bg-muted'}`} />
                <span className="text-sm capitalize text-muted-foreground">{key}</span>
                <span className="font-medium">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
