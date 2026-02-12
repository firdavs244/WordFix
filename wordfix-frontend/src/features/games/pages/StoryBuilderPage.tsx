import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BookOpen,
  Check,
  ChevronRight,
  Copy,
  Loader2,
  Sparkles,
  Sword,
  Search,
  Laugh,
  Rocket,
  Home,
  Plane,
  Wand2,
  Ghost,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { PageTransition } from '@/components/animations/PageTransition';
import { ComboIndicator } from '@/features/review/components/ComboIndicator';
import {
  useStartStoryBuilder,
  useSubmitStoryRound,
  useCompleteStoryBuilder,
} from '../hooks/useGames';
import { toast } from 'sonner';
import type {
  StoryStartResponse,
  StorySubmitResponse,
  StoryCompleteResponse,
  StoryRoundResult,
} from '@/types';

// ─── Types ─────────────────────────────────────────────────────────────────────

type Phase = 'GENRE_SELECT' | 'PLAYING' | 'COMPLETE';

interface StorySegment {
  type: 'ai' | 'user';
  text: string;
  roundNumber: number;
}

// ─── Genre Data ────────────────────────────────────────────────────────────────

const GENRES = [
  { key: 'adventure', label: 'Adventure', icon: Sword, emoji: '🗡️' },
  { key: 'mystery', label: 'Mystery', icon: Search, emoji: '🔍' },
  { key: 'comedy', label: 'Comedy', icon: Laugh, emoji: '😂' },
  { key: 'sci-fi', label: 'Sci-Fi', icon: Rocket, emoji: '🚀' },
  { key: 'daily_life', label: 'Daily Life', icon: Home, emoji: '🏠' },
  { key: 'travel', label: 'Travel', icon: Plane, emoji: '✈️' },
  { key: 'fantasy', label: 'Fantasy', icon: Wand2, emoji: '🧙' },
  { key: 'thriller', label: 'Thriller', icon: Ghost, emoji: '👻' },
] as const;

// ─── Helpers ───────────────────────────────────────────────────────────────────

function getStars(score: number, maxScore: number) {
  const pct = maxScore > 0 ? (score / maxScore) * 100 : 0;
  if (pct >= 90) return 5;
  if (pct >= 75) return 4;
  if (pct >= 60) return 3;
  if (pct >= 40) return 2;
  if (pct >= 20) return 1;
  return 0;
}

function getRoundStars(score: number) {
  if (score >= 18) return 5;
  if (score >= 15) return 4;
  if (score >= 12) return 3;
  if (score >= 8) return 2;
  if (score >= 4) return 1;
  return 0;
}

function fireConfetti() {
  import('canvas-confetti').then((mod) => {
    const confetti = mod.default;
    confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
  }).catch(() => {});
}

// ─── Main Component ────────────────────────────────────────────────────────────

export function StoryBuilderPage() {
  const navigate = useNavigate();
  const startMutation = useStartStoryBuilder();
  const submitMutation = useSubmitStoryRound();
  const completeMutation = useCompleteStoryBuilder();

  // Phase
  const [phase, setPhase] = useState<Phase>('GENRE_SELECT');

  // Genre
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  // Session
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [totalRounds, setTotalRounds] = useState(5);
  const [currentRound, setCurrentRound] = useState(1);
  const [targetWords, setTargetWords] = useState<string[]>([]);
  const [allTargetWords, setAllTargetWords] = useState<string[]>([]);

  // Story segments
  const [segments, setSegments] = useState<StorySegment[]>([]);

  // User input
  const [userText, setUserText] = useState('');

  // Timer
  const [timeElapsed, setTimeElapsed] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Round result
  const [showResult, setShowResult] = useState(false);
  const [roundResult, setRoundResult] = useState<StoryRoundResult | null>(null);
  const [roundXp, setRoundXp] = useState(0);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState(0);

  // Combo
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);

  // Complete
  const [completeData, setCompleteData] = useState<StoryCompleteResponse | null>(null);

  // Refs
  const storyEndRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // Timer
  useEffect(() => {
    if (phase === 'PLAYING' && !showResult) {
      timerRef.current = setInterval(() => {
        setTimeElapsed((t) => t + 1);
      }, 1000);
      return () => {
        if (timerRef.current) clearInterval(timerRef.current);
      };
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [phase, showResult]);

  // Auto-scroll
  useEffect(() => {
    storyEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [segments]);

  // Auto-focus textarea
  useEffect(() => {
    if (phase === 'PLAYING' && !showResult) {
      setTimeout(() => textareaRef.current?.focus(), 300);
    }
  }, [phase, showResult, currentRound]);

  // Auto-advance countdown
  useEffect(() => {
    if (!showResult || autoAdvanceTimer <= 0) return;
    const t = setInterval(() => {
      setAutoAdvanceTimer((v) => {
        if (v <= 1) {
          clearInterval(t);
          handleNextRound();
          return 0;
        }
        return v - 1;
      });
    }, 1000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showResult, autoAdvanceTimer > 0]);

  // Format time
  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  // ─── Start Game ────────────────────────────────────────────────────────────

  const handleStart = () => {
    if (!selectedGenre) return;
    startMutation.mutate(selectedGenre, {
      onSuccess: (res) => {
        const d = res.data as StoryStartResponse;
        setSessionId(d.session_id);
        setTotalRounds(d.total_rounds);
        setCurrentRound(d.current_round);
        setTargetWords(d.target_words);
        setAllTargetWords(d.all_target_words);
        setSegments([{ type: 'ai', text: d.ai_text, roundNumber: 1 }]);
        setPhase('PLAYING');
      },
    });
  };

  // ─── Submit Round ──────────────────────────────────────────────────────────

  const handleSubmit = () => {
    if (!sessionId || userText.trim().length < 10 || submitMutation.isPending) return;
    submitMutation.mutate(
      { sessionId, userText: userText.trim() },
      {
        onSuccess: (res) => {
          const d = res.data as StorySubmitResponse;
          setSegments((prev) => [
            ...prev,
            { type: 'user', text: userText.trim(), roundNumber: currentRound },
          ]);
          setUserText('');
          setRoundResult(d.round_result);
          setRoundXp(d.xp_earned);
          setCombo(d.combo);
          setMultiplier(d.multiplier);
          setShowResult(true);

          if (d.next_round) {
            // Next round will be triggered by handleNextRound
            setAutoAdvanceTimer(5);
          } else {
            // Last round — auto complete after showing result
            setAutoAdvanceTimer(5);
          }
        },
        onError: () => {
          toast.error('Failed to submit your text. Try again.');
        },
      },
    );
  };

  // ─── Next Round / Complete ─────────────────────────────────────────────────

  const handleNextRound = useCallback(() => {
    setShowResult(false);
    setAutoAdvanceTimer(0);

    // Check last submit result to decide next
    if (submitMutation.data) {
      const d = submitMutation.data.data as StorySubmitResponse;
      if (d.next_round) {
        setSegments((prev) => [
          ...prev,
          { type: 'ai', text: d.next_round!.ai_text, roundNumber: d.next_round!.round_number },
        ]);
        setCurrentRound(d.next_round!.round_number);
        setTargetWords(d.next_round!.target_words);
      } else {
        // Complete
        handleComplete();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [submitMutation.data]);

  const handleComplete = () => {
    if (!sessionId) return;
    completeMutation.mutate(sessionId, {
      onSuccess: (res) => {
        const d = res.data as StoryCompleteResponse;
        setCompleteData(d);
        setPhase('COMPLETE');
        if (d.max_score > 0 && (d.total_score / d.max_score) * 100 >= 80) {
          fireConfetti();
        }
      },
    });
  };

  // ─── Copy Story ────────────────────────────────────────────────────────────

  const handleCopyStory = () => {
    if (completeData?.full_story) {
      navigator.clipboard.writeText(completeData.full_story).then(() => {
        toast.success('Story copied to clipboard!');
      });
    }
  };

  // ─── Keyboard ──────────────────────────────────────────────────────────────

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleSubmit();
    }
  };

  // ─── RENDER: GENRE SELECT ─────────────────────────────────────────────────

  if (phase === 'GENRE_SELECT') {
    return (
      <PageTransition>
        <div className="mx-auto max-w-2xl space-y-8 py-8">
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', bounce: 0.4 }}
              className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-500/10"
            >
              <BookOpen className="h-8 w-8 text-purple-500" />
            </motion.div>
            <h1 className="text-2xl font-bold">Story Builder</h1>
            <p className="mt-2 text-muted-foreground">
              Choose a genre for your story
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {GENRES.map((genre, i) => (
              <motion.button
                key={genre.key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                onClick={() => setSelectedGenre(genre.key)}
                className={`relative flex flex-col items-center gap-2 rounded-xl border-2 p-4 transition-all hover:scale-105 hover:shadow-md ${
                  selectedGenre === genre.key
                    ? 'border-primary bg-primary/10 shadow-md'
                    : 'border-border hover:border-primary/50'
                }`}
              >
                {selectedGenre === genre.key && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -right-1.5 -top-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-primary-foreground"
                  >
                    <Check className="h-3 w-3" />
                  </motion.div>
                )}
                <span className="text-2xl">{genre.emoji}</span>
                <span className="text-sm font-medium">{genre.label}</span>
              </motion.button>
            ))}
          </div>

          <div className="flex justify-center">
            <Button
              size="lg"
              disabled={!selectedGenre || startMutation.isPending}
              onClick={handleStart}
              className="gap-2"
            >
              {startMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Sparkles className="h-4 w-4" />
              )}
              Start Story
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </PageTransition>
    );
  }

  // ─── RENDER: PLAYING ──────────────────────────────────────────────────────

  if (phase === 'PLAYING') {
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
                      <span className="text-sm font-medium">
                        +{roundXp} XP ⭐
                      </span>
                      <ComboIndicator
                        combo={combo}
                        multiplier={multiplier}
                        isActive={combo >= 2}
                      />
                    </div>

                    {/* Auto advance */}
                    <div className="space-y-2">
                      <Button
                        onClick={handleNextRound}
                        className="w-full gap-2"
                      >
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
                onChange={(e) => setUserText(e.target.value)}
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
                    userText.length < 10 && userText.length > 0
                      ? 'text-red-500'
                      : ''
                  }
                >
                  {userText.length}/500 characters{' '}
                  {userText.length < 10 && userText.length > 0 && '(min 10)'}
                </span>
                <span className="text-muted-foreground/60">Ctrl+Enter to submit</span>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={
                  userText.trim().length < 10 || submitMutation.isPending
                }
                className="w-full gap-2"
              >
                {submitMutation.isPending ? (
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
              <ComboIndicator
                combo={combo}
                multiplier={multiplier}
                isActive={true}
              />
            </div>
          )}
        </div>
      </PageTransition>
    );
  }

  // ─── RENDER: COMPLETE ─────────────────────────────────────────────────────

  if (phase === 'COMPLETE' && completeData) {
    const totalStars = getStars(completeData.total_score, completeData.max_score);

    return (
      <PageTransition>
        <div className="mx-auto max-w-2xl space-y-6 py-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', bounce: 0.4 }}
            className="text-center"
          >
            <div className="mx-auto mb-3 flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-500/10">
              <BookOpen className="h-8 w-8 text-purple-500" />
            </div>
            <h1 className="text-2xl font-bold">Story Complete!</h1>
          </motion.div>

          {/* Score */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center"
          >
            <p className="text-4xl font-bold">
              {completeData.total_score}/{completeData.max_score}
            </p>
            <div className="mt-2 flex justify-center gap-1">
              {Array.from({ length: 5 }).map((_, i) => (
                <span
                  key={i}
                  className={`text-xl ${i < totalStars ? '' : 'opacity-20'}`}
                >
                  ⭐
                </span>
              ))}
            </div>
          </motion.div>

          {/* Round Scores */}
          <Card className="border-border/50">
            <CardContent className="space-y-2 p-5">
              <p className="text-sm font-semibold">📊 Round Scores</p>
              {completeData.rounds.map((r, i) => {
                const stars = getRoundStars(r.score);
                return (
                  <motion.div
                    key={r.round_number}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 }}
                    className="flex items-center justify-between rounded-lg border px-3 py-2"
                  >
                    <span className="text-sm font-medium">
                      Round {r.round_number}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold">{r.score}/20</span>
                      <span className="text-xs">
                        {Array.from({ length: stars }).map((_, si) => (
                          <span key={si}>⭐</span>
                        ))}
                      </span>
                      {r.score === 20 && (
                        <span className="text-xs font-medium text-green-600">
                          🎯 Perfect!
                        </span>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </CardContent>
          </Card>

          {/* Full Story */}
          <Card className="border-border/50">
            <CardContent className="p-5">
              <div className="mb-3 flex items-center justify-between">
                <p className="text-sm font-semibold">📖 Your Full Story</p>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCopyStory}
                  className="gap-1.5 text-xs"
                >
                  <Copy className="h-3.5 w-3.5" />
                  Copy Story
                </Button>
              </div>
              <div className="max-h-64 overflow-y-auto rounded-lg bg-muted/50 p-4 text-sm leading-relaxed dark:bg-muted/30">
                {completeData.full_story}
              </div>
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
                setPhase('GENRE_SELECT');
                setSessionId(null);
                setSegments([]);
                setCompleteData(null);
                setTimeElapsed(0);
                setCombo(0);
                setMultiplier(1);
                setCurrentRound(1);
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
