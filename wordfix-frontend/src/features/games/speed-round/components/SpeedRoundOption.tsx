import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Props {
  text: string;
  index: number;
  state: 'default' | 'correct' | 'wrong';
  disabled: boolean;
  onClick: () => void;
}

export default function SpeedRoundOption({ text, index, state, disabled, onClick }: Props) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      disabled={disabled}
      whileTap={{ scale: 0.95 }}
      animate={state === 'wrong' ? { x: [0, -6, 6, -4, 4, 0] } : {}}
      transition={state === 'wrong' ? { duration: 0.3 } : undefined}
      className={cn(
        'flex h-14 w-full items-center justify-center rounded-xl border text-sm font-semibold transition-all',
        state === 'default' && 'border-border/50 bg-card hover:border-border hover:bg-muted/30',
        state === 'correct' && 'scale-105 border-success bg-success/10 text-success',
        state === 'wrong' && 'border-destructive bg-destructive/10 text-destructive',
        disabled && 'cursor-default',
      )}
      data-testid={`speed-option-${index}`}
    >
      {text}
    </motion.button>
  );
}
