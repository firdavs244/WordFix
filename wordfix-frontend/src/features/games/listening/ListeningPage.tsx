import { useCallback, useRef } from 'react';
import { Headphones } from 'lucide-react';
import GamePreScreen from '../components/GamePreScreen';
import AudioPlayer from './components/AudioPlayer';
import AttemptIndicator from './components/AttemptIndicator';
import ListeningInput from './components/ListeningInput';
import ListeningFeedback from './components/ListeningFeedback';
import ListeningComplete from './components/ListeningComplete';
import { useListening } from './hooks/useListening';

const RULES = [
  'Listen to the word pronunciation',
  'Type what you hear in the text field',
  'You have 3 attempts per word',
  'Use replay to hear the word again',
];

export default function ListeningPage() {
  const game = useListening();
  const lastResponseRef = useRef<any>(null);

  const handleSubmit = useCallback(async (answer: string) => {
    const res = await game.submitAnswer(answer);
    lastResponseRef.current = res;
  }, [game]);

  const handleNext = useCallback(async () => {
    const res = lastResponseRef.current;
    await game.nextRound(res);
    lastResponseRef.current = null;
  }, [game]);

  if (game.phase === 'ready') {
    return <GamePreScreen title="Listening Challenge" icon={Headphones} rules={RULES} onStart={game.start} isLoading={game.isStarting} />;
  }

  if (game.phase === 'complete' && game.result) {
    return (
      <div className="mx-auto max-w-lg px-4 py-8">
        <ListeningComplete data={game.result} />
      </div>
    );
  }

  if (!game.round) return null;

  return (
    <div className="mx-auto flex max-w-lg flex-col items-center gap-6 px-4 py-8">
      <p className="text-sm text-muted-foreground">
        Round {game.round.roundNumber} of {game.totalRounds}
      </p>
      <AudioPlayer audioUrl={game.round.audioUrl} />
      <AttemptIndicator total={game.round.maxAttempts} remaining={game.attemptsRemaining} />
      {game.round.hint && (
        <p className="text-xs text-muted-foreground">Hint: {game.round.hint}</p>
      )}
      {!game.answered && <ListeningInput onSubmit={handleSubmit} disabled={game.answered} />}
      {game.answered && (
        <ListeningFeedback
          isCorrect={game.isCorrect}
          correctAnswer={game.correctAnswer}
          onNext={handleNext}
        />
      )}
    </div>
  );
}
