import { useParams, useSearchParams } from 'react-router-dom';
import PageTransition from '@/components/shared/PageTransition';
import GameResultDisplay from './components/GameResultDisplay';
import GameResultStats from './components/GameResultStats';
import GameResultActions from './components/GameResultActions';

export default function GameResultPage() {
  const { gameId } = useParams<{ gameId: string }>();
  const [searchParams] = useSearchParams();

  const correct = parseInt(searchParams.get('correct') || '0', 10);
  const total = parseInt(searchParams.get('total') || '0', 10);
  const time = parseInt(searchParams.get('time') || '0', 10);
  const xp = parseInt(searchParams.get('xp') || '0', 10);

  const wrong = total - correct;
  const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

  return (
    <PageTransition>
      <div className="mx-auto max-w-md space-y-8 py-8 text-center">
        <GameResultDisplay percentage={percentage} />
        <GameResultStats
          correct={correct}
          incorrect={wrong}
          duration={time}
          xp={xp}
        />
        <GameResultActions
          gameRoute={`/games/${gameId}`}
          dashboardRoute="/games"
        />
      </div>
    </PageTransition>
  );
}
