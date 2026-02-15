import { useState } from 'react';
import { Sparkles } from 'lucide-react';
import QuestionTypeSelector from './QuestionTypeSelector';
import DifficultySelector from './DifficultySelector';
import QuestionCountSlider from './QuestionCountSlider';
import TestGenerateButton from './TestGenerateButton';
import { useGenerateTest } from '../hooks/useTests';
import type { TestType, TestDifficulty } from '@/types';

export default function TestConfigPanel() {
  const [questionType, setQuestionType] = useState<string>('multiple_choice');
  const [difficulty, setDifficulty] = useState<string>('medium');
  const [count, setCount] = useState(10);
  const generate = useGenerateTest();

  const handleGenerate = () => {
    generate.mutate({
      test_type: questionType as TestType,
      question_count: count,
      difficulty: difficulty as TestDifficulty,
    });
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br from-primary/[0.02] to-transparent p-6 shadow-card lg:p-8">
      <Sparkles className="absolute right-4 top-4 h-20 w-20 rotate-12 text-foreground opacity-[0.03]" />
      <div className="relative space-y-6">
        <QuestionTypeSelector value={questionType} onChange={setQuestionType} />
        <DifficultySelector value={difficulty} onChange={setDifficulty} />
        <QuestionCountSlider value={count} onChange={setCount} />
        <TestGenerateButton onGenerate={handleGenerate} isLoading={generate.isPending} />
      </div>
    </div>
  );
}
