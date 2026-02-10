import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, ArrowRight, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { PageTransition } from '@/components/animations/PageTransition';
import { useStartWordContext, useSubmitWordContext } from '../hooks/useGames';
import { ComboIndicator } from '@/features/review/components';
import type { WordContextQuestion, WordContextAnswer } from '@/types';

export function WordContextPage() {
  const navigate = useNavigate();
  const startGame = useStartWordContext();
  const submitGame = useSubmitWordContext();

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<WordContextQuestion[]>([]);
  const [started, setStarted] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [answers, setAnswers] = useState<WordContextAnswer[]>([]);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [combo, setCombo] = useState(0);

  const currentQ = questions[currentIndex];
  const progress = questions.length > 0 ? ((currentIndex + (feedback ? 1 : 0)) / questions.length) * 100 : 0;

  const handleStart = () => {
    startGame.mutate(undefined as void, {
      onSuccess: (res) => {
        setSessionId(res.data.session_id);
        setQuestions(res.data.questions);
        setStarted(true);
      },
    });
  };

  const handleSubmit = () => {
    if (!currentQ || !userAnswer.trim()) return;
    const isCorrectGuess = userAnswer.trim().toLowerCase() === currentQ.correct_answer.toLowerCase();
    const answer: WordContextAnswer = {
      word_id: currentQ.word_id,
      selected_answer: userAnswer.trim(),
    };
    const newAnswers = [...answers, answer];
    setAnswers(newAnswers);

    if (isCorrectGuess) {
      setCombo((c) => c + 1);
    } else {
      setCombo(0);
    }

    // Show instant feedback
    setFeedback(currentQ.word_id);

    if (currentIndex + 1 >= questions.length) {
      // Submit all
      submitGame.mutate(
        { sessionId: sessionId!, answers: newAnswers },
        {
          onSuccess: (res) => {
            navigate(`/games/result/${sessionId}`, {
              replace: true,
              state: {
                game_type: 'word_context',
                score: res.data.score,
                max_score: res.data.max_score,
                xp_earned: res.data.xp_earned,
                correct_answers: res.data.correct_answers,
                total_questions: res.data.total_questions,
                max_combo: res.data.max_combo,
                combo_xp_bonus: res.data.combo_xp_bonus,
              },
            });
          },
        },
      );
    }
  };

  const handleNext = () => {
    setFeedback(null);
    setUserAnswer('');
    setCurrentIndex((i) => i + 1);
  };

  if (!started) {
    return (
      <PageTransition>
        <div className="mx-auto flex max-w-md flex-col items-center justify-center gap-6 py-20">
          <div className="rounded-2xl bg-purple-500/10 p-6">
            <BookOpen className="h-16 w-16 text-purple-500" />
          </div>
          <h1 className="text-2xl font-bold">Word Context</h1>
          <p className="text-center text-muted-foreground">
            Read a context paragraph and guess the blanked-out word. Use the clues to fill in the correct word.
          </p>
          <Button size="lg" onClick={handleStart} disabled={startGame.isPending}>
            {startGame.isPending ? 'Loading...' : 'Start Game'}
          </Button>
          {startGame.isError && (
            <p className="text-sm text-red-500">Not enough words to play. Add more words first!</p>
          )}
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Progress */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>Question {currentIndex + 1} of {questions.length}</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Combo Indicator */}
        <div className="flex justify-center">
          <ComboIndicator combo={combo} multiplier={combo >= 20 ? 5 : combo >= 10 ? 3 : combo >= 5 ? 2 : combo >= 2 ? 1.5 : 1} isActive={combo >= 2} />
        </div>

        {currentQ && (
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
                  <p className="text-lg leading-relaxed">{currentQ.context}</p>

                  {currentQ.hint && (
                    <p className="text-sm text-muted-foreground italic">Hint: {currentQ.hint}</p>
                  )}

                  <div className="flex gap-2">
                    <Input
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      placeholder="Type the missing word..."
                      disabled={!!feedback}
                      onKeyDown={(e) => e.key === 'Enter' && !feedback && handleSubmit()}
                      autoFocus
                    />
                    {!feedback && (
                      <Button onClick={handleSubmit} disabled={!userAnswer.trim()}>
                        <Send className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </AnimatePresence>
        )}

        {/* Next */}
        {feedback && currentIndex + 1 < questions.length && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <Button onClick={handleNext} className="w-full gap-2" size="lg">
              Next Question <ArrowRight className="h-5 w-5" />
            </Button>
          </motion.div>
        )}
      </div>
    </PageTransition>
  );
}
