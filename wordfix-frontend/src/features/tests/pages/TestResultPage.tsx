import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, BarChart3, Clock, RotateCcw, ArrowLeft, Trophy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { useTestDetail } from '../hooks/useTests';

export function TestResultPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const { data, isLoading } = useTestDetail(sessionId!);

  const detail = data?.data;
  const session = detail?.session;
  const questions = detail?.questions;

  if (isLoading) {
    return (
      <PageTransition>
        <div className="flex h-full items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        </div>
      </PageTransition>
    );
  }

  if (!session) {
    return (
      <PageTransition>
        <div className="flex h-full items-center justify-center">
          <p className="text-muted-foreground">Test not found.</p>
        </div>
      </PageTransition>
    );
  }

  const pct = session.score_percentage ?? 0;
  const grade = pct >= 90 ? 'A' : pct >= 80 ? 'B' : pct >= 70 ? 'C' : pct >= 60 ? 'D' : 'F';
  const gradeColor = pct >= 80 ? 'text-green-500' : pct >= 60 ? 'text-yellow-500' : 'text-red-500';

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Score Card */}
        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.3 }}>
          <Card className="border-border/50 text-center">
            <CardContent className="space-y-4 p-8">
              <div className="flex items-center justify-center">
                <Trophy className={`h-12 w-12 ${gradeColor}`} />
              </div>
              <div>
                <p className={`text-6xl font-bold ${gradeColor}`}>{grade}</p>
                <p className="mt-1 text-2xl font-semibold">{pct}%</p>
              </div>
              <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
                <span className="flex items-center gap-1"><CheckCircle2 className="h-4 w-4 text-green-500" /> {session.correct_answers} correct</span>
                <span className="flex items-center gap-1"><XCircle className="h-4 w-4 text-red-500" /> {session.incorrect_answers} incorrect</span>
                <span className="flex items-center gap-1"><BarChart3 className="h-4 w-4" /> {session.total_questions} total</span>
              </div>
              {session.duration_seconds != null && (
                <p className="flex items-center justify-center gap-1 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  {Math.floor(session.duration_seconds / 60)}m {session.duration_seconds % 60}s
                </p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Question Review */}
        {questions && questions.length > 0 && (
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="text-lg">Question Review</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {questions.map((q: any, i: number) => (
                <div
                  key={q.id}
                  className={`rounded-lg p-3 ${q.is_correct ? 'bg-green-500/5' : 'bg-red-500/5'}`}
                >
                  <div className="flex items-start gap-2">
                    <span className="mt-0.5">
                      {q.is_correct ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                    </span>
                    <div className="flex-1 text-sm">
                      <p className="font-medium">{i + 1}. {q.question_text}</p>
                      <p className="text-muted-foreground">
                        Your answer: <span className={q.is_correct ? 'text-green-600' : 'text-red-600'}>{q.user_answer || '—'}</span>
                        {!q.is_correct && <span> · Correct: <span className="text-green-600">{q.correct_answer}</span></span>}
                      </p>
                      {q.explanation && <p className="mt-1 text-xs text-muted-foreground italic">{q.explanation}</p>}
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/tests')}>
            <RotateCcw className="h-4 w-4" /> New Test
          </Button>
          <Button variant="outline" className="flex-1 gap-2" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </div>
      </div>
    </PageTransition>
  );
}
