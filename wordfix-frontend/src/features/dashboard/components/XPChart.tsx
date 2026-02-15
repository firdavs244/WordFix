import { useMemo } from 'react';
import { TrendingUp, BarChart3 } from 'lucide-react';
import { AnimatedCounter } from '@/components/shared';
import { Skeleton } from '@/components/ui/skeleton';
import { useXPHistory } from '@/features/progress/hooks/useProgress';
import XPChartBar from './XPChartBar';

const DAY_LABELS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export default function XPChart() {
  const { data, isLoading } = useXPHistory(7);
  const history = data?.data ?? [];

  const { bars, maxVal, totalXP } = useMemo(() => {
    const today = new Date().getDay();
    const todayIdx = today === 0 ? 6 : today - 1;
    const entries = DAY_LABELS.map((label, i) => ({
      label,
      value: (history as Array<{ xp: number }>)[i]?.xp ?? 0,
      isToday: i === todayIdx,
    }));
    const mx = Math.max(...entries.map((e) => e.value), 1);
    const total = entries.reduce((s, e) => s + e.value, 0);
    return { bars: entries, maxVal: mx, totalXP: total };
  }, [history]);

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 shadow-card">
        <Skeleton className="h-52 w-full rounded-xl" />
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-border/50 bg-card p-8 shadow-card text-center">
        <BarChart3 className="h-10 w-10 text-muted-foreground/30" />
        <p className="mt-3 text-sm text-muted-foreground">
          Start learning to see your progress!
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center justify-between px-5 lg:px-6 pt-5">
        <div className="flex items-center gap-2">
          <TrendingUp className="h-[18px] w-[18px] text-primary" />
          <h3 className="text-base font-heading font-semibold">XP This Week</h3>
        </div>
        <span className="text-sm text-muted-foreground">
          <AnimatedCounter value={totalXP} suffix=" XP" />
        </span>
      </div>

      <div className="relative px-5 lg:px-6 py-5 h-52">
        {/* Grid lines */}
        {[25, 50, 75].map((pct) => (
          <div
            key={pct}
            className="absolute left-5 right-5 border-t border-dashed border-border/20"
            style={{ bottom: `${pct}%` }}
          />
        ))}
        <div className="flex h-full items-end justify-between gap-2 lg:gap-3">
          {bars.map((bar, i) => (
            <XPChartBar
              key={bar.label}
              value={bar.value}
              maxValue={maxVal}
              label={bar.label}
              isToday={bar.isToday}
              index={i}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
