import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, ArrowRight, RotateCcw, Brain, Lightbulb, BookOpen, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useGenerateDrill, useResolvePair } from '../hooks/useConfusingPairs';
import type { DrillData } from '../types';
import confetti from 'canvas-confetti';

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
        onError: () => {
          onClose();
        },
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
  const getMessage = () => {
    if (scorePct === 100) return "Perfect! You've mastered this pair!";
    if (scorePct >= 80) return 'Great job! Almost there!';
    return "Keep practicing! You'll get it!";
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        className="w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-background border shadow-2xl"
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        transition={{ duration: 0.2 }}
      >
        <div className="p-6">
          {/* Close button */}
          <div className="flex justify-end mb-2">
            <Button variant="ghost" size="sm" onClick={onClose}>
              ✕
            </Button>
          </div>

          {/* Loading */}
          {step === 'loading' && (
            <div className="flex flex-col items-center justify-center gap-4 py-12">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
              <p className="text-muted-foreground">Generating drill...</p>
            </div>
          )}

          {/* Explanation */}
          {step === 'explanation' && drill && (
            <AnimatePresence mode="wait">
              <motion.div
                key="explanation"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                className="space-y-6"
              >
                <div className="flex items-center gap-2">
                  <Brain className="h-6 w-6 text-primary" />
                  <h2 className="font-heading text-xl font-bold">Understanding the Difference</h2>
                </div>

                {/* Explanation */}
                <Card className="border-border/50">
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center gap-2 text-base">
                      <BookOpen className="h-4 w-4 text-blue-500" />
                      Explanation
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm leading-relaxed">{drill.explanation}</p>
                  </CardContent>
                </Card>

                {/* Mnemonic */}
                <Card className="border-amber-500/30 bg-amber-500/5">
                  <CardContent className="flex items-start gap-3 p-4">
                    <Lightbulb className="h-5 w-5 mt-0.5 text-amber-500" />
                    <div>
                      <p className="text-sm font-medium text-amber-600 dark:text-amber-400">Memory Trick</p>
                      <p className="text-sm mt-1">{drill.mnemonic}</p>
                    </div>
                  </CardContent>
                </Card>

                {/* Examples */}
                <div className="grid gap-4 sm:grid-cols-2">
                  {drill.word_1_examples.length > 0 && (
                    <Card className="border-border/50">
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm text-primary">Examples</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        {drill.word_1_examples.map((ex, i) => (
                          <div key={i} className="text-sm">
                            <p className="italic">&ldquo;{ex.sentence}&rdquo;</p>
                            <p className="text-muted-foreground text-xs">{ex.translation}</p>
                          </div>
                        ))}
                      </CardContent>
                    </Card>
                  )}

                  {drill.word_2_examples.length > 0 && (
                    <Card className="border-border/50">
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm text-primary">Examples</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        {drill.word_2_examples.map((ex, i) => (
                          <div key={i} className="text-sm">
                            <p className="italic">&ldquo;{ex.sentence}&rdquo;</p>
                            <p className="text-muted-foreground text-xs">{ex.translation}</p>
                          </div>
                        ))}
                      </CardContent>
                    </Card>
                  )}
                </div>

                <Button onClick={() => setStep('quiz')} className="w-full gap-2" size="lg">
                  Start Practice Quiz
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </motion.div>
            </AnimatePresence>
          )}

          {/* Quiz */}
          {step === 'quiz' && drill && currentQuestion && (
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
                  &ldquo;{currentQuestion.sentence}&rdquo;
                </p>

                <div className="grid gap-3">
                  {[currentQuestion.correct_answer, currentQuestion.wrong_answer]
                    .sort(() => Math.random() - 0.5)
                    .map((opt) => {
                      let variant: 'outline' | 'default' | 'destructive' = 'outline';
                      if (answered) {
                        if (opt === currentQuestion.correct_answer) variant = 'default';
                        else if (opt === selectedAnswer) variant = 'destructive';
                      }
                      return (
                        <Button
                          key={opt}
                          variant={!answered && selectedAnswer === opt ? 'default' : variant}
                          className="justify-start text-left h-auto py-3 px-4 transition-all"
                          onClick={() => handleAnswer(opt)}
                          disabled={answered}
                        >
                          {opt}
                        </Button>
                      );
                    })}
                </div>

                {/* Feedback */}
                {answered && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`rounded-lg p-4 ${
                      selectedAnswer === currentQuestion.correct_answer
                        ? 'bg-green-500/10 text-green-700 dark:text-green-400'
                        : 'bg-red-500/10 text-red-700 dark:text-red-400'
                    }`}
                  >
                    <div className="flex items-center gap-2 font-medium">
                      {selectedAnswer === currentQuestion.correct_answer ? (
                        <>
                          <CheckCircle2 className="h-5 w-5" />
                          Correct! 🎉
                        </>
                      ) : (
                        <>
                          <XCircle className="h-5 w-5" />
                          The correct answer is &ldquo;{currentQuestion.correct_answer}&rdquo;
                        </>
                      )}
                    </div>
                    {currentQuestion.explanation && (
                      <p className="mt-1 text-sm opacity-80">{currentQuestion.explanation}</p>
                    )}
                  </motion.div>
                )}

                {answered && (
                  <Button onClick={handleNext} className="w-full gap-2" size="lg">
                    {quizIndex + 1 < totalQuestions ? 'Next Question' : 'See Results'}
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                )}
              </motion.div>
            </AnimatePresence>
          )}

          {/* Result */}
          {step === 'result' && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-6 text-center"
            >
              <Sparkles className="mx-auto h-12 w-12 text-primary" />
              <h2 className="font-heading text-2xl font-bold">🎉 Drill Complete!</h2>
              <p className="text-3xl font-bold">
                {score.correct}/{totalQuestions}{' '}
                <span className="text-lg text-muted-foreground">({scorePct}%)</span>
              </p>
              <p className="text-muted-foreground">{getMessage()}</p>

              <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
                {scorePct >= 80 && (
                  <Button onClick={handleResolve} className="gap-2" size="lg">
                    Mark as Resolved ✅
                  </Button>
                )}
                <Button variant="outline" onClick={handleRetry} className="gap-2" size="lg">
                  <RotateCcw className="h-4 w-4" />
                  Practice Again 🔄
                </Button>
                <Button variant="ghost" onClick={onClose} size="lg">
                  Close
                </Button>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
