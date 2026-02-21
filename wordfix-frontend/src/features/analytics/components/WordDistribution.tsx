import ConfidenceChart from './ConfidenceChart';
import DifficultyDistribution from './DifficultyDistribution';
import type { WordProgressData } from '@/types';

interface WordDistributionProps {
  data: WordProgressData;
}

export default function WordDistribution({ data }: WordDistributionProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <ConfidenceChart data={data.by_confidence} />
      <DifficultyDistribution data={data.by_difficulty} />
    </div>
  );
}
