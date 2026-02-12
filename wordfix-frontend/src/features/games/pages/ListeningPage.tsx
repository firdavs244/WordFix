import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Headphones,
  Volume2,
  Loader2,
  Check,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { PageTransition } from '@/components/animations/PageTransition';
import { ComboIndicator } from '@/features/review/components/ComboIndicator';
import {
  useStartListening,
  useSubmitListeningAnswer,
  useCompleteListening,
} from '../hooks/useGames';
import { toast } from 'sonner';
import type {
  ListeningStartResponse,
  ListeningAnswerResponse,
  ListeningCompleteResponse,
} from '@/types';

// ─── Types ─────────────────────────────────────────────────────────────────────

type Phase = 'READY' | 'PLAYING' | 'COMPLETE';
type FeedbackType = 'correct' | 'wrong' | 'failed' | null;

interface RoundState {
  roundNumber: number;
  audioUrl: string;
  hint: string;
  maxAttempts: number;
  attemptsUsed: number;
}

// ─── Audio Hook ────────────────────────────────────────────────────────────────

function useAudioPlayer(url: string) {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!url) return;
    const audio = new Audio(url);
    audioRef.current = audio;
    audio.addEventListener('ended', () => setIsPlaying(false));
    audio.addEventListener('error', () => setIsPlaying(false));
    return () => {
      audio.pause();
      audio.removeEventListener('ended', () => setIsPlaying(false));
      audio.removeEventListener('error', () => setIsPlaying(false));
    };
  }, [url]);

  const play = useCallback(() => {
    if (!audioRef.current || !url) return;
    audioRef.current.currentTime = 0;
    audioRef.current.play().then(() => setIsPlaying(true)).catch(() => {});
  }, [url]);

  return { play, isPlaying };
}

// ─── Helpers ───────────────────────────────────────────────────────────────────

function getStars(pct: number) {
  if (pct >= 90) return 5;
  if (pct >= 75) return 4;
  if (pct >= 60) return 3;
  if (pct >= 40) return 2;
  if (pct >= 20) return 1;
  return 0;
}

function getAttemptLabel(attempts: number) {
  switch (attempts) {
    case 1: return '1st try';
    case 2: return '2nd try';
    case 3: return '3rd try';
    default: return `${attempts}th try`;
  }
}

function fireConfetti() {
  import('canvas-confetti').then((mod) => {
    const confetti = mod.default;
    confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
  }).catch(() => {});
}

// ─── Main Component ────────────────────────────────────────────────────────────

export function ListeningPage() {
  const navigate = useNavigate();
  const startMutation = useStartListening();
  const submitMutation = useSubmitListeningAnswer();
  const completeMutation = useCompleteListening();

  // Phase
  const [phase, setPhase] = useState<Phase>('READY');

  // Session
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [totalRounds, setTotalRounds] = useState(10);
  const [score, setScore] = useState(0);

  // Current round
  const [round, setRound] = useState<RoundState | null>(null);

  // Input
  const [answer, setAnswer] = useState('');
  const inputRef = useRef<HTMLInputElement | null>(null);

  // Feedback
  const [feedback, setFeedback] = useState<FeedbackType>(null);
  const [feedbackData, setFeedbackData] = useState<ListeningAnswerResponse | null>(null);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState(0);

  // Combo
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);

  // Complete
  const [completeData, setCompleteData] = useState<ListeningCompleteResponse | null>(null);

  // Audio
  const { play: playAudio, isPlaying } = useAudioPlayer(round?.audioUrl ?? '');

  // Auto-play audio on new round
  const prevRoundRef = useRef<number | null>(null);
  useEffect(() => {
    if (round && round.roundNumber !== prevRoundRef.current && phase === 'PLAYING' && !feedback) {
      prevRoundRef.current = round.roundNumber;
      // Small delay for smooth transition
      const t = setTimeout(() => playAudio(), 400);
      return () => clearTimeout(t);
    }
  }, [round, phase, feedback, playAudio]);

  // Auto-focus input
  useEffect(() => {
    if (phase === 'PLAYING' && !feedback) {
      setTimeout(() => inputRef.current?.focus(), 400);
    }
  }, [phase, feedback, round?.roundNumber]);

  // Auto-advance countdown
  useEffect(() => {
    if (autoAdvanceTimer <= 0 || !feedback) return;
    const t = setInterval(() => {
      setAutoAdvanceTimer((v) => {
        if (v <= 1) {
          clearInterval(t);
          handleAdvance();
          return 0;
        }
        return v - 1;
      });
    }, 1000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoAdvanceTimer > 0, feedback]);

  // ─── Start ─────────────────────────────────────────────────────────────────

  const handleStart = () => {
    startMutation.mutate(undefined as void, {
      onSuccess: (res) => {
        const d = res.data as ListeningStartResponse;
        setSessionId(d.session_id);
        setTotalRounds(d.total_rounds);
        setRound({
          roundNumber: d.first_word.round_number,
          audioUrl: d.first_word.audio_url,
          hint: d.first_word.hint,
          maxAttempts: d.first_word.max_attempts,
          attemptsUsed: 0,
        });
        setPhase('PLAYING');
      },
    });
  };

  // ─── Submit Answer ─────────────────────────────────────────────────────────

  const handleSubmitAnswer = () => {
    if (!sessionId || !round || !answer.trim() || submitMutation.isPending) return;

    submitMutation.mutate(
      {
        sessionId,
        roundNumber: round.roundNumber,
        answer: answer.trim(),
      },
      {
        onSuccess: (res) => {
          const d = res.data as ListeningAnswerResponse;
          setFeedbackData(d);
          setCombo(d.combo);
          setMultiplier(d.multiplier);
          setScore((s) => s + d.score);

          if (d.is_correct) {
            setFeedback('correct');
            setAutoAdvanceTimer(2);
          } else if (d.attempts_remaining <= 0) {
            setFeedback('failed');
            setAutoAdvanceTimer(3);
          } else {
            // Wrong but has attempts left
            setFeedback('wrong');
            setRound((prev) =>
              prev
                ? {
                    ...prev,
                    hint: d.hint,
                    attemptsUsed: d.attempts_used,
                  }
                : prev,
            );
            // Auto-replay audio after brief pause
            setTimeout(() => {
              playAudio();
            }, 800);
            // Clear feedback after a brief moment, re-focus input
            setTimeout(() => {
              setFeedback(null);
              setFeedbackData(null);
              setAnswer('');
              inputRef.current?.focus();
            }, 1200);
          }
        },
        onError: () => {
          toast.error('Failed to submit answer.');
        },
      },
    );
  };

  // ─── Advance to next round / complete ──────────────────────────────────────

  const handleAdvance = useCallback(() => {
    setFeedback(null);
    setAutoAdvanceTimer(0);
    setAnswer('');

    if (feedbackData?.next_round) {
      setRound({
        roundNumber: feedbackData.next_round.round_number,
        audioUrl: feedbackData.next_round.audio_url,
        hint: feedbackData.next_round.hint,
        maxAttempts: feedbackData.next_round.max_attempts,
        attemptsUsed: 0,
      });
      setFeedbackData(null);
    } else {
      // Complete
      handleComplete();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [feedbackData]);

  const handleComplete = () => {
    if (!sessionId) return;
    completeMutation.mutate(sessionId, {
      onSuccess: (res) => {
        const d = res.data as ListeningCompleteResponse;
        setCompleteData(d);
        setPhase('COMPLETE');
        if (d.accuracy_pct >= 80) {
          fireConfetti();
        }
      },
    });
  };

  // ─── Key handler ───────────────────────────────────────────────────────────

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmitAnswer();
    }
  };

  // ─── RENDER: READY ────────────────────────────────────────────────────────

  if (phase === 'READY') {
    return (
      <PageTransition>
        <div className="mx-auto max-w-lg space-y-8 py-12">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', bounce: 0.4 }}
            className="text-center"
          >
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-500/10">
              <Headphones className="h-8 w-8 text-teal-500" />
            </div>
            <h1 className="text-2xl font-bold">Listening Challenge</h1>
            <p className="mt-2 text-muted-foreground">
              Listen carefully and type what you hear.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="border-border/50">
              <CardContent className="space-y-3 p-5">
                <p className="text-sm font-semibold">📋 Rules:</p>
                <ul className="space-y-1.5 text-sm text-muted-foreground">
                  <li>• You&apos;ll hear 10 words</li>
                  <li>• Type the word you hear</li>
                  <li>• 3 attempts per word</li>
                  <li>• Hints revealed after each wrong attempt</li>
                </ul>
                <div className="flex items-center gap-2 rounded-lg bg-yellow-500/10 p-2.5 text-sm">
                  <span>🎵</span>
                  <span className="text-yellow-700 dark:text-yellow-400">
                    Make sure your volume is on!
                  </span>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <div className="flex justify-center">
            <Button
              size="lg"
              disabled={startMutation.isPending}
              onClick={handleStart}
              className="gap-2"
            >
              {startMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Headphones className="h-4 w-4" />
              )}
              Start Challenge
            </Button>
          </div>
        </div>
      </PageTransition>
    );
  }

  // ─── RENDER: PLAYING ──────────────────────────────────────────────────────

  if (phase === 'PLAYING' && round) {
    const progress = (round.roundNumber / totalRounds) * 100;
    const attemptDots = Array.from({ length: round.maxAttempts });

    return (
      <PageTransition>
        <div className="mx-auto max-w-lg space-y-5 pb-8">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Headphones className="h-5 w-5 text-teal-500" />
              <span className="font-semibold">Listening Challenge</span>
            </div>
            <span className="text-sm text-muted-foreground">
              Word {round.roundNumber}/{totalRounds}
            </span>
          </div>

          <Progress value={progress} className="h-2" />

          {/* Combo + Score */}
          <div className="flex items-center justify-between">
            <ComboIndicator
              combo={combo}
              multiplier={multiplier}
              isActive={combo >= 2}
            />
            <span className="text-sm font-medium">Score: {score}</span>
          </div>

          {/* Audio Play Button */}
          <div className="flex justify-center py-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={playAudio}
              disabled={!round.audioUrl}
              className="group relative flex h-28 w-28 items-center justify-center rounded-2xl border-2 border-teal-500/30 bg-teal-500/10 transition-colors hover:border-teal-500/60 hover:bg-teal-500/20 disabled:cursor-not-allowed disabled:opacity-50 sm:h-32 sm:w-32"
              aria-label="Play audio"
            >
              {/* Pulse rings while playing */}
              <AnimatePresence>
                {isPlaying && (
                  <>
                    {[1, 2, 3].map((ring) => (
                      <motion.div
                        key={ring}
                        className="absolute inset-0 rounded-2xl border-2 border-teal-500/40"
                        initial={{ scale: 1, opacity: 0.5 }}
                        animate={{ scale: 1.3 + ring * 0.15, opacity: 0 }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          delay: ring * 0.3,
                        }}
                      />
                    ))}
                  </>
                )}
              </AnimatePresence>

              <div className="flex flex-col items-center gap-1.5">
                <motion.div
                  animate={isPlaying ? { scale: [1, 1.1, 1] } : {}}
                  transition={{ repeat: Infinity, duration: 0.8 }}
                >
                  <Volume2 className="h-10 w-10 text-teal-500 sm:h-12 sm:w-12" />
                </motion.div>
                <span className="text-xs text-muted-foreground">
                  {isPlaying ? 'Playing...' : 'Click to play'}
                </span>
              </div>
            </motion.button>
          </div>

          {/* Hint */}
          <div className="text-center">
            <p className="mb-2 text-sm text-muted-foreground">Hint:</p>
            <p className="font-mono text-2xl tracking-[0.3em]">
              {round.hint.split('').map((c, i) => (
                <motion.span
                  key={`${round.roundNumber}-${i}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.05 }}
                  className={
                    c !== '_' && c !== ' '
                      ? 'font-bold text-primary'
                      : 'text-muted-foreground'
                  }
                >
                  {c}
                </motion.span>
              ))}
            </p>
          </div>

          {/* Attempt Dots */}
          <div className="flex items-center justify-center gap-2">
            <span className="text-xs text-muted-foreground">Attempts:</span>
            {attemptDots.map((_, i) => {
              const isUsed = i < round.attemptsUsed;
              return (
                <motion.div
                  key={i}
                  initial={isUsed ? { scale: 0.5 } : {}}
                  animate={isUsed ? { scale: 1 } : {}}
                  className={`h-3 w-3 rounded-full transition-colors ${
                    isUsed
                      ? 'bg-red-500'
                      : 'border border-muted-foreground/40 bg-transparent'
                  }`}
                />
              );
            })}
            <span className="text-xs text-muted-foreground">
              ({round.attemptsUsed}/{round.maxAttempts} used)
            </span>
          </div>

          {/* Feedback Overlay */}
          <AnimatePresence>
            {feedback === 'correct' && feedbackData && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
              >
                <Card className="border-green-500/30 bg-green-500/5">
                  <CardContent className="space-y-3 p-5 text-center">
                    <motion.span
                      initial={{ scale: 0 }}
                      animate={{ scale: [1.3, 1] }}
                      className="inline-block text-4xl"
                    >
                      ✅
                    </motion.span>
                    <p className="text-lg font-bold text-green-600 dark:text-green-400">
                      Correct!
                    </p>
                    <p className="text-xl font-semibold text-primary">
                      &quot;{feedbackData.correct_answer}&quot;
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Score: +{feedbackData.score} ⭐ ({getAttemptLabel(feedbackData.attempts_used)})
                    </p>
                    <div className="flex items-center justify-center gap-2">
                      <span className="text-sm">+{feedbackData.xp_earned} XP</span>
                      <ComboIndicator
                        combo={feedbackData.combo}
                        multiplier={feedbackData.multiplier}
                        isActive={feedbackData.combo >= 2}
                      />
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {feedback === 'wrong' && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: [10, -8, 6, -4, 0] }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4 }}
              >
                <Card className="border-red-500/30 bg-red-500/5">
                  <CardContent className="space-y-2 p-4 text-center">
                    <span className="inline-block text-2xl">❌</span>
                    <p className="text-sm font-semibold text-red-600 dark:text-red-400">
                      Try again!
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {feedback === 'failed' && feedbackData && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
              >
                <Card className="border-red-500/30 bg-red-500/5">
                  <CardContent className="space-y-3 p-5 text-center">
                    <span className="text-2xl">😔</span>
                    <p className="text-sm text-muted-foreground">The word was:</p>
                    <motion.p
                      className="text-2xl font-bold text-primary"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    >
                      &quot;{feedbackData.correct_answer}&quot;
                    </motion.p>
                    <p className="text-sm text-muted-foreground">
                      Score: 0 · Combo lost! 💔
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Input (hidden during correct/failed feedback) */}
          {feedback !== 'correct' && feedback !== 'failed' && (
            <div className="space-y-3">
              <div className="relative">
                <input
                  ref={inputRef}
                  type="text"
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type what you hear..."
                  disabled={submitMutation.isPending}
                  className={`w-full rounded-lg border bg-background p-3 text-center text-2xl focus:outline-none focus:ring-1 focus:ring-primary dark:bg-muted/30 ${
                    feedback === 'wrong'
                      ? 'animate-pulse border-red-500'
                      : 'border-border focus:border-primary'
                  }`}
                  aria-label="Type the word you hear"
                  autoComplete="off"
                  autoCorrect="off"
                  spellCheck={false}
                />
              </div>

              <Button
                onClick={handleSubmitAnswer}
                disabled={!answer.trim() || submitMutation.isPending}
                className="w-full gap-2"
              >
                {submitMutation.isPending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <>
                    Check Answer
                    <Check className="h-4 w-4" />
                  </>
                )}
              </Button>
            </div>
          )}
        </div>
      </PageTransition>
    );
  }

  // ─── RENDER: COMPLETE ─────────────────────────────────────────────────────

  if (phase === 'COMPLETE' && completeData) {
    const stars = getStars(completeData.accuracy_pct);

    return (
      <PageTransition>
        <div className="mx-auto max-w-lg space-y-6 py-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', bounce: 0.4 }}
            className="text-center"
          >
            <div className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-500/10">
              <Headphones className="h-8 w-8 text-teal-500" />
            </div>
            <h1 className="text-2xl font-bold">Challenge Complete!</h1>
          </motion.div>

          {/* Score + Accuracy */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center space-y-2"
          >
            <p className="text-4xl font-bold">
              {completeData.total_score}/{completeData.max_score}
            </p>
            <p className="text-lg text-muted-foreground">
              Accuracy: {completeData.accuracy_pct}%
            </p>
            <div className="flex justify-center gap-1">
              {Array.from({ length: 5 }).map((_, i) => (
                <span
                  key={i}
                  className={`text-xl ${i < stars ? '' : 'opacity-20'}`}
                >
                  ⭐
                </span>
              ))}
            </div>
          </motion.div>

          {/* Results List */}
          <Card className="border-border/50">
            <CardContent className="space-y-1.5 p-5">
              <p className="mb-2 text-sm font-semibold">📊 Results</p>
              {completeData.rounds.map((r, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className={`flex items-center justify-between rounded-lg px-3 py-2 ${
                    r.is_correct
                      ? 'bg-green-500/5'
                      : 'bg-red-500/5'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span>{r.is_correct ? '✅' : '❌'}</span>
                    <span className="text-sm font-medium">{r.word}</span>
                  </div>
                  <div className="text-right text-xs text-muted-foreground">
                    <span>
                      {r.is_correct
                        ? `${getAttemptLabel(r.attempts_used)} (${r.score})`
                        : `failed (${r.score})`}
                    </span>
                  </div>
                </motion.div>
              ))}
            </CardContent>
          </Card>

          {/* XP */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-center"
          >
            <div className="inline-flex items-center gap-2 rounded-lg bg-primary/5 px-4 py-2">
              <span className="text-lg font-bold text-primary">
                +{completeData.xp_earned} XP earned ⭐
              </span>
            </div>
          </motion.div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => {
                setPhase('READY');
                setSessionId(null);
                setRound(null);
                setCompleteData(null);
                setScore(0);
                setCombo(0);
                setMultiplier(1);
                setAnswer('');
                prevRoundRef.current = null;
              }}
            >
              Play Again
            </Button>
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => navigate('/games')}
            >
              Other Games
            </Button>
            <Button className="flex-1" onClick={() => navigate('/')}>
              Dashboard
            </Button>
          </div>
        </div>
      </PageTransition>
    );
  }

  // Loading fallback
  return (
    <PageTransition>
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    </PageTransition>
  );
}
