import { useParams, useNavigate } from 'react-router-dom';
import { PageTransition } from '@/components/shared';
import CompletionCelebration from './components/CompletionCelebration';
import CompletionStats from './components/CompletionStats';
import CompletionActions from './components/CompletionActions';
import { useReviewSession } from './hooks/useReview';

export default function ReviewCompletePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const { data } = useReviewSession(sessionId!);
  const session = data?.data;
  const total = session?.total_words ?? 0;
  const correct = session?.correct_count ?? 0;
  const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0;

  return (
    <PageTransition>
      <div className="mx-auto max-w-lg px-4 py-12">
        <CompletionCelebration accuracy={accuracy} />
        <CompletionStats total={total} correct={correct} accuracy={accuracy} maxCombo={session?.max_combo ?? 0} comboXp={session?.combo_xp_bonus ?? 0} />
        <CompletionActions onDashboard={() => navigate('/')} onReviewAgain={() => navigate('/review')} />
      </div>
    </PageTransition>
  );
}
