import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap } from 'lucide-react';
import GamePreScreen from '../components/GamePreScreen';
import GameComboIndicator from '../components/GameComboIndicator';
import SpeedRoundCountdown from './components/SpeedRoundCountdown';
import SpeedRoundTimer from './components/SpeedRoundTimer';
import SpeedRoundWord from './components/SpeedRoundWord';
import SpeedRoundOptions from './components/SpeedRoundOptions';
import { useSpeedRound } from './hooks/useSpeedRound';

const RULES = [
  'Translate as many words as possible in 60 seconds',
  'Choose the correct translation from 4 options',
  'Build combos for bonus XP by answering correctly in a row',
  'Wrong answers break your combo streak',
];

export default function SpeedRoundPage() {
  const navigate = useNavigate();
  const game = useSpeedRound();
  const [remaining, setRemaining] = useState(60);

  useEffect(() => {
    if (game.phase !== 'playing') return;
    const interval = setInterval(() => {
      setRemaining((t) => {
        if (t <= 1) { clearInterval(interval); game.endGame().then((r) => {
          if (r) navigate(`/games/result/${r.id}`);
        }); return 0; }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [game.phase, game.endGame, navigate]);

  const handleAnswer = useCallback((wordId: string, selected: string, correct: boolean) => {
    game.answerWord(wordId, selected, correct);
  }, [game]);

  if (game.phase === 'ready') {
    return <GamePreScreen title="Speed Round" icon={Zap} rules={RULES} onStart={game.start} isLoading={game.isStarting} />;
  }

  if (game.phase === 'countdown') {
    return <SpeedRoundCountdown onComplete={game.onCountdownDone} />;
  }

  if (!game.current) return null;

  return (
    <div className="mx-auto flex min-h-screen max-w-lg flex-col items-center justify-center gap-8 px-4">
      <SpeedRoundTimer remaining={remaining} total={game.timeLimit} />
      <GameComboIndicator combo={game.combo} multiplier={1 + game.combo * 0.1} />
      <SpeedRoundWord word={game.current.word} />
      <SpeedRoundOptions
        key={game.currentIndex}
        options={game.current.options}
        correctAnswer={game.current.correct_translation}
        onAnswer={(sel, cor) => handleAnswer(game.current!.word_id, sel, cor)}
      />
    </div>
  );
}
