import { motion } from 'framer-motion';

interface ProfileDailyGoalSliderProps {
  value: number;
  onChange: (v: number) => void;
}

export default function ProfileDailyGoalSlider({ value, onChange }: ProfileDailyGoalSliderProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-medium">Daily Goal</label>
        <motion.span
          key={value}
          className="text-sm font-bold text-primary bg-primary/10 px-2.5 py-0.5 rounded-lg"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
        >
          {value} words
        </motion.span>
      </div>
      <input
        type="range"
        min={5}
        max={50}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-2 rounded-full appearance-none bg-muted accent-primary cursor-pointer"
        aria-label="Daily Goal"
      />
      <div className="flex justify-between text-[10px] text-muted-foreground mt-1">
        <span>5</span>
        <span>50</span>
      </div>
    </div>
  );
}
