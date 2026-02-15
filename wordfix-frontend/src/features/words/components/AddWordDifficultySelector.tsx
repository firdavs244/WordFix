import type { DifficultyLevel } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  value: DifficultyLevel;
  onChange: (v: DifficultyLevel) => void;
}

const options: { value: DifficultyLevel; label: string; dot: string; selected: string }[] = [
  { value: 'easy', label: 'Easy', dot: 'bg-success', selected: 'bg-success/10 border-success/50 text-success' },
  { value: 'medium', label: 'Medium', dot: 'bg-accent', selected: 'bg-accent/10 border-accent/50 text-accent' },
  { value: 'hard', label: 'Hard', dot: 'bg-destructive', selected: 'bg-destructive/10 border-destructive/50 text-destructive' },
];

export default function AddWordDifficultySelector({ value, onChange }: Props) {
  return (
    <div>
      <label className="mb-2 block text-sm font-medium">Difficulty</label>
      <div className="grid grid-cols-3 gap-2">
        {options.map((opt) => (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            className={cn(
              'flex h-11 items-center justify-center gap-1.5 rounded-xl border text-sm font-medium transition-colors duration-150',
              value === opt.value ? opt.selected : 'border-border/50 text-muted-foreground hover:bg-muted/50',
            )}
          >
            <span className={cn('h-1.5 w-1.5 rounded-full', opt.dot)} />
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
