import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface WeeklyChartBarProps {
  day: string;
  value: number;
  maxValue: number;
  isToday: boolean;
  index: number;
}

export default function WeeklyChartBar({ day, value, maxValue, isToday, index }: WeeklyChartBarProps) {
  const height = maxValue > 0 ? (value / maxValue) * 100 : 0;

  return (
    <div className="flex flex-1 flex-col items-center gap-1">
      {value > 0 && <span className="text-[9px] font-medium text-muted-foreground">{value}</span>}
      <div className="relative h-40 w-full">
        <div className="absolute bottom-0 left-1/2 w-3/4 -translate-x-1/2 overflow-hidden rounded-t-md bg-muted/30">
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: `${height}%` }}
            transition={{ duration: 0.5, delay: index * 0.06, ease: 'easeOut' }}
            className={cn(
              'absolute bottom-0 w-full rounded-t-md',
              isToday ? 'bg-primary' : 'bg-primary/40',
            )}
            style={{ minHeight: value > 0 ? 4 : 0 }}
          />
          <div className="h-40" />
        </div>
      </div>
      <span className={cn('text-[10px] font-medium', isToday ? 'text-primary' : 'text-muted-foreground/60')}>
        {day}
      </span>
    </div>
  );
}
