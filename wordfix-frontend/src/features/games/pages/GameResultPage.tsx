import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Trophy, CheckCircle2, XCircle, Star, RotateCcw, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';

const GAME_LABELS: Record<string, string> = {
  speed_round: 'Speed Round',
  word_match: 'Word Match',
  word_context: 'Word Context',
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
            </CardContent>
          </Card>
        </motion.div>

        <div className="flex w-full gap-3">
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/games')}>
            <RotateCcw className="h-4 w-4" /> Play Again
          </Button>
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </div>
      </div>
    </PageTransition>
  );
}
