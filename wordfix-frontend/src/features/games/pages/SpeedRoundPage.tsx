import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { PageTransition } from '@/components/animations/PageTransition';
import { useStartSpeedRound, useSubmitSpeedRound } from '../hooks/useGames';
import type { SpeedRoundWord, SpeedRoundAnswer } from '@/types';

export function SpeedRoundPage() {
  const navigate = useNavigate();
  const startGame = useStartSpeedRound();
  const submitGame = useSubmitSpeedRound();

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [words, setWords] = useState<SpeedRoundWord[]>([]);
  const [timeLimit, setTimeLimit] = useState(60);
  const [timeLeft, setTimeLeft] = useState(60);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<SpeedRoundAnswer[]>([]);
  const [started, setStarted] = useState(false);
  const [finished, setFinished] = useState(false);
  const [flash, setFlash] = useState<'correct' | 'wrong' | null>(null);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const currentWord = words[currentIndex];

  // Start game
  const handleStart = () => {
    startGame.mutate(undefined as void, {
      onSuccess: (res) => {
        setSessionId(res.data.session_id);
        setWords(res.data.words);
        setTimeLimit(res.data.time_limit);
        setTimeLeft(res.data.time_limit);
        setStarted(true);
      },
    });
  };

  // Timer
  useEffect(() => {
    if (!started || finished) return;
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current!);
          setFinished(true);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [started, finished]);

  // Submit when finished or all answered
  useEffect(() => {
    if (!finished || !sessionId) return;
    submitGame.mutate(
      { sessionId, answers, duration: timeLimit - timeLeft },
      {
        onSuccess: (res) => {
          navigate(`/games/result/${sessionId}`, {
            replace: true,
            state: {
              game_type: 'speed_round',
              score: res.data.score,
              max_score: res.data.max_score,
              xp_earned: res.data.xp_earned,
              correct_answers: res.data.correct_answers,
              total_questions: res.data.total_questions,
            },
          });
        },
      },
    );
  }, [finished]);

  const handleAnswer = useCallback(
    (option: string) => {
      if (finished || !currentWord) return;
      const correct = option === currentWord.correct_translation;
      setFlash(correct ? 'correct' : 'wrong');
      setAnswers((a) => [...a, { word_id: currentWord.word_id, selected_answer: option }]);

      setTimeout(() => {
        setFlash(null);
        if (currentIndex + 1 < words.length) {
          setCurrentIndex((i) => i + 1);
        } else {
          setFinished(true);
        }
      }, 300);
    },
    [currentIndex, currentWord, finished, words.length],
  );

  // Pre-game screen
  if (!started) {
    return (
      <PageTransition>
        <div className="mx-auto flex max-w-md flex-col items-center justify-center gap-6 py-20">
          <div className="rounded-2xl bg-yellow-500/10 p-6">
            <Zap className="h-16 w-16 text-yellow-500" />
          </div>
          <h1 className="text-2xl font-bold">Speed Round</h1>
          <p className="text-center text-muted-foreground">
            Answer as many word translations as you can before time runs out! You have 60 seconds.
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
      <div className="mx-auto max-w-lg space-y-6">
        {/* Timer */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="flex items-center gap-1 text-muted-foreground">
              <Clock className="h-4 w-4" /> {timeLeft}s
            </span>
            <span className="text-muted-foreground">
              {currentIndex + 1}/{words.length}
            </span>
          </div>
          <Progress value={(timeLeft / timeLimit) * 100} className="h-2" />
        </div>

        {/* Word Card */}
        {currentWord && (
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.15 }}
            >
              <Card
                className={`border-2 transition-colors ${
                  flash === 'correct'
                    ? 'border-green-500 bg-green-500/5'
                    : flash === 'wrong'
                    ? 'border-red-500 bg-red-500/5'
                    : 'border-border/50'
                }`}
              >
                <CardContent className="space-y-6 p-6">
                  <p className="text-center text-2xl font-bold">{currentWord.word}</p>

                  <div className="grid grid-cols-2 gap-3">
                    {currentWord.options.map((opt) => (
                      <Button
                        key={opt}
                        variant="outline"
                        className="h-auto py-3 text-sm"
                        onClick={() => handleAnswer(opt)}
                        disabled={!!flash}
                      >
                        {opt}
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </AnimatePresence>
        )}
      </div>
    </PageTransition>
  );
}
