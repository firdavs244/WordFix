interface Props {
  value: number;
  onChange: (v: number) => void;
  min?: number;
  max?: number;
}

const TICKS = [5, 10, 15, 20, 25, 30];

export default function QuestionCountSlider({ value, onChange, min = 5, max = 30 }: Props) {
  const pct = ((value - min) / (max - min)) * 100;

  return (
    <div>
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium">Questions</label>
        <span className="min-w-[28px] rounded-full bg-primary px-2 py-0.5 text-center text-xs font-bold text-white">
          {value}
        </span>
      </div>

      <div className="relative mt-3">
        <div className="h-2 rounded-full bg-muted">
          <div
            className="absolute left-0 h-2 rounded-full bg-gradient-to-r from-primary to-primary/70"
            style={{ width: `${pct}%` }}
          />
          <div
            className="absolute top-1/2 h-5 w-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-primary bg-white shadow-md transition-transform hover:scale-110"
            style={{ left: `${pct}%` }}
          />
        </div>
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="absolute inset-0 w-full cursor-pointer opacity-0"
          aria-label="Question count"
        />
      </div>

      <div className="mt-2 flex justify-between">
        {TICKS.map((t) => (
          <span key={t} className="text-[8px] text-muted-foreground/30">{t}</span>
        ))}
      </div>
    </div>
  );
}
