import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useXPHistory } from '../hooks/useProgress';

export function XPChart() {
  const { data, isLoading } = useXPHistory(7);
  const history = data?.data ?? [];

  if (isLoading) {
    return (
      <Card className="border-border/50">
        <CardContent className="p-6">
          <Skeleton className="h-32 w-full" />
        </CardContent>
      </Card>
    );
  }

  const maxXP = Math.max(...history.map((h) => h.xp), 1);

  return (
    <Card className="border-border/50">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">XP This Week</CardTitle>
      </CardHeader>
      <CardContent className="px-6 pb-6">
        <div className="flex items-end justify-between gap-2 h-28">
          {history.map((entry, i) => {
            const height = (entry.xp / maxXP) * 100;
            const day = new Date(entry.date).toLocaleDateString('en', { weekday: 'short' });
            return (
              <div key={entry.date} className="flex flex-1 flex-col items-center gap-1">
                <span className="text-[10px] font-medium text-muted-foreground">
                  {entry.xp > 0 ? entry.xp : ''}
                </span>
                <motion.div
                  className="w-full rounded-t-md bg-primary/80"
                  initial={{ height: 0 }}
                  animate={{ height: `${Math.max(height, 4)}%` }}
                  transition={{ duration: 0.4, delay: i * 0.05 }}
                />
                <span className="text-[10px] text-muted-foreground">{day}</span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
