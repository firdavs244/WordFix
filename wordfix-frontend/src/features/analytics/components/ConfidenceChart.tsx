import { BarChart3 } from 'lucide-react';
import ConfidenceBar from './ConfidenceBar';

interface ConfidenceChartProps {
  data: Record<string, number>;
}

const COLORS: Record<string, string> = {
  mastered: 'bg-emerald-500',
  confident: 'bg-blue-500',
  learning: 'bg-amber-500',
  new: 'bg-slate-400',
  struggling: 'bg-red-500',
};

const ORDER = ['mastered', 'confident', 'learning', 'new', 'struggling'];

export default function ConfidenceChart({ data }: ConfidenceChartProps) {
  const total = Object.values(data).reduce((s, v) => s + v, 0);
  const sorted = ORDER.filter((k) => k in data);

  return (
    <div className="rounded-2xl border border-border/50 p-5 shadow-card">
      <div className="flex items-center gap-2">
        <BarChart3 className="h-4 w-4 text-muted-foreground" />
        <span className="font-heading text-sm font-semibold">By Confidence</span>
      </div>
      <div className="mt-4 space-y-3">
        {sorted.map((key) => (
          <ConfidenceBar
            key={key}
            label={key}
            count={data[key]}
            total={total}
            color={COLORS[key] ?? 'bg-muted'}
          />
        ))}
      </div>
    </div>
  );
}
