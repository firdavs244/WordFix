import { useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Check, Loader2 } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import type { OnboardingQuestion as QType } from '../types';
import { OnboardingProgress } from './OnboardingProgress';
import { OnboardingOptionCard } from './OnboardingOptionCard';

interface Props {
  question: QType;
  currentIndex: number;
  totalQuestions: number;
  selectedAnswer: string | null;
  selectAnswer: (a: string) => void;
  nextQuestion: () => void;
  isLastQuestion: boolean;
  isSubmitting: boolean;
}

export function OnboardingQuestionScreen({
  question, currentIndex, totalQuestions, selectedAnswer, selectAnswer, nextQuestion, isLastQuestion, isSubmitting,
}: Props) {
  const handleKey = useCallback((e: KeyboardEvent) => {
    const n = parseInt(e.key, 10);
    if (n >= 1 && n <= question.options.length) selectAnswer(question.options[n - 1]);
  }, [question.options, selectAnswer]);

  useEffect(() => {
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  return (
    <motion.div initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }} transition={{ duration: 0.25 }}>
      <OnboardingProgress current={currentIndex + 1} total={totalQuestions} />

      <h2 className="mx-auto mt-4 mb-8 max-w-md text-center font-heading text-lg font-semibold leading-snug lg:text-xl">
        {question.question_text}
      </h2>

      <motion.div variants={staggerContainer} initial="initial" animate="animate" className="space-y-3">
        {question.options.map((opt, i) => (
          <OnboardingOptionCard key={opt} text={opt} index={i} isSelected={selectedAnswer === opt} onClick={() => selectAnswer(opt)} />
        ))}
      </motion.div>

      <button
        onClick={nextQuestion}
        disabled={!selectedAnswer || isSubmitting}
        className="mt-8 flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white transition-all hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : isLastQuestion ? <><Check className="h-4 w-4" /> Finish Assessment</> : <>Next Question <ArrowRight className="h-4 w-4" /></>}
      </button>
    </motion.div>
  );
}
