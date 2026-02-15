import GameResultStars from './GameResultStars';

interface Props {
  percentage: number;
}

export default function GameResultDisplay({ percentage }: Props) {
  return (
    <div className="text-center" data-testid="result-display">
      <GameResultStars score={percentage} />
      <p className="mt-4 font-heading text-4xl font-bold">{percentage}%</p>
    </div>
  );
}
