import { motion } from 'framer-motion';
import { Copy } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { toast } from 'sonner';
import type { StoryCompleteResponse } from '@/types';
import { BookOpen, getStars, getRoundStars } from './storyBuilderHelpers';

interface StoryCompleteProps {
  completeData: StoryCompleteResponse;
  onPlayAgain: () => void;
}

export function StoryComplete({ completeData, onPlayAgain }: StoryCompleteProps) {
  const navigate = useNavigate();
  const totalStars = getStars(completeData.total_score, completeData.max_score);

  const handleCopyStory = () => {
    if (completeData.full_story) {
      navigator.clipboard.writeText(completeData.full_story).then(() => {
        toast.success('Story copied to clipboard!');
      });
    }
  };

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
              <span key={i} className={`text-xl ${i < totalStars ? '' : 'opacity-20'}`}>
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
                  <span className="text-sm font-medium">Round {r.round_number}</span>
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
