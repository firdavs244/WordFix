import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface TopicChipProps {
  emoji: string;
  label: string;
  isSelected: boolean;
  onClick: () => void;
}

export default function TopicChip({ emoji, label, isSelected, onClick }: TopicChipProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-1.5 rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-200',
        isSelected
          ? 'bg-primary/10 border border-primary/30 text-primary font-semibold ring-2 ring-primary/10'
          : 'bg-muted/50 border border-border/30 hover:bg-muted hover:border-border hover:shadow-sm',
      )}
    >
      <span className="text-base">{emoji}</span>
      <span>{label}</span>
    </motion.button>
  );
}
