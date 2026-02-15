import { useState } from 'react';
import { ChevronDown, CheckCircle2, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { TestQuestion } from '@/types';

interface Props {
  question: TestQuestion;
  index: number;
}

export default function TestQuestionReviewItem({ question, index }: Props) {
  const [open, setOpen] = useState(false);
  const correct = question.is_correct === true;

  return (
    <div className={cn('overflow-hidden rounded-lg border-l-4', correct ? 'border-l-success' : 'border-l-destructive')}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-3 p-3 text-left transition-colors hover:bg-muted/30"
      >
        {correct ? (
          <CheckCircle2 className="h-4 w-4 flex-shrink-0 text-success" />
        ) : (
          <XCircle className="h-4 w-4 flex-shrink-0 text-destructive" />
        )}
        <span className="text-xs font-bold text-muted-foreground">Q{index + 1}</span>
        <span className="flex-1 truncate text-sm">{question.question_text}</span>
        <ChevronDown className={cn('h-4 w-4 text-muted-foreground transition-transform', open && 'rotate-180')} />
      </button>

      {open && (
        <div className="border-t border-border/30 bg-muted/10 px-4 py-3">
          <p className="text-sm">{question.question_text}</p>
          <div className="mt-2 space-y-1">
            <p className="text-xs">
              <span className="text-muted-foreground">Your answer: </span>
              <span className={cn('font-medium', correct ? 'text-success' : 'text-destructive')}>
                {question.user_answer || '—'}
              </span>
            </p>
            {!correct && question.correct_answer && (
              <p className="text-xs">
                <span className="text-muted-foreground">Correct: </span>
                <span className="font-medium text-success">{question.correct_answer}</span>
              </p>
            )}
            {question.explanation && (
              <p className="mt-1 text-xs text-muted-foreground">{question.explanation}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
