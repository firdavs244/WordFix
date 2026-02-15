import { useParams, Link } from 'react-router-dom';
import PageTransition from '@/components/shared/PageTransition';
import TestResultHeader from './components/TestResultHeader';
import TestResultStats from './components/TestResultStats';
import TestQuestionReview from './components/TestQuestionReview';
import { useTestSession } from './hooks/useTests';

function getGrade(score: number): 'A' | 'B' | 'C' | 'D' | 'F' {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'F';
}

export default function TestResultPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const { data } = useTestSession(sessionId!);

  if (!data) {
    return <div className="flex min-h-screen items-center justify-center text-muted-foreground">Loading...</div>;
  }

  const { session, questions } = data;
  const grade = getGrade(session.score_percentage);

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6 px-4 py-8">
        <TestResultHeader grade={grade} score={session.score_percentage} />
        <TestResultStats
          correct={session.correct_answers}
          incorrect={session.incorrect_answers}
          total={session.total_questions}
          duration={session.duration_seconds}
        />
        <TestQuestionReview questions={questions} />
        <div className="flex gap-3">
          <Link
            to="/tests"
            className="flex h-10 flex-1 items-center justify-center rounded-xl bg-primary text-sm font-medium text-white"
          >
            Take Another Test
          </Link>
          <Link
            to="/dashboard"
            className="flex h-10 flex-1 items-center justify-center rounded-xl border border-border/50 text-sm font-medium"
          >
            Dashboard
          </Link>
        </div>
      </div>
    </PageTransition>
  );
}
