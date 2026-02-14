import { useState, useCallback, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useGenerateDrill, useResolvePair } from '../hooks/useConfusingPairs';
import type { DrillData } from '../types';
import confetti from 'canvas-confetti';
import { DrillExplanation } from './DrillExplanation';
import { DrillQuiz } from './DrillQuiz';
import { DrillResult } from './DrillResult';

interface DrillModalProps {
  pairId: string;
  isOpen: boolean;
  onClose: () => void;
}

type DrillStep = 'loading' | 'explanation' | 'quiz' | 'result';

export function DrillModal({ pairId, isOpen, onClose }: DrillModalProps) {
  const [step, setStep] = useState<DrillStep>('loading');
  const [drill, setDrill] = useState<DrillData | null>(null);
  const [quizIndex, setQuizIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState({ correct: 0, total: 0 });

  const generateDrill = useGenerateDrill();
  const resolvePair = useResolvePair();

  useEffect(() => {
    if (isOpen && pairId) {
      setStep('loading');
      setQuizIndex(0);
      setScore({ correct: 0, total: 0 });
      setSelectedAnswer(null);
      setAnswered(false);
      generateDrill.mutate(pairId, {
        onSuccess: (res) => {
          setDrill(res.data);
          setStep('explanation');
        },
        onError: () => onClose(),
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, pairId]);

  const currentQuestion = drill?.test_questions[quizIndex] ?? null;
  const totalQuestions = drill?.test_questions.length ?? 0;

  const handleAnswer = useCallback(
    (answer: string) => {
      if (answered || !currentQuestion) return;
      setSelectedAnswer(answer);
      setAnswered(true);
      const isCorrect = answer === currentQuestion.correct_answer;
      setScore((s) => ({
        correct: s.correct + (isCorrect ? 1 : 0),
        total: s.total + 1,
      }));
    },
    [answered, currentQuestion],
  );

  const handleNext = () => {
    if (quizIndex + 1 < totalQuestions) {
      setQuizIndex((i) => i + 1);
      setSelectedAnswer(null);
      setAnswered(false);
    } else {
      setStep('result');
      const pct = totalQuestions > 0 ? (score.correct / totalQuestions) * 100 : 0;
      if (pct === 100) {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      }
    }
  };

  const handleResolve = () => {
    resolvePair.mutate(pairId);
    onClose();
  };

  const handleRetry = () => {
    setStep('explanation');
    setQuizIndex(0);
    setScore({ correct: 0, total: 0 });
    setSelectedAnswer(null);
    setAnswered(false);
  };

  if (!isOpen) return null;

  const scorePct = totalQuestions > 0 ? Math.round((score.correct / totalQuestions) * 100) : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border bg-background shadow-2xl"
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        transition={{ duration: 0.2 }}
      >
        <div className="p-6">
          <div className="mb-2 flex justify-end">
            <Button variant="ghost" size="sm" onClick={onClose}>
              ✕
            </Button>
          </div>

          {step === 'loading' && (
            <div className="flex flex-col items-center justify-center gap-4 py-12">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
              <p className="text-muted-foreground">Generating drill...</p>
            </div>
          )}

          {step === 'explanation' && drill && (
            <DrillExplanation drill={drill} onStartQuiz={() => setStep('quiz')} />
          )}

          {step === 'quiz' && drill && currentQuestion && (
            <DrillQuiz
              question={currentQuestion}
              quizIndex={quizIndex}
              totalQuestions={totalQuestions}
              selectedAnswer={selectedAnswer}
              answered={answered}
              onAnswer={handleAnswer}
              onNext={handleNext}
            />
          )}

          {step === 'result' && (
            <DrillResult
              correct={score.correct}
              total={totalQuestions}
              scorePct={scorePct}
              onResolve={handleResolve}
              onRetry={handleRetry}
              onClose={onClose}
            />
          )}
        </div>
      </motion.div>
    </div>
  );
}
