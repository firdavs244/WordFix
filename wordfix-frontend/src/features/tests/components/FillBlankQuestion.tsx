import { useState, useRef, useEffect } from 'react';
import { SendHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Props {
  sentence: string;
  onSubmit: (answer: string) => void;
  answered: boolean;
  correctAnswer?: string;
  userAnswer?: string;
  isCorrect?: boolean;
}

export default function FillBlankQuestion({
  sentence, onSubmit, answered, correctAnswer, userAnswer, isCorrect,
}: Props) {
  const [value, setValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { inputRef.current?.focus(); }, []);

  const handleSubmit = () => {
    if (value.trim() && !answered) onSubmit(value.trim());
  };

  const parts = sentence.split('___');

  return (
    <div>
      <p className="text-base leading-relaxed">
        {parts[0]}
        <span className={cn(
          'inline-block min-w-[80px] rounded border-b-2 px-4 py-0.5',
          !answered && 'border-primary/30 bg-primary/10',
          answered && isCorrect && 'border-success/30 bg-success/10 font-semibold text-success',
          answered && !isCorrect && 'border-destructive/30 bg-destructive/10 font-semibold text-destructive line-through',
        )}>
          {answered ? userAnswer || '___' : '___'}
        </span>
        {parts[1]}
      </p>

      {answered && !isCorrect && correctAnswer && (
        <p className="mt-1 text-sm font-medium text-success">Correct: {correctAnswer}</p>
      )}

      {!answered && (
        <div className="mt-6 flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            placeholder="Type your answer..."
            className="h-11 flex-1 rounded-xl border border-border/50 bg-background px-4 text-sm outline-none transition-colors focus:border-primary focus:ring-2 focus:ring-primary/10"
            disabled={answered}
            aria-label="Answer input"
          />
          <button
            type="button"
            onClick={handleSubmit}
            disabled={!value.trim()}
            className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-white transition-opacity disabled:opacity-50"
            aria-label="Submit answer"
          >
            <SendHorizontal className="h-[18px] w-[18px]" />
          </button>
        </div>
      )}
    </div>
  );
}
