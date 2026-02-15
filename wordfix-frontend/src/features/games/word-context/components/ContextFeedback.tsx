import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, ArrowRight } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface Props {
  isCorrect: boolean;
  explanation?: string;
  onNext: () => void;
  isLast: boolean;
}

export default function ContextFeedback({ isCorrect, explanation, onNext, isLast }: Props) {
  return (
    <motion.div variants={fadeInUp} initial="initial" animate="animate" className="mt-4">
      <div className={cn(
        'rounded-xl border p-4',
        isCorrect ? 'border-success/15 bg-success/[0.06]' : 'border-destructive/15 bg-destructive/[0.06]',
      )}>
        <div className="flex items-center gap-2">
          {isCorrect ? (
            <><CheckCircle2 className="h-[18px] w-[18px] text-success" /><span className="font-semibold text-success">Correct!</span></>
          ) : (
            <><XCircle className="h-[18px] w-[18px] text-destructive" /><span className="font-semibold text-destructive">Incorrect</span></>
          )}
        </div>
        {explanation && <p className="mt-2 text-sm text-muted-foreground">{explanation}</p>}
        <button
          type="button" onClick={onNext}
          className="mt-3 flex h-9 items-center gap-2 rounded-lg bg-primary px-3 text-sm font-medium text-white"
        >
          {isLast ? 'See Results' : 'Next'} <ArrowRight className="h-3.5 w-3.5" />
        </button>
      </div>
    </motion.div>
  );
}
