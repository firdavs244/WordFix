import { motion } from 'framer-motion';

interface XPChartBarProps {
  value: number;
  maxValue: number;
  label: string;
  isToday: boolean;
  index: number;
}

export default function XPChartBar({ value, maxValue, label, isToday, index }: XPChartBarProps) {
  const heightPct = maxValue > 0 ? Math.max((value / maxValue) * 100, 2) : 2;

  return (
    <div className="flex flex-1 flex-col items-center gap-1.5">
      {/* Value label */}
      {value > 0 && (
        <span className={`text-[10px] font-semibold ${isToday ? 'text-primary font-bold' : 'text-foreground/70'}`}>
          {value}
        </span>
      )}

      {/* Bar */}
      <div className="flex w-full flex-1 items-end justify-center">
        <motion.div
          className={`w-full max-w-[40px] rounded-t-lg ${
            isToday
              ? 'bg-gradient-to-t from-primary to-primary/70 shadow-[0_0_12px_hsl(var(--primary)/0.25)]'
              : 'bg-gradient-to-t from-primary/90 to-primary/50'
          }`}
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: `${heightPct}%`, opacity: 1 }}
          transition={{ duration: 0.5, delay: index * 0.07, ease: [0.25, 0.46, 0.45, 0.94] }}
          style={{ minHeight: 4 }}
        >
          {isToday && (
            <div className="flex justify-center -mt-1.5">
              <span className="h-1 w-1 rounded-full bg-primary animate-pulse" />
            </div>
          )}
        </motion.div>
      </div>

      {/* Day label */}
      <span className={`text-[10px] font-medium ${isToday ? 'text-primary font-semibold' : 'text-muted-foreground/60'}`}>
        {label}
      </span>
    </div>
  );
}
