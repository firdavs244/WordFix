import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';

interface StreakWeekDotsProps {
  activeDays: boolean[];
  currentDayIndex: number;
}

const DAY_LABELS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

export default function StreakWeekDots({ activeDays, currentDayIndex }: StreakWeekDotsProps) {
  return (
    <div className="mt-3 flex items-center justify-center gap-1">
      {DAY_LABELS.map((label, i) => {
        const isActive = activeDays[i];
        const isToday = i === currentDayIndex;

        return (
          <div key={i} className="flex flex-col items-center gap-1">
            <span className="text-[8px] text-muted-foreground/40 font-medium">{label}</span>
            <motion.div
              variants={staggerItem}
              initial="initial"
              animate="animate"
              transition={{ delay: i * 0.05 }}
              className={`rounded-full transition-colors ${
                isToday
                  ? 'h-[10px] w-[10px] ring-2 ring-orange-500/30'
                  : 'h-2 w-2'
              } ${
                isActive
                  ? 'bg-orange-500 shadow-[0_0_6px_rgba(249,115,22,0.3)]'
                  : 'bg-muted'
              }`}
            />
            {i < 6 && <div className="hidden" />}
          </div>
        );
      })}
    </div>
  );
}
