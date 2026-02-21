import { motion } from 'framer-motion';
import { PenLine } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import type { ChatCorrection as CorrectionType } from '@/types';

interface ChatCorrectionProps {
  correction: CorrectionType;
}

export default function ChatCorrection({ correction }: ChatCorrectionProps) {
  return (
    <motion.div
      variants={fadeInUp}
      initial="initial"
      animate="animate"
      className="ml-[38px] mt-1 max-w-[75%] rounded-xl border border-warning/15 bg-warning/[0.06] p-3"
    >
      <div className="flex items-center gap-1.5">
        <PenLine className="h-3 w-3 text-warning" />
        <span className="text-[10px] font-semibold uppercase tracking-wide text-warning">Correction</span>
      </div>
      <p className="mt-1.5 text-sm text-destructive/70 line-through">{correction.original}</p>
      <p className="mt-0.5 text-sm font-medium text-success">{correction.corrected}</p>
      {correction.explanation && (
        <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{correction.explanation}</p>
      )}
    </motion.div>
  );
}
