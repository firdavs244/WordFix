import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, ArrowRight, BarChart3 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { fadeInUp } from '@/lib/motion';

interface Props {
  isCorrect: boolean;
  correctAnswer?: string;
  explanation?: string;
  onNext: () => void;
  isLast: boolean;
}

export default function AnswerFeedbackPanel({ isCorrect, correctAnswer, explanation, onNext, isLast }: Props) {
  return (
    <motion.div variants={fadeInUp} initial="initial" animate="animate" className="mt-4" data-testid="answer-feedback">
      <div className={cn(
        'rounded-xl border p-4',
        isCorrect ? 'border-success/15 bg-success/[0.06]' : 'border-destructive/15 bg-destructive/[0.06]',
      )}>
        <div className="flex items-center gap-2">
          {isCorrect ? (
            <>
              <CheckCircle2 className="h-[18px] w-[18px] text-success" />
              <span className="font-semibold text-success">Correct!</span>
            </>
          ) : (
            <>
              <XCircle className="h-[18px] w-[18px] text-destructive" />
              <span className="font-semibold text-destructive">Incorrect</span>
            </>
          )}
        </div>
        {!isCorrect && correctAnswer && (
          <p className="mt-1 text-sm">Correct answer: <span className="font-medium">{correctAnswer}</span></p>
        )}
        {explanation && (
          <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{explanation}</p>
        )}
        <button
          type="button"
          onClick={onNext}
          className="mt-3 flex h-10 items-center gap-2 rounded-xl bg-primary px-4 text-sm font-medium text-white"
        >
          {isLast ? (
            <><BarChart3 className="h-4 w-4" />See Results</>
          ) : (
            <><ArrowRight className="h-4 w-4" />Next Question</>
          )}
        </button>
      </div>
    </motion.div>
  );
}
