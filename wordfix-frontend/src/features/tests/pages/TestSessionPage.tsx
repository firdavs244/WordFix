import { useState, useEffect, useCallback } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, ArrowRight, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Input } from '@/components/ui/input';
import { PageTransition } from '@/components/animations/PageTransition';
import { useSubmitTestAnswer, useCompleteTest } from '../hooks/useTests';
import type { TestQuestion, TestSession } from '@/types';

export function TestSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const [questions] = useState<TestQuestion[]>(location.state?.questions ?? []);
  const [session] = useState<TestSession | null>(location.state?.session ?? null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [fillAnswer, setFillAnswer] = useState('');
  const [feedback, setFeedback] = useState<{ isCorrect: boolean; correctAnswer: string; explanation: string } | null>(null);
  const [startTime, setStartTime] = useState(Date.now());
  const [score, setScore] = useState({ correct: 0, total: 0 });

  const submitAnswer = useSubmitTestAnswer();
  const completeTest = useCompleteTest();

  const currentQ = questions[currentIndex];
  const isFillBlank = currentQ?.question_type === 'fill_blank' || currentQ?.question_type === 'translation_to_word';
  const progress = questions.length > 0 ? ((currentIndex + (feedback ? 1 : 0)) / questions.length) * 100 : 0;

  useEffect(() => { setStartTime(Date.now()); }, [currentIndex]);

  const handleSubmit = useCallback(() => {
    if (!sessionId || !currentQ) return;
    const answer = isFillBlank ? fillAnswer.trim() : selectedAnswer;
    if (!answer) return;

    const responseTime = Date.now() - startTime;

    submitAnswer.mutate(
      { sessionId, data: { question_id: currentQ.id, answer, response_time_ms: responseTime } },
      {
        onSuccess: (res) => {
          setFeedback({
            isCorrect: res.data.is_correct,
            correctAnswer: res.data.correct_answer,
            explanation: res.data.explanation,
          });
          setScore((s) => ({
            correct: s.correct + (res.data.is_correct ? 1 : 0),
            total: s.total + 1,
          }));
        },
      },
    );
  }, [sessionId, currentQ, isFillBlank, fillAnswer, selectedAnswer, startTime, submitAnswer]);

  const handleNext = () => {
    setFeedback(null);
    setSelectedAnswer('');
    setFillAnswer('');
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
    } else {
      completeTest.mutate(sessionId!, {
        onSuccess: () => navigate(`/tests/result/${sessionId}`, { replace: true }),
      });
    }
  };

  if (!session || questions.length === 0) {
    return (
      <PageTransition>
        <div className="flex h-full items-center justify-center">
          <p className="text-muted-foreground">No test data. Please generate a test first.</p>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>Question {currentIndex + 1} of {questions.length}</span>
            <span className="flex items-center gap-1">
              <CheckCircle2 className="h-4 w-4 text-green-500" /> {score.correct}/{score.total}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -30 }}
            transition={{ duration: 0.25 }}
          >
            <Card className="border-border/50">
              <CardContent className="space-y-6 p-6">
                <p className="text-lg font-medium leading-relaxed">{currentQ.question_text}</p>

                {/* Options or Input */}
                {isFillBlank ? (
                  <div className="flex gap-2">
                    <Input
                      value={fillAnswer}
                      onChange={(e) => setFillAnswer(e.target.value)}
                      placeholder="Type your answer..."
                      disabled={!!feedback}
                      onKeyDown={(e) => e.key === 'Enter' && !feedback && handleSubmit()}
                      autoFocus
                    />
                    {!feedback && (
                      <Button onClick={handleSubmit} disabled={!fillAnswer.trim() || submitAnswer.isPending}>
                        <Send className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ) : (
                  <div className="grid gap-2">
                    {currentQ.options.map((opt) => {
                      let variant: 'outline' | 'default' | 'destructive' = 'outline';
                      if (feedback) {
                        if (opt === feedback.correctAnswer) variant = 'default';
                        else if (opt === selectedAnswer && !feedback.isCorrect) variant = 'destructive';
                      }
                      return (
                        <Button
                          key={opt}
                          variant={!feedback && selectedAnswer === opt ? 'default' : variant}
                          className="justify-start text-left h-auto py-3 px-4"
                          onClick={() => {
                            if (!feedback) {
                              setSelectedAnswer(opt);
                              // Auto-submit on option select
                              const answer = opt;
                              const responseTime = Date.now() - startTime;
                              submitAnswer.mutate(
                                { sessionId: sessionId!, data: { question_id: currentQ.id, answer, response_time_ms: responseTime } },
                                {
                                  onSuccess: (res) => {
                                    setSelectedAnswer(opt);
                                    setFeedback({
                                      isCorrect: res.data.is_correct,
                                      correctAnswer: res.data.correct_answer,
                                      explanation: res.data.explanation,
                                    });
                                    setScore((s) => ({
                                      correct: s.correct + (res.data.is_correct ? 1 : 0),
                                      total: s.total + 1,
                                    }));
                                  },
                                },
                              );
                            }
                          }}
                          disabled={!!feedback}
                        >
                          {opt}
                        </Button>
                      );
                    })}
                  </div>
                )}

                {/* Feedback */}
                <AnimatePresence>
                  {feedback && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`rounded-lg p-4 ${feedback.isCorrect ? 'bg-green-500/10 text-green-700 dark:text-green-400' : 'bg-red-500/10 text-red-700 dark:text-red-400'}`}
                    >
                      <div className="flex items-center gap-2 font-medium">
                        {feedback.isCorrect ? <CheckCircle2 className="h-5 w-5" /> : <XCircle className="h-5 w-5" />}
                        {feedback.isCorrect ? 'Correct!' : `Incorrect. Answer: ${feedback.correctAnswer}`}
                      </div>
                      {feedback.explanation && (
                        <p className="mt-1 text-sm opacity-80">{feedback.explanation}</p>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>

        {/* Next Button */}
        {feedback && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <Button onClick={handleNext} className="w-full gap-2" size="lg">
              {currentIndex + 1 < questions.length ? 'Next Question' : 'See Results'}
              <ArrowRight className="h-5 w-5" />
            </Button>
          </motion.div>
        )}
      </div>
    </PageTransition>
  );
}
