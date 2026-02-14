import { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { PageTransition } from '@/components/animations/PageTransition';
import { ComboIndicator } from '@/features/review/components/ComboIndicator';
import type { StoryRoundResult } from '@/types';
import { BookOpen, formatTime, type StorySegment } from './storyBuilderHelpers';

interface StoryPlayingProps {
  currentRound: number;
  totalRounds: number;
  targetWords: string[];
  allTargetWords: string[];
  segments: StorySegment[];
  userText: string;
  onUserTextChange: (text: string) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
  timeElapsed: number;
  showResult: boolean;
  roundResult: StoryRoundResult | null;
  roundXp: number;
  combo: number;
  multiplier: number;
  autoAdvanceTimer: number;
  onNextRound: () => void;
}

export function StoryPlaying({
  currentRound,
  totalRounds,
  targetWords,
  allTargetWords,
  segments,
  userText,
  onUserTextChange,
  onSubmit,
  isSubmitting,
  timeElapsed,
  showResult,
  roundResult,
  roundXp,
  combo,
  multiplier,
  autoAdvanceTimer,
  onNextRound,
}: StoryPlayingProps) {
  const storyEndRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // Auto-scroll
  useEffect(() => {
    storyEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [segments]);

  // Auto-focus textarea
  useEffect(() => {
    if (!showResult) {
      setTimeout(() => textareaRef.current?.focus(), 300);
    }
  }, [showResult, currentRound]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onSubmit();
    }
  };

  const progress = (currentRound / totalRounds) * 100;

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-4 pb-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-purple-500" />
            <span className="font-semibold">Story Builder</span>
          </div>
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <span>
              Round {currentRound}/{totalRounds}
            </span>
            <span>⏱️ {formatTime(timeElapsed)}</span>
          </div>
        </div>

        <Progress value={progress} className="h-2" />

        {/* Target Word Badge */}
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">🎯 Use this word:</span>
          {targetWords.map((w) => (
            <Badge
              key={w}
              variant="secondary"
              className="animate-pulse border-yellow-500/30 bg-yellow-500/15 text-yellow-700 dark:text-yellow-400"
            >
              &quot;{w}&quot;
            </Badge>
          ))}
        </div>

        {/* Story Display */}
        <Card className="border-border/50">
          <CardContent className="max-h-72 overflow-y-auto p-4">
            <p className="mb-3 text-xs font-medium uppercase tracking-wider text-muted-foreground">
              📖 Story so far
            </p>
            <div className="space-y-3">
              <AnimatePresence mode="popLayout">
                {segments.map((seg, i) => (
                  <motion.div
                    key={`${seg.type}-${seg.roundNumber}-${i}`}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4 }}
                    className={`rounded-lg p-3 text-sm leading-relaxed ${
                      seg.type === 'ai'
                        ? 'bg-muted dark:bg-muted/50'
                        : 'ml-4 bg-primary/10'
                    }`}
                  >
                    <span className="mr-1.5 text-xs">
                      {seg.type === 'ai' ? '🤖' : '👤'}
                    </span>
                    {seg.text}
                  </motion.div>
                ))}
              </AnimatePresence>
              <div ref={storyEndRef} />
            </div>
          </CardContent>
        </Card>

        {/* Round Result Overlay */}
        <AnimatePresence>
          {showResult && roundResult && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="border-border/50">
                <CardContent className="space-y-4 p-5">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">Round {currentRound} Result</h3>
                    <div className="flex items-center gap-1.5">
                      <span className="text-lg font-bold">
                        {roundResult.score}/20
                      </span>
                      <span>⭐</span>
                    </div>
                  </div>

                  {/* Word usage */}
                  <div
                    className={`flex items-center gap-2 rounded-lg p-2 text-sm ${
                      roundResult.is_correct_usage
                        ? 'bg-green-500/10 text-green-700 dark:text-green-400'
                        : 'bg-red-500/10 text-red-700 dark:text-red-400'
                    }`}
                  >
                    {roundResult.is_correct_usage ? (
                      <>
                        <motion.span
                          initial={{ scale: 0 }}
                          animate={{ scale: [1.3, 1] }}
                          transition={{ type: 'spring' }}
                        >
                          ✅
                        </motion.span>
                        Used &quot;{targetWords[0]}&quot; correctly!
                      </>
                    ) : (
                      <>
                        <motion.span
                          initial={{ scale: 0 }}
                          animate={{ scale: [1.3, 1] }}
                          transition={{ type: 'spring' }}
                        >
                          ❌
                        </motion.span>
                        You didn&apos;t use &quot;{targetWords[0]}&quot;
                      </>
                    )}
                  </div>

                  {/* Grammar Corrections */}
                  {roundResult.grammar_corrections.length > 0 ? (
                    <div className="space-y-2">
                      <p className="text-sm font-medium">📝 Grammar:</p>
                      {roundResult.grammar_corrections.map((c, idx) => (
                        <motion.div
                          key={idx}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                          className="rounded-lg border bg-muted/50 p-2.5 text-sm"
                        >
                          <p className="text-red-500 line-through dark:text-red-400">
                            ❌ &quot;{c.original}&quot;
                          </p>
                          <p className="text-green-600 dark:text-green-400">
                            ✅ &quot;{c.corrected}&quot;
                          </p>
                          <p className="mt-1 text-xs text-muted-foreground">
                            💡 {c.explanation}
                          </p>
                        </motion.div>
                      ))}
                    </div>
                  ) : (
                    <div className="rounded-lg bg-green-500/10 p-2 text-sm text-green-700 dark:text-green-400">
                      ✅ Great grammar!
                    </div>
                  )}

                  {/* Feedback */}
                  {roundResult.feedback && (
                    <div className="rounded-lg bg-primary/5 p-2.5 text-sm italic text-muted-foreground">
                      💬 &quot;{roundResult.feedback}&quot;
                    </div>
                  )}

                  {/* XP + Combo */}
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">+{roundXp} XP ⭐</span>
                    <ComboIndicator
                      combo={combo}
                      multiplier={multiplier}
                      isActive={combo >= 2}
                    />
                  </div>

                  {/* Auto advance */}
                  <div className="space-y-2">
                    <Button onClick={onNextRound} className="w-full gap-2">
                      {currentRound >= totalRounds ? 'View Results' : 'Next Round'}
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                    {autoAdvanceTimer > 0 && (
                      <div className="space-y-1">
                        <p className="text-center text-xs text-muted-foreground">
                          Auto-advancing in {autoAdvanceTimer}s...
                        </p>
                        <Progress
                          value={(autoAdvanceTimer / 5) * 100}
                          className="h-1"
                        />
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Text Input (hidden during result) */}
        {!showResult && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-3"
          >
            <p className="text-sm font-medium">✍️ Continue the story:</p>
            <textarea
              ref={textareaRef}
              value={userText}
              onChange={(e) => onUserTextChange(e.target.value)}
              onKeyDown={handleKeyDown}
              maxLength={500}
              rows={4}
              placeholder={`Write your continuation here... Use the word "${targetWords[0] ?? ''}" naturally.`}
              className="w-full resize-none rounded-lg border bg-background p-3 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary dark:bg-muted/30"
              aria-label="Story continuation input"
            />
            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span
                className={
                  userText.length < 10 && userText.length > 0 ? 'text-red-500' : ''
                }
              >
                {userText.length}/500 characters{' '}
                {userText.length < 10 && userText.length > 0 && '(min 10)'}
              </span>
              <span className="text-muted-foreground/60">Ctrl+Enter to submit</span>
            </div>

            <Button
              onClick={onSubmit}
              disabled={userText.trim().length < 10 || isSubmitting}
              className="w-full gap-2"
            >
              {isSubmitting ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  Submit Round
                  <ChevronRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </motion.div>
        )}

        {/* All target words hint */}
        {allTargetWords.length > 0 && (
          <p className="text-xs text-muted-foreground">
            💡 All target words:{' '}
            {allTargetWords.map((w, i) => (
              <span key={w}>
                {i > 0 && ', '}
                <span
                  className={
                    targetWords.includes(w) ? 'font-semibold text-primary' : ''
                  }
                >
                  {w}
                </span>
              </span>
            ))}
          </p>
        )}

        {/* Combo */}
        {combo >= 2 && !showResult && (
          <div className="flex justify-center">
            <ComboIndicator combo={combo} multiplier={multiplier} isActive={true} />
          </div>
        )}
      </div>
    </PageTransition>
  );
}
