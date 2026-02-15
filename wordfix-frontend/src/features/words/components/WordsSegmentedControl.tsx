import { useId } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Option {
  value: string;
  label: string;
}

interface Props {
  options: Option[];
  value: string;
  onChange: (v: string) => void;
  size?: 'sm' | 'md';
}

export default function WordsSegmentedControl({ options, value, onChange, size = 'sm' }: Props) {
  const id = useId();

  return (
    <div className="relative inline-flex rounded-xl bg-muted/50 p-1" role="radiogroup">
      {options.map((opt) => (
        <button
          key={opt.value}
          role="radio"
          aria-checked={value === opt.value}
          onClick={() => onChange(opt.value)}
          className={cn(
            'relative z-10 cursor-pointer transition-colors duration-200',
            size === 'sm' ? 'px-3 py-1.5 text-xs' : 'px-4 py-2 text-sm',
            'font-medium',
            value === opt.value ? 'text-foreground' : 'text-muted-foreground hover:text-foreground/70',
          )}
        >
          {value === opt.value && (
            <motion.div
              layoutId={`seg-${id}`}
              className="absolute inset-0 rounded-lg border border-border/30 bg-card shadow-sm"
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
          <span className="relative z-10">{opt.label}</span>
        </button>
      ))}
    </div>
  );
}
