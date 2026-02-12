import { useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { OnboardingQuestion as QuestionType } from '@/features/onboarding/types';

interface OnboardingQuestionProps {
  question: QuestionType;
  selectedOption: string | null;
  onSelect: (option: string) => void;
  questionNumber: number;
}

export function OnboardingQuestion({
  question,
  selectedOption,
  onSelect,
  questionNumber,
}: OnboardingQuestionProps) {
  // Keyboard navigation: press 1-4 to select option
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      const num = parseInt(e.key, 10);
      if (num >= 1 && num <= question.options.length) {
        onSelect(question.options[num - 1]);
      }
    },
    [question.options, onSelect],
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return (
    <motion.div
      key={question.id}
      initial={{ opacity: 0, x: 60 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -60 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="space-y-6"
    >
      <div className="space-y-2">
        <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Question {questionNumber}
        </span>
        <h2 className="text-xl font-semibold leading-relaxed text-foreground md:text-2xl">
          {question.question_text}
        </h2>
      </div>

      <div className="grid gap-3">
        {question.options.map((option, i) => {
          const isSelected = selectedOption === option;

          return (
            <motion.button
              key={option}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              onClick={() => onSelect(option)}
              className={cn(
                'group flex items-center gap-4 rounded-xl border-2 p-4 text-left transition-all',
                'hover:border-primary/50 hover:bg-primary/5',
                isSelected
                  ? 'border-primary bg-primary/10 ring-1 ring-primary/30'
                  : 'border-border bg-card',
              )}
            >
              <span
                className={cn(
                  'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-bold transition-colors',
                  isSelected
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground group-hover:bg-primary/20 group-hover:text-primary',
                )}
              >
                {i + 1}
              </span>
              <span className={cn('text-sm font-medium md:text-base', isSelected && 'text-primary')}>
                {option}
              </span>
            </motion.button>
          );
        })}
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Press <kbd className="rounded bg-muted px-1.5 py-0.5 text-xs font-mono">1</kbd>-
        <kbd className="rounded bg-muted px-1.5 py-0.5 text-xs font-mono">{question.options.length}</kbd>{' '}
        to select, then <kbd className="rounded bg-muted px-1.5 py-0.5 text-xs font-mono">Enter</kbd> to continue
      </p>
    </motion.div>
  );
}
