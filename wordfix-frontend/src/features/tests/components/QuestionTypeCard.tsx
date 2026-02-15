import { Check, type LucideIcon } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Props {
  value: string;
  icon: LucideIcon;
  title: string;
  description: string;
  isSelected: boolean;
  onClick: () => void;
}

export default function QuestionTypeCard({ icon: Icon, title, description, isSelected, onClick }: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'relative w-full cursor-pointer rounded-xl border p-4 text-left transition-all duration-200',
        isSelected
          ? 'border-primary bg-primary/[0.05] ring-2 ring-primary/10'
          : 'border-border/50 bg-card hover:border-border hover:bg-muted/30',
      )}
    >
      {isSelected && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 12 }}
          className="absolute right-3 top-3 flex h-[18px] w-[18px] items-center justify-center rounded-full bg-primary"
        >
          <Check className="h-2.5 w-2.5 text-white" />
        </motion.div>
      )}
      <Icon className={cn('h-5 w-5', isSelected ? 'text-primary' : 'text-muted-foreground')} />
      <p className={cn('mt-2 text-sm font-semibold', isSelected && 'text-primary')}>{title}</p>
      <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>
    </button>
  );
}
