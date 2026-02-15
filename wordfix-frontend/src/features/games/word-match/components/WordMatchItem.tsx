import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Check } from 'lucide-react';

interface Props {
  text: string;
  type: 'word' | 'translation';
  isSelected: boolean;
  isMatched: boolean;
  isWrong: boolean;
  onClick: () => void;
}

export default function WordMatchItem({ text, type, isSelected, isMatched, isWrong, onClick }: Props) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      disabled={isMatched}
      animate={isWrong ? { x: [0, -4, 4, -3, 3, 0] } : {}}
      transition={isWrong ? { duration: 0.3 } : undefined}
      className={cn(
        'relative w-full rounded-xl border p-3 text-center text-sm font-medium transition-all',
        isMatched && 'opacity-30 border-success/50 bg-success/10',
        isSelected && !isMatched && 'border-primary bg-primary/[0.05] ring-2 ring-primary/20 shadow-glow-primary/10',
        isWrong && 'border-destructive bg-destructive/10',
        !isSelected && !isMatched && !isWrong && 'border-border/50 bg-card hover:border-border hover:bg-muted/30',
      )}
      data-testid={`match-${type}-${text}`}
    >
      {text}
      {isMatched && (
        <Check className="absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-success" />
      )}
    </motion.button>
  );
}
