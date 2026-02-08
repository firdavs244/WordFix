import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Brain, Zap, BookOpen, ArrowRight, Clock, Target } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { PageTransition } from '@/components/animations/PageTransition';
import { listContainerVariants, listItemVariants, cardHoverVariants } from '@/components/animations/PageTransition';
import { StreakWidget, DailyProgressWidget } from '../components';
import { useReviewWords, useReviewSummary, useStartSession } from '../hooks/useReview';
import { Skeleton } from '@/components/ui/skeleton';
import { useNavigate } from 'react-router-dom';
import type { SessionType } from '@/types';

export function ReviewPage() {
  const navigate = useNavigate();
  const { data: reviewWordsData, isLoading: wordsLoading } = useReviewWords();
  const { data: summaryData, isLoading: summaryLoading } = useReviewSummary();
  const startSession = useStartSession();

  const reviewWords = reviewWordsData?.data ?? [];
  const summary = summaryData?.data;
  const wordsDue = reviewWords.length;

  const handleStartSession = async (type: SessionType) => {
    try {
      const response = await startSession.mutateAsync(type);
      navigate(`/review/session/${response.data.id}`, {
        state: { words: reviewWords, sessionType: type },
      });
    } catch {
      // Error handled by mutation
    }
  };

  const sessionTypes = [
    {
      type: 'review' as SessionType,
      label: 'Review Due',
      description: 'Review words that are due for spaced repetition',
      icon: Brain,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      count: wordsDue,
    },
    {
      type: 'learn' as SessionType,
      label: 'Learn New',
      description: 'Practice recently added words',
      icon: BookOpen,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
      count: null,
    },
    {
      type: 'mixed' as SessionType,
      label: 'Mixed Practice',
      description: 'A mix of new and review words',
      icon: Zap,
      color: 'text-amber-500',
      bgColor: 'bg-amber-500/10',
      count: null,
    },
  ];

  return (
    <PageTransition>
      <div className="mx-auto max-w-5xl space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <h1 className="font-heading text-3xl font-bold">Review</h1>
          <p className="mt-1 text-muted-foreground">
            Practice your vocabulary with spaced repetition
          </p>
        </motion.div>

        {/* Streak & Progress */}
        <div className="grid gap-4 sm:grid-cols-2">
          <StreakWidget />
          <DailyProgressWidget />
        </div>

        {/* Summary Stats */}
        {summaryLoading ? (
          <div className="grid gap-3 grid-cols-2 sm:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-20 rounded-xl" />
            ))}
          </div>
        ) : summary ? (
          <motion.div
            className="grid gap-3 grid-cols-2 sm:grid-cols-4"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {[
              { label: 'Words Due', value: summary.words_due, icon: Clock, color: 'text-orange-500' },
              { label: 'Today', value: summary.reviews_today, icon: Target, color: 'text-blue-500' },
              { label: 'Accuracy', value: `${summary.average_accuracy}%`, icon: Brain, color: 'text-purple-500' },
              { label: 'Total Reviews', value: summary.total_reviews, icon: BookOpen, color: 'text-green-500' },
            ].map((stat) => (
              <motion.div key={stat.label} variants={listItemVariants}>
                <Card className="border-border/50">
                  <CardContent className="flex items-center gap-3 p-4">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-muted ${stat.color}`}>
                      <stat.icon className="h-5 w-5" />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">{stat.label}</p>
                      <p className="font-heading text-xl font-bold">{stat.value}</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        ) : null}

        {/* Session Types */}
        <div>
          <h2 className="mb-3 font-heading text-xl font-semibold">Start a Session</h2>
          <motion.div
            className="grid gap-4 sm:grid-cols-3"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {sessionTypes.map((session) => (
              <motion.div key={session.type} variants={listItemVariants}>
                <motion.div variants={cardHoverVariants} initial="rest" whileHover="hover" whileTap="tap">
                  <Card
                    className="cursor-pointer border-border/50 transition-shadow hover:shadow-lg"
                    onClick={() => handleStartSession(session.type)}
                  >
                    <CardContent className="p-6">
                      <div className={`mb-3 flex h-12 w-12 items-center justify-center rounded-xl ${session.bgColor}`}>
                        <session.icon className={`h-6 w-6 ${session.color}`} />
                      </div>
                      <h3 className="font-heading text-lg font-semibold">{session.label}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">{session.description}</p>
                      {session.count !== null && (
                        <Badge className="mt-3" variant={session.count > 0 ? 'default' : 'outline'}>
                          {session.count} words
                        </Badge>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Due Words Preview */}
        {!wordsLoading && wordsDue > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="border-border/50">
              <CardContent className="p-6">
                <div className="mb-3 flex items-center justify-between">
                  <h3 className="font-heading text-lg font-semibold">Words Due for Review</h3>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-1 text-primary"
                    onClick={() => handleStartSession('review')}
                  >
                    Start <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {reviewWords.slice(0, 12).map((word) => (
                    <Badge key={word.id} variant="outline" className="py-1">
                      {word.original_word}
                    </Badge>
                  ))}
                  {wordsDue > 12 && (
                    <Badge variant="outline" className="py-1 text-muted-foreground">
                      +{wordsDue - 12} more
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* History Link */}
        <div className="text-center">
          <Link to="/review/history">
            <Button variant="outline" className="gap-2">
              <Clock className="h-4 w-4" />
              View Review History
            </Button>
          </Link>
        </div>
      </div>
    </PageTransition>
  );
}
