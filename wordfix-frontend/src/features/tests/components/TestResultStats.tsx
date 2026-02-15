import { CheckCircle2, XCircle, Hash, Clock } from 'lucide-react';

interface StatItem {
  label: string;
  value: number | string;
  icon: React.ReactNode;
}

interface Props {
  correct: number;
  incorrect: number;
  total: number;
  duration: number;
}

export default function TestResultStats({ correct, incorrect, total, duration }: Props) {
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;

  const stats: StatItem[] = [
    { label: 'Correct', value: correct, icon: <CheckCircle2 className="h-4 w-4 text-success" /> },
    { label: 'Incorrect', value: incorrect, icon: <XCircle className="h-4 w-4 text-destructive" /> },
    { label: 'Total', value: total, icon: <Hash className="h-4 w-4 text-primary" /> },
    { label: 'Duration', value: `${mins}:${String(secs).padStart(2, '0')}`, icon: <Clock className="h-4 w-4 text-muted-foreground" /> },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 rounded-2xl border border-border/50 p-5 shadow-card sm:grid-cols-4" data-testid="result-stats">
      {stats.map((s) => (
        <div key={s.label} className="text-center">
          <div className="mb-1 flex items-center justify-center">{s.icon}</div>
          <p className="font-heading text-xl font-bold">{s.value}</p>
          <p className="text-xs text-muted-foreground">{s.label}</p>
        </div>
      ))}
    </div>
  );
}
