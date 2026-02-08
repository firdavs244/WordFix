import { useState } from 'react';
import { motion } from 'framer-motion';
import { Clock, CheckCircle2, XCircle, Brain, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { PageTransition } from '@/components/animations/PageTransition';
import { listContainerVariants, listItemVariants } from '@/components/animations/PageTransition';
import { useReviewHistory } from '../hooks/useReview';

export function ReviewHistoryPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useReviewHistory(page, 10);

  const sessions = data?.data ?? [];
  const meta = data?.meta;

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDuration = (start: string, end: string | null) => {
    if (!end) return 'In progress';
    const diff = new Date(end).getTime() - new Date(start).getTime();
    const minutes = Math.round(diff / 60000);
    return minutes < 1 ? '< 1 min' : `${minutes} min`;
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-3xl space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Link to="/review">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <div>
            <h1 className="font-heading text-3xl font-bold">Review History</h1>
            <p className="mt-1 text-muted-foreground">
              {meta ? `${meta.total_count} sessions` : 'Your past review sessions'}
            </p>
          </div>
        </div>

        {/* Sessions List */}
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} className="h-24 w-full rounded-xl" />
            ))}
          </div>
        ) : sessions.length === 0 ? (
          <Card className="border-border/50">
            <CardContent className="py-12 text-center">
              <Brain className="mx-auto h-12 w-12 text-muted-foreground/50" />
              <p className="mt-3 text-lg font-medium">No sessions yet</p>
              <p className="text-sm text-muted-foreground">Start a review session to see history here.</p>
              <Link to="/review">
                <Button className="mt-4">Start Reviewing</Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <motion.div
            className="space-y-3"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {sessions.map((session) => {
              const accuracy =
                session.total_words > 0
                  ? Math.round((session.correct_count / session.total_words) * 100)
                  : 0;

              return (
                <motion.div key={session.id} variants={listItemVariants}>
                  <Card className="border-border/50 transition-shadow hover:shadow-md">
                    <CardContent className="flex items-center gap-4 p-4">
                      <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${
                        session.is_completed ? 'bg-success/10' : 'bg-muted'
                      }`}>
                        {session.is_completed ? (
                          <CheckCircle2 className="h-6 w-6 text-success" />
                        ) : (
                          <Clock className="h-6 w-6 text-muted-foreground" />
                        )}
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="font-medium capitalize">
                            {session.session_type} Session
                          </p>
                          <Badge variant={session.is_completed ? 'default' : 'outline'}>
                            {session.is_completed ? 'Completed' : 'In Progress'}
                          </Badge>
                        </div>
                        <p className="mt-0.5 text-sm text-muted-foreground">
                          {formatDate(session.started_at)}
                          {' · '}
                          {formatDuration(session.started_at, session.completed_at)}
                        </p>
                      </div>

                      <div className="hidden sm:flex items-center gap-4 text-sm">
                        <div className="text-center">
                          <p className="font-heading font-bold">{session.total_words}</p>
                          <p className="text-xs text-muted-foreground">Words</p>
                        </div>
                        <div className="text-center">
                          <div className="flex items-center gap-1">
                            <CheckCircle2 className="h-3 w-3 text-success" />
                            <span className="font-heading font-bold text-success">{session.correct_count}</span>
                          </div>
                          <p className="text-xs text-muted-foreground">Correct</p>
                        </div>
                        <div className="text-center">
                          <div className="flex items-center gap-1">
                            <XCircle className="h-3 w-3 text-error" />
                            <span className="font-heading font-bold text-error">{session.incorrect_count}</span>
                          </div>
                          <p className="text-xs text-muted-foreground">Wrong</p>
                        </div>
                        <div className="text-center">
                          <p className="font-heading font-bold text-primary">{accuracy}%</p>
                          <p className="text-xs text-muted-foreground">Accuracy</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        )}

        {/* Pagination */}
        {meta && meta.total_pages > 1 && (
          <div className="flex items-center justify-center gap-2 pt-4">
            <Button
              variant="outline"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Previous
            </Button>
            <span className="text-sm text-muted-foreground">
              Page {meta.page} of {meta.total_pages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= meta.total_pages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </PageTransition>
  );
}
