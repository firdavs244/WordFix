import { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Headphones, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
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
import {
  type ListeningPhase,
  type FeedbackType,
  type RoundState,
  useAudioPlayer,
  fireConfetti,
} from '../components/listeningHelpers';
import { ListeningPlaying } from '../components/ListeningPlaying';
import { ListeningComplete } from '../components/ListeningComplete';

// ─── Main Component ────────────────────────────────────────────────────────────

export function ListeningPage() {
  const startMutation = useStartListening();
  const submitMutation = useSubmitListeningAnswer();
  const completeMutation = useCompleteListening();

  const [phase, setPhase] = useState<ListeningPhase>('READY');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [totalRounds, setTotalRounds] = useState(10);
  const [score, setScore] = useState(0);
  const [round, setRound] = useState<RoundState | null>(null);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<FeedbackType>(null);
  const [feedbackData, setFeedbackData] = useState<ListeningAnswerResponse | null>(null);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState(0);
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);
  const [completeData, setCompleteData] = useState<ListeningCompleteResponse | null>(null);

  const { play: playAudio } = useAudioPlayer(round?.audioUrl ?? '');
  const prevRoundRef = useRef<number | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  // Auto-play audio on new round
  useEffect(() => {
    if (round && round.roundNumber !== prevRoundRef.current && phase === 'PLAYING' && !feedback) {
      prevRoundRef.current = round.roundNumber;
      const t = setTimeout(() => playAudio(), 400);
      return () => clearTimeout(t);
    }
  }, [round, phase, feedback, playAudio]);

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

  const handleSubmitAnswer = () => {
    if (!sessionId || !round || !answer.trim() || submitMutation.isPending) return;
    submitMutation.mutate(
      { sessionId, roundNumber: round.roundNumber, answer: answer.trim() },
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
            setFeedback('wrong');
            setRound((prev) =>
              prev ? { ...prev, hint: d.hint, attemptsUsed: d.attempts_used } : prev,
            );
            setTimeout(() => playAudio(), 800);
            setTimeout(() => {
              setFeedback(null);
              setFeedbackData(null);
              setAnswer('');
              inputRef.current?.focus();
            }, 1200);
          }
        },
        onError: () => toast.error('Failed to submit answer.'),
      },
    );
  };

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
        if (d.accuracy_pct >= 80) fireConfetti();
      },
    });
  };

  const handlePlayAgain = () => {
    setPhase('READY');
    setSessionId(null);
    setRound(null);
    setCompleteData(null);
    setScore(0);
    setCombo(0);
    setMultiplier(1);
    setAnswer('');
    prevRoundRef.current = null;
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
    return (
      <ListeningPlaying
        round={round}
        totalRounds={totalRounds}
        score={score}
        answer={answer}
        onAnswerChange={setAnswer}
        onSubmitAnswer={handleSubmitAnswer}
        isSubmitting={submitMutation.isPending}
        feedback={feedback}
        feedbackData={feedbackData}
        combo={combo}
        multiplier={multiplier}
      />
    );
  }

  // ─── RENDER: COMPLETE ─────────────────────────────────────────────────────

  if (phase === 'COMPLETE' && completeData) {
    return (
      <ListeningComplete completeData={completeData} onPlayAgain={handlePlayAgain} />
    );
  }

  return (
    <PageTransition>
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    </PageTransition>
  );
}
