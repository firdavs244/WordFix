import { useId } from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, List } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Props {
  view: 'grid' | 'list';
  onChange: (v: 'grid' | 'list') => void;
}

const views = [
  { value: 'grid' as const, icon: LayoutGrid },
  { value: 'list' as const, icon: List },
];

export default function WordsViewToggle({ view, onChange }: Props) {
  const id = useId();
  return (
    <div className="inline-flex rounded-xl bg-muted/50 p-1">
      {views.map(({ value, icon: Icon }) => (
        <button
          key={value}
          onClick={() => onChange(value)}
          aria-label={`${value} view`}
          className={cn(
            'relative flex h-8 w-8 items-center justify-center rounded-lg',
            view === value ? 'text-foreground' : 'text-muted-foreground hover:text-foreground/70',
          )}
        >
          {view === value && (
            <motion.div
              layoutId={`view-${id}`}
              className="absolute inset-0 rounded-lg border border-border/30 bg-card shadow-sm"
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
          <Icon className="relative z-10 h-4 w-4" strokeWidth={1.75} />
        </button>
      ))}
    </div>
  );
}
