import { motion } from 'framer-motion';
import type { ReviewQuality } from '@/types';

interface Props {
  quality: ReviewQuality;
  emoji: string;
  label: string;
  shortcut: string;
  onRate: (q: ReviewQuality) => void;
}

export default function QualityButton({ quality, emoji, label, shortcut, onRate }: Props) {
  return (
    <motion.button
      whileTap={{ scale: 0.93 }}
      onClick={() => onRate(quality)}
      className="flex h-14 flex-col items-center justify-center gap-0.5 rounded-xl border border-border/50 transition-colors hover:bg-muted/50 active:scale-95 lg:h-16"
    >
      <span className="text-lg lg:text-xl">{emoji}</span>
      <span className="text-[10px] font-medium text-muted-foreground">{label}</span>
      <span className="hidden text-[8px] text-muted-foreground/30 lg:block">{shortcut}</span>
    </motion.button>
  );
}
