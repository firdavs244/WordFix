import { Target, XCircle, Clock, Zap } from 'lucide-react';

interface Props {
  correct: number;
  incorrect: number;
  duration: number;
  xp: number;
}

export default function GameResultStats({ correct, incorrect, duration, xp }: Props) {
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;

  const items = [
    { label: 'Correct', value: correct, icon: <Target className="h-4 w-4 text-success" /> },
    { label: 'Wrong', value: incorrect, icon: <XCircle className="h-4 w-4 text-destructive" /> },
    { label: 'Time', value: `${mins}:${String(secs).padStart(2, '0')}`, icon: <Clock className="h-4 w-4 text-muted-foreground" /> },
    { label: 'XP', value: `+${xp}`, icon: <Zap className="h-4 w-4 text-accent" /> },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 rounded-2xl border border-border/50 p-5 shadow-card sm:grid-cols-4" data-testid="game-result-stats">
      {items.map((s) => (
        <div key={s.label} className="text-center">
          <div className="mb-1 flex items-center justify-center">{s.icon}</div>
          <p className="font-heading text-xl font-bold">{s.value}</p>
          <p className="text-xs text-muted-foreground">{s.label}</p>
        </div>
      ))}
    </div>
  );
}
