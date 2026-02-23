import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Check, X, Loader2, Trophy } from 'lucide-react';
import { toast } from 'sonner';
import type { AxiosResponse } from 'axios';
import PageTransition from '@/components/shared/PageTransition';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import { cn } from '@/lib/utils';
import type {
  SynonymAntonymStartResponse,
  SynonymAntonymAnswerResponse,
  SynonymAntonymCompleteResponse,
} from '@/types/game';

type Phase = 'loading' | 'playing' | 'result' | 'complete';

export default function SynonymAntonymPage() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<Phase>('loading');
  const [sessionId, setSessionId] = useState('');
  const [rounds, setRounds] = useState<SynonymAntonymStartResponse['rounds']>([]);
  const [currentRound, setCurrentRound] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<SynonymAntonymAnswerResponse | null>(null);
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [completeData, setCompleteData] = useState<SynonymAntonymCompleteResponse | null>(null);

  // Start game
  const startMutation = useMutation({
    mutationFn: () => apiClient.post(API_ENDPOINTS.GAMES.SYNONYM_ANTONYM_START),
    onSuccess: (res: AxiosResponse) => {
      const data = res.data.data;
      setSessionId(data.session_id);
      setRounds(data.rounds);
      setPhase('playing');
    },
    onError: () => toast.error('Failed to start game'),
  });

  // Submit answer
  const answerMutation = useMutation({
    mutationFn: (answer: string) =>
      apiClient.post(API_ENDPOINTS.GAMES.SYNONYM_ANTONYM_ANSWER, {
        session_id: sessionId,
        round_number: rounds[currentRound].round_number,
        answer,
      }),
    onSuccess: (res: AxiosResponse) => {
      const data = res.data.data as SynonymAntonymAnswerResponse;
      setLastResult(data);
      setScore((s) => s + data.score);
      setCombo(data.combo);
      setPhase('result');
    },
  });

  // Complete game
  const completeMutation = useMutation({
    mutationFn: () =>
      apiClient.post(API_ENDPOINTS.GAMES.SYNONYM_ANTONYM_COMPLETE, { session_id: sessionId }),
    onSuccess: (res: AxiosResponse) => {
      setCompleteData(res.data.data);
      setPhase('complete');
    },
  });

  const handleStart = () => startMutation.mutate();
  const handleSelectAnswer = (answer: string) => {
    setSelected(answer);
    answerMutation.mutate(answer);
  };

  const handleNext = useCallback(() => {
    if (currentRound + 1 < rounds.length) {
      setCurrentRound((r) => r + 1);
      setSelected(null);
      setLastResult(null);
      setPhase('playing');
    } else {
      completeMutation.mutate();
    }
  }, [currentRound, rounds.length, completeMutation]);

  const round = rounds[currentRound];

  return (
    <PageTransition>
      <div className="mx-auto max-w-lg space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/games')} className="rounded-lg p-2 hover:bg-muted/40">
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="font-heading text-xl font-bold">Synonym & Antonym</h1>
        </div>

        {/* Loading / Start */}
        {phase === 'loading' && (
          <div className="flex flex-col items-center gap-4 py-12">
            <p className="text-center text-sm text-muted-foreground">
              Find synonyms and antonyms for vocabulary words
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

              {/* Question */}
              <div className="rounded-2xl border border-border/50 bg-card p-6 text-center shadow-card">
                <span className={cn(
                  'inline-block rounded-full px-3 py-1 text-xs font-semibold uppercase',
                  round.question_type === 'synonym'
                    ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400'
                    : 'bg-rose-100 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400',
                )}>
                  Find the {round.question_type}
                </span>
                <h2 className="mt-4 font-heading text-3xl font-bold">{round.word}</h2>
              </div>

              {/* Options */}
              <div className="grid grid-cols-2 gap-3">
                {round.options.map((opt) => (
                  <button
                    key={opt}
                    onClick={() => handleSelectAnswer(opt)}
                    disabled={answerMutation.isPending || !!selected}
                    className={cn(
                      'rounded-xl border-2 px-4 py-3.5 text-sm font-medium transition-all',
                      selected === opt
                        ? 'border-primary bg-primary/10'
                        : 'border-border/50 hover:border-primary/30 hover:bg-muted/20',
                      answerMutation.isPending && 'opacity-50',
                    )}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </motion.div>
          </AnimatePresence>
        )}

        {/* Result */}
        {phase === 'result' && lastResult && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
            <div className={cn(
              'flex items-center gap-3 rounded-xl p-4',
              lastResult.is_correct ? 'bg-emerald-50 dark:bg-emerald-900/20' : 'bg-red-50 dark:bg-red-900/20',
            )}>
              {lastResult.is_correct ? (
                <Check className="h-6 w-6 text-emerald-500" />
              ) : (
                <X className="h-6 w-6 text-red-500" />
              )}
              <div>
                <p className="text-sm font-semibold">
                  {lastResult.is_correct ? 'Correct!' : 'Incorrect'}
                </p>
                {!lastResult.is_correct && (
                  <p className="text-xs text-muted-foreground">
                    Correct answer: <strong>{lastResult.correct_answer}</strong>
                  </p>
                )}
              </div>
              <span className="ml-auto text-sm font-bold">+{lastResult.xp_earned} XP</span>
            </div>
            <button
              onClick={handleNext}
              className="flex h-11 w-full items-center justify-center rounded-xl bg-primary text-sm font-semibold text-white"
            >
              {currentRound + 1 < rounds.length ? 'Next Round' : 'See Results'}
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
