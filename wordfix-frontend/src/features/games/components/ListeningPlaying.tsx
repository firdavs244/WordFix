import { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Headphones, Volume2, Loader2, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { PageTransition } from '@/components/animations/PageTransition';
import { ComboIndicator } from '@/features/review/components/ComboIndicator';
import type { ListeningAnswerResponse } from '@/types';
import {
  type RoundState,
  type FeedbackType,
  useAudioPlayer,
  getAttemptLabel,
} from './listeningHelpers';

interface ListeningPlayingProps {
  round: RoundState;
  totalRounds: number;
  score: number;
  answer: string;
  onAnswerChange: (value: string) => void;
  onSubmitAnswer: () => void;
  isSubmitting: boolean;
  feedback: FeedbackType;
  feedbackData: ListeningAnswerResponse | null;
  combo: number;
  multiplier: number;
}

export function ListeningPlaying({
  round,
  totalRounds,
  score,
  answer,
  onAnswerChange,
  onSubmitAnswer,
  isSubmitting,
  feedback,
  feedbackData,
  combo,
  multiplier,
}: ListeningPlayingProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { play: playAudio, isPlaying } = useAudioPlayer(round.audioUrl);

  // Auto-focus input
  useEffect(() => {
    if (!feedback) {
      setTimeout(() => inputRef.current?.focus(), 400);
    }
  }, [feedback, round.roundNumber]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      onSubmitAnswer();
    }
  };

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
                    Score: +{feedbackData.score} ⭐ (
                    {getAttemptLabel(feedbackData.attempts_used)})
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
                onChange={(e) => onAnswerChange(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type what you hear..."
                disabled={isSubmitting}
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
              onClick={onSubmitAnswer}
              disabled={!answer.trim() || isSubmitting}
              className="w-full gap-2"
            >
              {isSubmitting ? (
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
