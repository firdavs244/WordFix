import { CheckSquare, PenLine, FileText, Shuffle } from 'lucide-react';
import QuestionTypeCard from './QuestionTypeCard';

const TYPES = [
  { value: 'multiple_choice', icon: CheckSquare, title: 'Multiple Choice', description: 'Choose the correct answer from 4 options' },
  { value: 'fill_blank', icon: PenLine, title: 'Fill in the Blank', description: 'Type the missing word in the sentence' },
  { value: 'context_guess', icon: FileText, title: 'Context Guess', description: 'Determine meaning from context clues' },
  { value: 'mixed', icon: Shuffle, title: 'Mixed', description: 'A blend of all question types' },
] as const;

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export default function QuestionTypeSelector({ value, onChange }: Props) {
  return (
    <div>
      <label className="mb-3 block text-sm font-medium">Question Type</label>
      <div className="grid grid-cols-2 gap-3">
        {TYPES.map((t) => (
          <QuestionTypeCard
            key={t.value}
            value={t.value}
            icon={t.icon}
            title={t.title}
            description={t.description}
            isSelected={value === t.value}
            onClick={() => onChange(t.value)}
          />
        ))}
      </div>
    </div>
  );
}
