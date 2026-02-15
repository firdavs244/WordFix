import TestGradeBadge from './TestGradeBadge';

interface Props {
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  score: number;
}

const MESSAGES: Record<string, string> = {
  A: 'Outstanding! You nailed it!',
  B: 'Great job! Keep it up!',
  C: 'Good effort. Practice more!',
  D: 'Needs improvement. Try again!',
  F: "Don't give up! Review and retry.",
};

export default function TestResultHeader({ grade, score }: Props) {
  return (
    <div className="text-center">
      <TestGradeBadge grade={grade} score={score} />
      <p className="mt-3 text-sm text-muted-foreground">{MESSAGES[grade]}</p>
    </div>
  );
}
