import { useParams, useSearchParams, useLocation } from 'react-router-dom';
import PageTransition from '@/components/shared/PageTransition';
import GameResultDisplay from './components/GameResultDisplay';
import GameResultStats from './components/GameResultStats';
import GameResultActions from './components/GameResultActions';

interface GameResultState {
  correct?: number;
  total?: number;
  time?: number;
  xp?: number;
  gameType?: string;
}

export default function GameResultPage() {
  const { gameId } = useParams<{ gameId: string }>();
  const [searchParams] = useSearchParams();
  const location = useLocation();

  // Try navigate state first, then search params as fallback
  const state = (location.state as GameResultState) || {};

  const correct = state.correct ?? parseInt(searchParams.get('correct') || '0', 10);
  const total = state.total ?? parseInt(searchParams.get('total') || '0', 10);
  const time = state.time ?? parseInt(searchParams.get('time') || '0', 10);
  const xp = state.xp ?? parseInt(searchParams.get('xp') || '0', 10);

  const wrong = total - correct;
  const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

  // Derive game route from gameId or gameType
  const gameType = state.gameType || gameId || '';
  const gameRoute = `/games/${gameType}`;

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
          gameRoute={gameRoute}
          dashboardRoute="/games"
        />
      </div>
    </PageTransition>
  );
}
