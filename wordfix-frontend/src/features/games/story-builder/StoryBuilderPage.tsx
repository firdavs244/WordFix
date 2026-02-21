import GenreSelector from './components/GenreSelector';
import StoryDisplay from './components/StoryDisplay';
import StoryWritingArea from './components/StoryWritingArea';
import StoryRoundScore from './components/StoryRoundScore';
import StoryComplete from './components/StoryComplete';
import { useStoryBuilder } from './hooks/useStoryBuilder';

export default function StoryBuilderPage() {
  const game = useStoryBuilder();

  if (game.phase === 'genre') {
    return <GenreSelector onSelect={game.selectGenre} isLoading={game.isStarting} />;
  }

  if (game.phase === 'complete') {
    return (
      <div className="mx-auto max-w-lg px-4 py-8">
        <StoryComplete fullStory={game.fullStory} totalScore={game.totalScore} maxScore={game.totalRounds * 20} />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-lg px-4 py-8">
      <p className="mb-4 text-center text-sm text-muted-foreground">
        Round {game.round} of {game.totalRounds}
      </p>
      <StoryDisplay text={game.aiText} targetWords={game.targetWords} />
      {game.roundScore !== null ? (
        <StoryRoundScore score={game.roundScore} feedback={game.roundFeedback} />
      ) : (
        <StoryWritingArea
          targetWords={game.targetWords}
          onSubmit={game.submitText}
          isSubmitting={game.isSubmitting}
        />
      )}
      {game.round >= game.totalRounds && game.roundScore !== null && (
        <button
          type="button"
          onClick={game.complete}
          className="mt-4 flex h-10 w-full items-center justify-center rounded-xl bg-primary text-sm font-medium text-white"
        >
          See Final Story
        </button>
      )}
    </div>
  );
}
