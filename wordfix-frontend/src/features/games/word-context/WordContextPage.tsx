import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText } from 'lucide-react';
import GamePreScreen from '../components/GamePreScreen';
import ContextParagraph from './components/ContextParagraph';
import ContextInput from './components/ContextInput';
import ContextFeedback from './components/ContextFeedback';
import { useWordContext } from './hooks/useWordContext';

const RULES = [
  'Read the sentence with a missing word',
  'Use context clues to determine the correct word',
  'Type your answer and press Enter',
  'Build streaks for bonus XP',
];

export default function WordContextPage() {
  const navigate = useNavigate();
  const game = useWordContext();

  useEffect(() => {
    if (game.phase === 'complete' && game.result) {
      navigate(`/games/result/${game.result.id}`, {
        state: {
          correct: game.result.correct_answers,
          total: game.result.correct_answers + game.result.incorrect_answers,
          time: game.result.duration_seconds,
          xp: game.result.xp_earned,
          gameType: 'word-context',
        }
      });
    }
  }, [game.phase, game.result, navigate]);

  if (game.phase === 'ready') {
    return <GamePreScreen title="Word Context" icon={FileText} rules={RULES} onStart={game.start} isLoading={game.isStarting} />;
  }

  if (!game.current) return null;

  return (
    <div className="mx-auto max-w-lg px-4 py-8">
      <p className="mb-6 text-center text-sm text-muted-foreground">
        Question {game.currentIndex + 1} of {game.total}
      </p>
      <ContextParagraph
        context={game.current.context}
        answered={game.answered}
        correctAnswer={game.current.correct_answer}
        userAnswer={game.userAnswer}
        isCorrect={game.isCorrect}
      />
      {!game.answered && <ContextInput onSubmit={game.submitAnswer} disabled={game.answered} />}
      {game.answered && (
        <ContextFeedback
          isCorrect={game.isCorrect}
          explanation={game.current.explanation}
          onNext={game.next}
          isLast={game.currentIndex >= game.total - 1}
        />
      )}
    </div>
  );
}
