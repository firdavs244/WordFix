import { Layers } from 'lucide-react';
import ConfidenceBar from './ConfidenceBar';

interface DifficultyDistributionProps {
  data: Record<string, number>;
}

const COLORS: Record<string, string> = {
  easy: 'bg-emerald-400',
  medium: 'bg-amber-400',
  hard: 'bg-red-400',
  unknown: 'bg-slate-400',
};

const ORDER = ['easy', 'medium', 'hard', 'unknown'];

export default function DifficultyDistribution({ data }: DifficultyDistributionProps) {
  const total = Object.values(data).reduce((s, v) => s + v, 0);
  const sorted = ORDER.filter((k) => k in data);

  return (
    <div className="rounded-2xl border border-border/50 p-5 shadow-card">
      <div className="flex items-center gap-2">
        <Layers className="h-4 w-4 text-muted-foreground" />
        <span className="font-heading text-sm font-semibold">By Difficulty</span>
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
