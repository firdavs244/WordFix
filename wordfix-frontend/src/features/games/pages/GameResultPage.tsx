import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Trophy, CheckCircle2, XCircle, Star, RotateCcw, ArrowLeft, Flame, Zap, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { toast } from 'sonner';

const GAME_LABELS: Record<string, string> = {
  speed_round: 'Speed Round',
  word_match: 'Word Match',
  word_context: 'Word Context',
  story_builder: 'Story Complete!',
  listening_challenge: 'Challenge Complete!',
};



export function GameResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const state = location.state as {
    game_type: string;
    score: number;
    max_score: number;
    xp_earned: number;
    correct_answers: number;
    total_questions: number;
    max_combo?: number;
    combo_xp_bonus?: number;
    // Story Builder extras
    rounds?: Array<{ round_number: number; score: number; words_used: string[]; corrections: any[] }>;
    full_story?: string;
    // Listening Challenge extras
    listening_rounds?: Array<{ word: string; is_correct: boolean; attempts_used: number; score: number }>;
    accuracy_pct?: number;
  } | null;

  if (!state) {
    return (
      <PageTransition>
        <div className="flex h-full items-center justify-center">
          <p className="text-muted-foreground">No result data available.</p>
        </div>
      </PageTransition>
    );
  }

  const pct = state.max_score > 0 ? Math.round((state.score / state.max_score) * 100) : 0;
  const stars = pct >= 90 ? 3 : pct >= 60 ? 2 : pct >= 30 ? 1 : 0;
  const color = pct >= 80 ? 'text-green-500' : pct >= 50 ? 'text-yellow-500' : 'text-red-500';

  return (
    <PageTransition>
      <div className="mx-auto flex max-w-md flex-col items-center gap-6 py-12">
        {/* Stars */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', bounce: 0.4, delay: 0.1 }}
          className="flex gap-2"
        >
          {[1, 2, 3].map((s) => (
            <Star
              key={s}
              className={`h-10 w-10 ${s <= stars ? 'fill-yellow-400 text-yellow-400' : 'text-muted-foreground/30'}`}
            />
          ))}
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card className="w-full border-border/50 text-center">
            <CardContent className="space-y-5 p-8">
              <p className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                {GAME_LABELS[state.game_type] ?? state.game_type}
              </p>

              <div className="flex items-center justify-center gap-2">
                <Trophy className={`h-8 w-8 ${color}`} />
                <span className={`text-5xl font-bold ${color}`}>{state.score}</span>
                <span className="text-xl text-muted-foreground">/ {state.max_score}</span>
              </div>

              <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <CheckCircle2 className="h-4 w-4 text-green-500" /> {state.correct_answers} correct
                </span>
                <span className="flex items-center gap-1">
                  <XCircle className="h-4 w-4 text-red-500" /> {state.total_questions - state.correct_answers} wrong
                </span>
              </div>

              <div className="rounded-lg bg-primary/5 p-3">
                <p className="text-sm text-muted-foreground">XP Earned</p>
                <p className="text-2xl font-bold text-primary">+{state.xp_earned}</p>
              </div>

              {/* Combo Stats */}
              {(state.max_combo ?? 0) >= 2 && (
                <div className="flex items-center justify-center gap-4">
                  <div className="flex items-center gap-1.5 rounded-lg bg-orange-500/10 px-3 py-1.5">
                    <Flame className="h-4 w-4 text-orange-500" />
                    <span className="text-sm font-bold text-orange-500">Max Combo: {state.max_combo}</span>
                  </div>
                  {(state.combo_xp_bonus ?? 0) > 0 && (
                    <div className="flex items-center gap-1.5 rounded-lg bg-primary/10 px-3 py-1.5">
                      <Zap className="h-4 w-4 text-primary" />
                      <span className="text-sm font-bold text-primary">+{state.combo_xp_bonus} XP Bonus</span>
                    </div>
                  )}
                </div>
              )}

              {/* Story Builder: Round Scores + Full Story */}
              {state.game_type === 'story_builder' && state.rounds && (
                <div className="space-y-3 text-left">
                  <p className="text-sm font-semibold">📊 Round Scores</p>
                  {state.rounds.map((r) => (
                    <div key={r.round_number} className="flex items-center justify-between rounded-lg border px-3 py-2 text-sm">
                      <span>Round {r.round_number}</span>
                      <span className="font-bold">{r.score}/20</span>
                    </div>
                  ))}
                  {state.full_story && (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-semibold">📖 Your Story</p>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="gap-1 text-xs"
                          onClick={() => {
                            navigator.clipboard.writeText(state.full_story ?? '');
                            toast.success('Story copied!');
                          }}
                        >
                          <Copy className="h-3.5 w-3.5" /> Copy
                        </Button>
                      </div>
                      <div className="max-h-48 overflow-y-auto rounded-lg bg-muted/50 p-3 text-sm leading-relaxed">
                        {state.full_story}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Listening Challenge: Word Results */}
              {state.game_type === 'listening_challenge' && state.listening_rounds && (
                <div className="space-y-2 text-left">
                  {state.accuracy_pct !== undefined && (
                    <p className="text-center text-sm text-muted-foreground">
                      Accuracy: {state.accuracy_pct}%
                    </p>
                  )}
                  <p className="text-sm font-semibold">📊 Results</p>
                  {state.listening_rounds.map((r, i) => (
                    <div
                      key={i}
                      className={`flex items-center justify-between rounded-lg px-3 py-2 text-sm ${
                        r.is_correct ? 'bg-green-500/5' : 'bg-red-500/5'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span>{r.is_correct ? '✅' : '❌'}</span>
                        <span className="font-medium">{r.word}</span>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {r.is_correct
                          ? `${r.attempts_used === 1 ? '1st' : r.attempts_used === 2 ? '2nd' : '3rd'} try (${r.score})`
                          : `failed (${r.score})`}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <div className="flex w-full gap-3">
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/games')}>
            <RotateCcw className="h-4 w-4" /> Play Again
          </Button>
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/')}>
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </div>
      </div>
    </PageTransition>
  );
}
