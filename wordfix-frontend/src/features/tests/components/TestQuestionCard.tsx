import { motion } from 'framer-motion';
import { slideInRight } from '@/lib/motion';
import MultipleChoiceQuestion from './MultipleChoiceQuestion';
import FillBlankQuestion from './FillBlankQuestion';
import AnswerFeedbackPanel from './AnswerFeedbackPanel';
import type { TestQuestion } from '@/types';

interface Props {
  question: TestQuestion;
  onAnswer: (answer: string, index?: number) => void;
  answered: boolean;
  feedback?: { isCorrect: boolean; correctAnswer: string; explanation: string } | null;
  selectedIndex?: number;
  correctIndex?: number;
  onNext: () => void;
  isLast: boolean;
}

export default function TestQuestionCard({
  question, onAnswer, answered, feedback, selectedIndex, correctIndex, onNext, isLast,
}: Props) {
  const isMC = question.question_type === 'multiple_choice' || question.question_type === 'context_guess';

  return (
    <motion.div variants={slideInRight} initial="initial" animate="animate" exit="exit">
      <div className="rounded-2xl border border-border/50 p-6 shadow-card lg:p-8">
        <p className="mb-6 font-heading text-lg font-semibold leading-snug lg:text-xl">
          {question.question_text}
        </p>

        {isMC ? (
          <MultipleChoiceQuestion
            options={question.options}
            onSelect={(i) => onAnswer(question.options[i], i)}
            selectedIndex={selectedIndex}
            correctIndex={correctIndex}
            answered={answered}
          />
        ) : (
          <FillBlankQuestion
            sentence={question.question_text}
            onSubmit={(val) => onAnswer(val)}
            answered={answered}
            correctAnswer={feedback?.correctAnswer}
            userAnswer={question.user_answer}
            isCorrect={feedback?.isCorrect}
          />
        )}

        {feedback && (
          <AnswerFeedbackPanel
            isCorrect={feedback.isCorrect}
            correctAnswer={feedback.correctAnswer}
            explanation={feedback.explanation}
            onNext={onNext}
            isLast={isLast}
          />
        )}
      </div>
    </motion.div>
  );
}
