import { TrendingUp } from 'lucide-react';
import WeeklyChartBar from './WeeklyChartBar';
import type { DailyStatsEntry } from '@/types';

interface WeeklyChartProps {
  data: DailyStatsEntry[];
}

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export default function WeeklyChart({ data }: WeeklyChartProps) {
  const total = data.reduce((s, d) => s + d.words_reviewed, 0);
  const maxValue = Math.max(...data.map((d) => d.words_reviewed), 1);
  const todayIdx = new Date().getDay();
  const todayAdjusted = todayIdx === 0 ? 6 : todayIdx - 1;

  return (
    <div className="rounded-2xl border border-border/50 p-5 shadow-card">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
          <span className="font-heading text-sm font-semibold">This Week</span>
        </div>
        <span className="text-sm font-bold text-primary">{total}</span>
      </div>
      <div className="mt-4 flex items-end gap-1">
        {data.length === 0 ? (
          <p className="w-full py-10 text-center text-sm text-muted-foreground/40">No data yet</p>
        ) : (
          data.map((d, i) => (
            <WeeklyChartBar key={d.date} day={DAY_NAMES[i] || ''} value={d.words_reviewed} maxValue={maxValue} isToday={i === todayAdjusted} index={i} />
          ))
        )}
      </div>
    </div>
  );
}
