import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { DailyStatsEntry } from '@/types';

// ─── Weekly Chart ──────────────────────────────────────────────────────────────

export function WeeklyChart({ data }: { data: DailyStatsEntry[] }) {
  const maxReviewed = Math.max(...data.map((d) => d.words_reviewed), 1);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <TrendingUp className="h-4 w-4 text-primary" />
          This Week
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-end justify-between gap-2" style={{ height: 120 }}>
          {data.map((day) => {
            const height = (day.words_reviewed / maxReviewed) * 100;
            const dayName = new Date(day.date).toLocaleDateString('en', { weekday: 'short' });
            return (
              <div key={day.date} className="flex flex-1 flex-col items-center gap-1">
                <span className="text-xs font-medium text-foreground">{day.words_reviewed}</span>
                <motion.div
                  className="w-full rounded-t bg-primary/80"
                  initial={{ height: 0 }}
                  animate={{ height: `${Math.max(height, 4)}%` }}
                  transition={{ duration: 0.5, ease: 'easeOut' }}
                />
                <span className="text-xs text-muted-foreground">{dayName}</span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
