import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Check, X, Loader2, Trophy, HelpCircle } from 'lucide-react';
import { toast } from 'sonner';
import type { AxiosResponse } from 'axios';
import PageTransition from '@/components/shared/PageTransition';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import { cn } from '@/lib/utils';
import type {
  IrregularVerbsStartResponse,
  IrregularVerbAnswerResponse,
  IrregularVerbsCompleteResponse,
} from '@/types/game';

type Phase = 'loading' | 'playing' | 'result' | 'complete';

export default function IrregularVerbsPage() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<Phase>('loading');
  const [sessionId, setSessionId] = useState('');
  const [rounds, setRounds] = useState<IrregularVerbsStartResponse['rounds']>([]);
  const [tier, setTier] = useState('');
  const [currentRound, setCurrentRound] = useState(0);
  const [pastSimple, setPastSimple] = useState('');
  const [pastParticiple, setPastParticiple] = useState('');
  const [lastResult, setLastResult] = useState<IrregularVerbAnswerResponse | null>(null);
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [completeData, setCompleteData] = useState<IrregularVerbsCompleteResponse | null>(null);

  // Start game
  const startMutation = useMutation({
    mutationFn: () => apiClient.post(API_ENDPOINTS.GAMES.IRREGULAR_VERBS_START),
    onSuccess: (res: AxiosResponse) => {
      const data = res.data.data;
      setSessionId(data.session_id);
      setRounds(data.rounds);
      setTier(data.tier);
      setPhase('playing');
    },
    onError: () => toast.error('Failed to start game'),
  });

  // Submit answer
  const answerMutation = useMutation({
    mutationFn: () =>
      apiClient.post(API_ENDPOINTS.GAMES.IRREGULAR_VERBS_ANSWER, {
        session_id: sessionId,
        round_number: rounds[currentRound].round_number,
        past_simple: pastSimple,
        past_participle: pastParticiple,
      }),
    onSuccess: (res: AxiosResponse) => {
      const data = res.data.data as IrregularVerbAnswerResponse;
      setLastResult(data);
      setScore((s) => s + data.score);
      setCombo(data.combo);
      setPhase('result');
    },
  });

  // Complete game
  const completeMutation = useMutation({
    mutationFn: () =>
      apiClient.post(API_ENDPOINTS.GAMES.IRREGULAR_VERBS_COMPLETE, { session_id: sessionId }),
    onSuccess: (res: AxiosResponse) => {
      setCompleteData(res.data.data);
      setPhase('complete');
    },
  });

  const handleStart = () => startMutation.mutate();

  const handleSubmit = () => {
    if (!pastSimple.trim() || !pastParticiple.trim()) {
      toast.error('Fill in both fields');
      return;
    }
    answerMutation.mutate();
  };

  const shouldAdvance = lastResult && (
    (lastResult.past_simple_correct && lastResult.past_participle_correct) ||
    lastResult.attempts_remaining === 0
  );

  const handleNext = useCallback(() => {
    if (!shouldAdvance && lastResult) {
      // Retry — keep inputs but allow re-submit
      setPastSimple('');
      setPastParticiple('');
      setLastResult(null);
      setPhase('playing');
      return;
    }

    if (currentRound + 1 < rounds.length) {
      setCurrentRound((r) => r + 1);
      setPastSimple('');
      setPastParticiple('');
      setLastResult(null);
      setPhase('playing');
    } else {
      completeMutation.mutate();
    }
  }, [currentRound, rounds.length, completeMutation, shouldAdvance, lastResult]);

  const round = rounds[currentRound];

  return (
    <PageTransition>
      <div className="mx-auto max-w-lg space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/games')} className="rounded-lg p-2 hover:bg-muted/40">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="font-heading text-xl font-bold">Irregular Verbs</h1>
          {tier && (
            <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
              {tier}
            </span>
          )}
        </div>

        {/* Loading / Start */}
        {phase === 'loading' && (
          <div className="flex flex-col items-center gap-4 py-12">
            <p className="text-center text-sm text-muted-foreground">
              Fill in Past Simple and Past Participle forms of irregular verbs
            </p>
            <button
              onClick={handleStart}
              disabled={startMutation.isPending}
              className="flex h-12 items-center gap-2 rounded-xl bg-primary px-8 text-sm font-semibold text-white disabled:opacity-50"
            >
              {startMutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
              Start Game
            </button>
          </div>
        )}

        {/* Playing */}
        {phase === 'playing' && round && (
          <AnimatePresence mode="wait">
            <motion.div
              key={currentRound}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              {/* Progress */}
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>Round {currentRound + 1} / {rounds.length}</span>
                <span>Score: {score} | Combo: {combo}x</span>
              </div>
              <div className="h-1.5 rounded-full bg-muted/30">
                <div
                  className="h-full rounded-full bg-primary transition-all"
                  style={{ width: `${((currentRound) / rounds.length) * 100}%` }}
                />
              </div>

              {/* Verb card */}
              <div className="rounded-2xl border border-border/50 bg-card p-6 text-center shadow-card">
                <p className="text-xs text-muted-foreground mb-1">Infinitive</p>
                <h2 className="font-heading text-3xl font-bold">{round.infinitive}</h2>
                {round.translation && (
                  <p className="mt-1 text-sm text-muted-foreground">{round.translation}</p>
                )}
              </div>

              {/* Hints from previous attempt */}
              {lastResult && lastResult.hints && Object.keys(lastResult.hints).length > 0 && (
                <div className="flex items-center gap-2 rounded-lg bg-amber-50 p-3 text-xs text-amber-700 dark:bg-amber-900/20 dark:text-amber-300">
                  <HelpCircle className="h-4 w-4" />
                  <div>
                    {lastResult.hints.past_simple && <span>Past Simple hint: <strong>{lastResult.hints.past_simple}</strong> &nbsp;</span>}
                    {lastResult.hints.past_participle && <span>Past Participle hint: <strong>{lastResult.hints.past_participle}</strong></span>}
                  </div>
                </div>
              )}

              {/* Input fields */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-1.5 block text-xs font-medium text-muted-foreground">Past Simple</label>
                  <input
                    value={pastSimple}
                    onChange={(e) => setPastSimple(e.target.value)}
                    placeholder="e.g. went"
                    className="h-11 w-full rounded-xl border border-border/50 bg-card px-4 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                    autoFocus
                  />
                </div>
                <div>
                  <label className="mb-1.5 block text-xs font-medium text-muted-foreground">Past Participle</label>
                  <input
                    value={pastParticiple}
                    onChange={(e) => setPastParticiple(e.target.value)}
                    placeholder="e.g. gone"
                    className="h-11 w-full rounded-xl border border-border/50 bg-card px-4 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                  />
                </div>
              </div>

              <button
                onClick={handleSubmit}
                disabled={answerMutation.isPending}
                className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-semibold text-white disabled:opacity-50"
              >
                {answerMutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Check'}
              </button>
            </motion.div>
          </AnimatePresence>
        )}

        {/* Result */}
        {phase === 'result' && lastResult && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
            {/* Past Simple result */}
            <div className={cn(
              'flex items-center gap-3 rounded-xl p-3',
              lastResult.past_simple_correct ? 'bg-emerald-50 dark:bg-emerald-900/20' : 'bg-red-50 dark:bg-red-900/20',
            )}>
              {lastResult.past_simple_correct ? <Check className="h-5 w-5 text-emerald-500" /> : <X className="h-5 w-5 text-red-500" />}
              <div className="text-sm">
                <span className="font-medium">Past Simple: </span>
                {lastResult.past_simple_correct ? (
                  <span className="text-emerald-600">{pastSimple}</span>
                ) : (
                  <>
                    <span className="text-red-500 line-through">{pastSimple}</span>
                    {lastResult.correct_past_simple && (
                      <span className="ml-1 font-semibold text-emerald-600">{lastResult.correct_past_simple}</span>
                    )}
                  </>
                )}
              </div>
            </div>

            {/* Past Participle result */}
            <div className={cn(
              'flex items-center gap-3 rounded-xl p-3',
              lastResult.past_participle_correct ? 'bg-emerald-50 dark:bg-emerald-900/20' : 'bg-red-50 dark:bg-red-900/20',
            )}>
              {lastResult.past_participle_correct ? <Check className="h-5 w-5 text-emerald-500" /> : <X className="h-5 w-5 text-red-500" />}
              <div className="text-sm">
                <span className="font-medium">Past Participle: </span>
                {lastResult.past_participle_correct ? (
                  <span className="text-emerald-600">{pastParticiple}</span>
                ) : (
                  <>
                    <span className="text-red-500 line-through">{pastParticiple}</span>
                    {lastResult.correct_past_participle && (
                      <span className="ml-1 font-semibold text-emerald-600">{lastResult.correct_past_participle}</span>
                    )}
                  </>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between rounded-lg bg-muted/20 px-4 py-2 text-xs">
              <span>Score: +{lastResult.score}</span>
              <span>XP: +{lastResult.xp_earned}</span>
              {lastResult.attempts_remaining > 0 && !shouldAdvance && (
                <span className="text-amber-500">{lastResult.attempts_remaining} attempt left</span>
              )}
            </div>

            <button
              onClick={handleNext}
              className="flex h-11 w-full items-center justify-center rounded-xl bg-primary text-sm font-semibold text-white"
            >
              {!shouldAdvance
                ? 'Try Again'
                : currentRound + 1 < rounds.length
                  ? 'Next Verb'
                  : 'See Results'}
            </button>
          </motion.div>
        )}

        {/* Complete */}
        {phase === 'complete' && completeData && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
            <div className="flex flex-col items-center gap-2 py-4">
              <Trophy className="h-12 w-12 text-amber-500" />
              <h2 className="font-heading text-2xl font-bold">Game Complete!</h2>
              <p className="text-sm text-muted-foreground">{completeData.accuracy_pct}% accuracy</p>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="rounded-xl bg-muted/30 p-3">
                <div className="text-xl font-bold">{completeData.total_score}</div>
                <div className="text-[10px] text-muted-foreground">Score</div>
              </div>
              <div className="rounded-xl bg-muted/30 p-3">
                <div className="text-xl font-bold">{completeData.max_score}</div>
                <div className="text-[10px] text-muted-foreground">Max Score</div>
              </div>
              <div className="rounded-xl bg-muted/30 p-3">
                <div className="text-xl font-bold">{completeData.xp_earned}</div>
                <div className="text-[10px] text-muted-foreground">XP Earned</div>
              </div>
            </div>

            {/* Round details */}
            <div className="space-y-2">
              <h3 className="text-sm font-semibold">Results</h3>
              {completeData.rounds.map((r) => (
                <div key={r.round_number} className="flex items-center gap-3 rounded-lg bg-muted/20 px-3 py-2 text-xs">
                  <span className="font-medium">{r.infinitive}</span>
                  <span className="text-muted-foreground">→</span>
                  <span className={r.past_simple_correct ? 'text-emerald-600' : 'text-red-500'}>{r.user_past_simple || '—'}</span>
                  <span className="text-muted-foreground">/</span>
                  <span className={r.past_participle_correct ? 'text-emerald-600' : 'text-red-500'}>{r.user_past_participle || '—'}</span>
                  <span className="ml-auto font-bold">+{r.score}</span>
                </div>
              ))}
            </div>

            <button
              onClick={() => navigate('/games')}
              className="flex h-11 w-full items-center justify-center rounded-xl bg-primary text-sm font-semibold text-white"
            >
              Back to Games
            </button>
          </motion.div>
        )}
      </div>
    </PageTransition>
  );
}
