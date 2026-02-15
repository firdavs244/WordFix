import WordsSegmentedControl from '@/features/words/components/WordsSegmentedControl';

const OPTIONS = [
  { value: 'easy', label: 'Easy' },
  { value: 'medium', label: 'Medium' },
  { value: 'hard', label: 'Hard' },
  { value: 'adaptive', label: 'Adaptive' },
];

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export default function DifficultySelector({ value, onChange }: Props) {
  return (
    <div>
      <label className="mb-3 block text-sm font-medium">Difficulty</label>
      <WordsSegmentedControl options={OPTIONS} value={value} onChange={onChange} size="md" />
    </div>
  );
}
