import { Target } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { CalendarDay } from '@/types';

// ─── Study Calendar Heatmap ────────────────────────────────────────────────────

export function StudyCalendar({ data }: { data: CalendarDay[] }) {
  const getColor = (day: CalendarDay) => {
    if (!day.active) return 'bg-muted';
    if (day.goal_completed) return 'bg-green-500';
    if (day.words_reviewed > 10) return 'bg-green-400';
    if (day.words_reviewed > 5) return 'bg-green-300';
    if (day.words_reviewed > 0) return 'bg-green-200 dark:bg-green-900';
    return 'bg-muted';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Target className="h-4 w-4 text-primary" />
          Study Calendar
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-7 gap-1">
          {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((d) => (
            <div key={d} className="text-center text-xs text-muted-foreground">
              {d}
            </div>
          ))}
          {data.map((day) => (
            <div
              key={day.date}
              className={`aspect-square rounded-sm ${getColor(day)} transition-colors`}
              title={`${day.date}: ${day.words_reviewed} words reviewed`}
            />
          ))}
        </div>
        <div className="mt-3 flex items-center justify-end gap-2">
          <span className="text-xs text-muted-foreground">Less</span>
          <div className="h-3 w-3 rounded-sm bg-muted" />
          <div className="h-3 w-3 rounded-sm bg-green-200 dark:bg-green-900" />
          <div className="h-3 w-3 rounded-sm bg-green-300" />
          <div className="h-3 w-3 rounded-sm bg-green-400" />
          <div className="h-3 w-3 rounded-sm bg-green-500" />
          <span className="text-xs text-muted-foreground">More</span>
        </div>
      </CardContent>
    </Card>
  );
}
