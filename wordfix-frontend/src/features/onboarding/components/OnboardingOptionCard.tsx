import { motion } from 'framer-motion';
import { CheckCircle2 } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface Props {
  text: string;
  isSelected: boolean;
  onClick: () => void;
  index: number;
}

export function OnboardingOptionCard({ text, isSelected, onClick, index: _index }: Props) {
  return (
    <motion.button
      variants={staggerItem}
      onClick={onClick}
      whileTap={{ scale: 0.98 }}
      className={cn(
        'flex w-full items-center justify-between rounded-xl p-4 text-left transition-all duration-200',
        isSelected
          ? 'border border-primary bg-primary/[0.06] text-sm font-semibold text-primary shadow-card ring-2 ring-primary/15'
          : 'border border-border/50 bg-card text-sm font-medium shadow-sm hover:border-border hover:bg-muted/30 hover:shadow-card',
      )}
    >
      <span>{text}</span>
      {isSelected && (
        <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 300, damping: 15 }}>
          <CheckCircle2 className="h-[18px] w-[18px] text-primary" />
        </motion.span>
      )}
    </motion.button>
  );
}
