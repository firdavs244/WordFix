import { cn } from '@/lib/utils';
import { Check, X } from 'lucide-react';
import { motion } from 'framer-motion';
import { shake } from '@/lib/motion';

interface Props {
  text: string;
  index: number;
  isSelected: boolean;
  isCorrect: boolean | null;
  isWrong: boolean | null;
  disabled: boolean;
  onClick: () => void;
}

const LETTERS = ['A', 'B', 'C', 'D'];

export default function MultipleChoiceOption({
  text, index, isSelected, isCorrect, isWrong, disabled, onClick,
}: Props) {
  const base = 'w-full rounded-xl border p-4 text-left transition-all duration-200 flex items-center';
  const letterBase = 'mr-3 inline-flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg text-xs font-bold';

  const style = isCorrect
    ? 'border-success bg-success/[0.06]'
    : isWrong
      ? 'border-destructive bg-destructive/[0.06]'
      : isSelected
        ? 'border-primary bg-primary/[0.05] ring-2 ring-primary/10'
        : 'border-border/50 bg-card hover:border-border hover:bg-muted/30';

  const letterStyle = isCorrect
    ? 'bg-success text-white'
    : isWrong
      ? 'bg-destructive text-white'
      : isSelected
        ? 'bg-primary text-white'
        : 'bg-muted text-muted-foreground';

  const Wrapper = isWrong ? motion.button : 'button';
  const motionProps = isWrong ? { animate: shake.animate } : {};

  return (
    <Wrapper
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={cn(base, style, disabled && 'cursor-default')}
      data-testid={`option-${index}`}
      {...motionProps}
    >
      <span className={cn(letterBase, letterStyle)}>{LETTERS[index]}</span>
      <span className="flex-1 text-sm">{text}</span>
      {isCorrect && <Check className="ml-2 h-4 w-4 flex-shrink-0 text-success" data-testid="check-icon" />}
      {isWrong && <X className="ml-2 h-4 w-4 flex-shrink-0 text-destructive" data-testid="x-icon" />}
    </Wrapper>
  );
}
