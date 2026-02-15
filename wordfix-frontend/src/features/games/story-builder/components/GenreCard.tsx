import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Props {
  genre: string;
  icon: string;
  gradient: string;
  isSelected: boolean;
  onClick: () => void;
}

export default function GenreCard({ genre, icon, gradient, isSelected, onClick }: Props) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      whileTap={{ scale: 0.95 }}
      className={cn(
        'flex flex-col items-center gap-2 rounded-xl border p-4 transition-all',
        isSelected
          ? 'border-primary bg-primary/[0.05] ring-2 ring-primary/10'
          : 'border-border/50 bg-card hover:border-border hover:bg-muted/30',
      )}
    >
      <span className={`flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${gradient} text-xl`}>
        {icon}
      </span>
      <span className="text-sm font-medium capitalize">{genre}</span>
    </motion.button>
  );
}
