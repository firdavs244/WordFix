import { AnimatedCounter } from '@/components/shared';

interface Props {
  total: number;
  correct: number;
  accuracy: number;
  maxCombo: number;
  comboXp: number;
}

export default function CompletionStats({ total, correct, accuracy, maxCombo, comboXp }: Props) {
  return (
    <div className="mt-6 rounded-2xl border border-border/50 bg-card p-6 shadow-card">
      <div className="grid grid-cols-3 gap-4 text-center">
        <div>
          <AnimatedCounter value={total} className="font-heading text-2xl font-bold" />
          <p className="mt-0.5 text-xs text-muted-foreground">Reviewed</p>
        </div>
        <div>
          <AnimatedCounter value={correct} className="font-heading text-2xl font-bold text-success" />
          <p className="mt-0.5 text-xs text-muted-foreground">Correct</p>
        </div>
        <div>
          <AnimatedCounter value={accuracy} suffix="%" className="font-heading text-2xl font-bold" />
          <p className="mt-0.5 text-xs text-muted-foreground">Accuracy</p>
        </div>
      </div>
      {maxCombo > 0 && (
        <>
          <div className="my-4 h-px bg-border/30" />
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Max Combo: {maxCombo}</span>
            <span className="font-medium text-accent">Bonus: +{comboXp} XP</span>
          </div>
        </>
      )}
    </div>
  );
}
