import { useNavigate } from 'react-router-dom';
import { Link2 } from 'lucide-react';
import GamePreScreen from '../components/GamePreScreen';
import GameComboIndicator from '../components/GameComboIndicator';
import WordMatchBoard from './components/WordMatchBoard';
import { useWordMatch } from './hooks/useWordMatch';
import { useEffect } from 'react';

const RULES = [
  'Match each word with its correct translation',
  'Click a word then click its matching translation',
  'Matched pairs will fade out',
  'Wrong matches shake and break your combo',
];

export default function WordMatchPage() {
  const navigate = useNavigate();
  const game = useWordMatch();

  useEffect(() => {
    if (game.phase === 'complete' && game.result) {
      navigate(`/games/result/${game.result.id}`);
    }
  }, [game.phase, game.result, navigate]);

  if (game.phase === 'ready') {
    return <GamePreScreen title="Word Match" icon={Link2} rules={RULES} onStart={game.start} isLoading={game.isStarting} />;
  }

  return (
    <div className="mx-auto max-w-lg px-4 py-8">
      <GameComboIndicator combo={game.combo} multiplier={1 + game.combo * 0.1} />
      <h2 className="mb-6 text-center font-heading text-xl font-bold">Match the Pairs</h2>
      <WordMatchBoard
        pairs={game.pairs}
        translations={game.translations}
        selectedWord={game.selectedWord}
        selectedTranslation={game.selectedTranslation}
        wrongPair={game.wrongPair}
        onSelectWord={game.selectWord}
        onSelectTranslation={game.selectTranslation}
      />
    </div>
  );
}
