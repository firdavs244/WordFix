import { Target } from 'lucide-react';
import CalendarCell from './CalendarCell';
import CalendarLegend from './CalendarLegend';
import type { CalendarDay } from '@/types';

interface StudyCalendarProps {
  data: CalendarDay[];
}

const DAY_HEADERS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

export default function StudyCalendar({ data }: StudyCalendarProps) {
  // Organize data into weeks (7 columns: Mon-Sun)
  const sorted = [...data].sort((a, b) => a.date.localeCompare(b.date));
  const weeks: CalendarDay[][] = [];
  let week: CalendarDay[] = [];

  for (const day of sorted) {
    const d = new Date(day.date);
    const dow = d.getDay() === 0 ? 6 : d.getDay() - 1; // Mon=0...Sun=6
    while (week.length < dow) week.push({ date: '', active: false, words_reviewed: 0, xp_earned: 0, goal_completed: false });
    week.push(day);
    if (week.length === 7) { weeks.push(week); week = []; }
  }
  if (week.length > 0) weeks.push(week);

  return (
    <div className="rounded-2xl border border-border/50 p-5 shadow-card">
      <div className="flex items-center gap-2">
        <Target className="h-4 w-4 text-muted-foreground" />
        <span className="font-heading text-sm font-semibold">Study Calendar</span>
      </div>
      <div className="mt-4">
        <div className="mb-1 grid grid-cols-7 gap-1">
          {DAY_HEADERS.map((d, i) => (
            <span key={i} className="text-center text-[8px] font-medium text-muted-foreground/40">{d}</span>
          ))}
        </div>
        <div className="space-y-1">
          {weeks.map((w, wi) => (
            <div key={wi} className="grid grid-cols-7 gap-1">
              {w.map((d, di) => (
                <CalendarCell key={di} date={d.date} wordCount={d.words_reviewed} goalCompleted={d.goal_completed} />
              ))}
              {Array.from({ length: 7 - w.length }).map((_, i) => (
                <div key={`empty-${i}`} className="h-3.5 w-3.5 md:h-4 md:w-4" />
              ))}
            </div>
          ))}
        </div>
        <CalendarLegend />
      </div>
    </div>
  );
}
