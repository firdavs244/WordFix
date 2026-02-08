import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle2, ArrowRight, Home, RotateCcw, Trophy, Star } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { useReviewSession } from '../hooks/useReview';

export function ReviewCompletePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { data: sessionData } = useReviewSession(sessionId!);

  const session = sessionData?.data;
  const stateData = location.state as { totalWords?: number; answers?: number } | null;
  const totalWords = session?.total_words ?? stateData?.totalWords ?? 0;
  const correctCount = session?.correct_count ?? 0;
  const incorrectCount = session?.incorrect_count ?? 0;
  const accuracy =
    totalWords > 0
      ? Math.round((correctCount / totalWords) * 100)
      : 0;

  const getMessage = () => {
    if (accuracy >= 90) return { text: 'Outstanding!', emoji: '🏆' };
    if (accuracy >= 70) return { text: 'Great job!', emoji: '🌟' };
    if (accuracy >= 50) return { text: 'Good effort!', emoji: '💪' };
    return { text: 'Keep practicing!', emoji: '📚' };
  };

  const msg = getMessage();

  return (
    <PageTransition>
      <div className="mx-auto flex min-h-[70vh] max-w-lg flex-col items-center justify-center gap-8">
        {/* Success Animation */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 15, delay: 0.2 }}
          className="flex h-24 w-24 items-center justify-center rounded-full bg-success/10"
        >
          <CheckCircle2 className="h-12 w-12 text-success" />
        </motion.div>

        {/* Title */}
        <motion.div
          className="text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <p className="text-4xl">{msg.emoji}</p>
          <h1 className="mt-2 font-heading text-3xl font-bold">{msg.text}</h1>
          <p className="mt-1 text-muted-foreground">Session completed</p>
        </motion.div>

        {/* Stats Card */}
        <motion.div
          className="w-full"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card className="border-border/50">
            <CardContent className="grid grid-cols-3 gap-4 p-6">
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <Star className="h-4 w-4 text-amber-500" />
                </div>
                <p className="mt-1 font-heading text-2xl font-bold">{totalWords}</p>
                <p className="text-xs text-muted-foreground">Words</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <CheckCircle2 className="h-4 w-4 text-success" />
                </div>
                <p className="mt-1 font-heading text-2xl font-bold text-success">{correctCount}</p>
                <p className="text-xs text-muted-foreground">Correct</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-1">
                  <Trophy className="h-4 w-4 text-primary" />
                </div>
                <p className="mt-1 font-heading text-2xl font-bold text-primary">{accuracy}%</p>
                <p className="text-xs text-muted-foreground">Accuracy</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Incorrect note */}
        {incorrectCount > 0 && (
          <motion.p
            className="text-sm text-muted-foreground"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            {incorrectCount} word{incorrectCount > 1 ? 's' : ''} need more practice. They'll appear sooner in your next review.
          </motion.p>
        )}

        {/* Actions */}
        <motion.div
          className="flex flex-col gap-3 sm:flex-row"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
        >
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => navigate('/')}
          >
            <Home className="h-4 w-4" />
            Dashboard
          </Button>
          <Button
            className="gap-2 shadow-lg shadow-primary/25"
            onClick={() => navigate('/review')}
          >
            <RotateCcw className="h-4 w-4" />
            Review Again
            <ArrowRight className="h-4 w-4" />
          </Button>
        </motion.div>
      </div>
    </PageTransition>
  );
}
