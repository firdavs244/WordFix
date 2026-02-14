import { motion } from 'framer-motion';
import { Headphones } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import type { ListeningCompleteResponse } from '@/types';
import { getStars, getAttemptLabel } from './listeningHelpers';

interface ListeningCompleteProps {
  completeData: ListeningCompleteResponse;
  onPlayAgain: () => void;
}

export function ListeningComplete({
  completeData,
  onPlayAgain,
}: ListeningCompleteProps) {
  const navigate = useNavigate();
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
          className="space-y-2 text-center"
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
                  r.is_correct ? 'bg-green-500/5' : 'bg-red-500/5'
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
          <Button variant="outline" className="flex-1" onClick={onPlayAgain}>
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
