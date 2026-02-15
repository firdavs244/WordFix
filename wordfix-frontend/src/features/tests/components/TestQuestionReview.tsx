import TestQuestionReviewItem from './TestQuestionReviewItem';
import type { TestQuestion } from '@/types';

interface Props {
  questions: TestQuestion[];
}

export default function TestQuestionReview({ questions }: Props) {
  return (
    <div data-testid="question-review">
      <h3 className="mb-3 text-sm font-semibold">Question Review</h3>
      <div className="space-y-2">
        {questions.map((q, i) => (
          <TestQuestionReviewItem key={q.id} question={q} index={i} />
        ))}
      </div>
    </div>
  );
}
