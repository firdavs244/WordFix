import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface QuizQuestion {
  sentence: string;
  correct_answer: string;
  wrong_answer: string;
  explanation?: string;
}

interface DrillQuizProps {
  question: QuizQuestion;
  quizIndex: number;
  totalQuestions: number;
  selectedAnswer: string | null;
  answered: boolean;
  onAnswer: (answer: string) => void;
  onNext: () => void;
}

export function DrillQuiz({
  question,
  quizIndex,
  totalQuestions,
  selectedAnswer,
  answered,
  onAnswer,
  onNext,
}: DrillQuizProps) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={`quiz-${quizIndex}`}
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -30 }}
        className="space-y-6"
      >
        <p className="text-sm text-muted-foreground">
          Question {quizIndex + 1} of {totalQuestions}
        </p>

        <p className="text-lg font-medium leading-relaxed">
          &ldquo;{question.sentence}&rdquo;
        </p>

        <div className="grid gap-3">
          {[question.correct_answer, question.wrong_answer]
            .sort(() => Math.random() - 0.5)
            .map((opt) => {
              let variant: 'outline' | 'default' | 'destructive' = 'outline';
              if (answered) {
                if (opt === question.correct_answer) variant = 'default';
                else if (opt === selectedAnswer) variant = 'destructive';
              }
              return (
                <Button
                  key={opt}
                  variant={!answered && selectedAnswer === opt ? 'default' : variant}
                  className="h-auto justify-start px-4 py-3 text-left transition-all"
                  onClick={() => onAnswer(opt)}
                  disabled={answered}
                >
                  {opt}
                </Button>
              );
            })}
        </div>

        {answered && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-lg p-4 ${
              selectedAnswer === question.correct_answer
                ? 'bg-green-500/10 text-green-700 dark:text-green-400'
                : 'bg-red-500/10 text-red-700 dark:text-red-400'
            }`}
          >
            <div className="flex items-center gap-2 font-medium">
              {selectedAnswer === question.correct_answer ? (
                <>
                  <CheckCircle2 className="h-5 w-5" />
                  Correct! 🎉
                </>
              ) : (
                <>
                  <XCircle className="h-5 w-5" />
                  The correct answer is &ldquo;{question.correct_answer}&rdquo;
                </>
              )}
            </div>
            {question.explanation && (
              <p className="mt-1 text-sm opacity-80">{question.explanation}</p>
            )}
          </motion.div>
        )}

        {answered && (
          <Button onClick={onNext} className="w-full gap-2" size="lg">
            {quizIndex + 1 < totalQuestions ? 'Next Question' : 'See Results'}
            <ArrowRight className="h-5 w-5" />
          </Button>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
