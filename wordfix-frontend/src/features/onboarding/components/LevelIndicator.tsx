import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

const LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const;

const LEVEL_COLORS: Record<string, { bg: string; text: string; ring: string }> = {
  A1: { bg: 'bg-emerald-100 dark:bg-emerald-950', text: 'text-emerald-700 dark:text-emerald-300', ring: 'ring-emerald-500' },
  A2: { bg: 'bg-green-100 dark:bg-green-950', text: 'text-green-700 dark:text-green-300', ring: 'ring-green-500' },
  B1: { bg: 'bg-blue-100 dark:bg-blue-950', text: 'text-blue-700 dark:text-blue-300', ring: 'ring-blue-500' },
  B2: { bg: 'bg-indigo-100 dark:bg-indigo-950', text: 'text-indigo-700 dark:text-indigo-300', ring: 'ring-indigo-500' },
  C1: { bg: 'bg-purple-100 dark:bg-purple-950', text: 'text-purple-700 dark:text-purple-300', ring: 'ring-purple-500' },
  C2: { bg: 'bg-amber-100 dark:bg-amber-950', text: 'text-amber-700 dark:text-amber-300', ring: 'ring-amber-500' },
};

const LEVEL_LABELS: Record<string, string> = {
  A1: 'Beginner',
  A2: 'Elementary',
  B1: 'Intermediate',
  B2: 'Upper-Intermediate',
  C1: 'Advanced',
  C2: 'Proficiency',
};

interface LevelIndicatorProps {
  level: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  animate?: boolean;
}

export function LevelIndicator({ level, size = 'md', showLabel = true, animate = true }: LevelIndicatorProps) {
  const colors = LEVEL_COLORS[level] || LEVEL_COLORS.B1;
  const label = LEVEL_LABELS[level] || level;

  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-12 w-12 text-sm',
    lg: 'h-20 w-20 text-xl',
  };

  const Wrapper = animate ? motion.div : 'div';
  const animationProps = animate
    ? {
        initial: { scale: 0, rotate: -180 },
        animate: { scale: 1, rotate: 0 },
        transition: { type: 'spring' as const, stiffness: 200, damping: 15 },
      }
    : {};

  return (
    <div className="flex flex-col items-center gap-2">
      <Wrapper
        {...animationProps}
        className={cn(
          'flex items-center justify-center rounded-full font-bold ring-2',
          sizeClasses[size],
          colors.bg,
          colors.text,
          colors.ring,
        )}
      >
        {level}
      </Wrapper>
      {showLabel && (
        <span className={cn('font-medium', colors.text, size === 'lg' ? 'text-base' : 'text-sm')}>
          {label}
        </span>
      )}
    </div>
  );
}

export function LevelScale({ currentLevel }: { currentLevel: string }) {
  const currentIndex = LEVELS.indexOf(currentLevel as (typeof LEVELS)[number]);

  return (
    <div className="flex items-center justify-center gap-1">
      {LEVELS.map((level, i) => {
        const colors = LEVEL_COLORS[level];
        const isActive = i === currentIndex;
        const isPast = i < currentIndex;

        return (
          <motion.div
            key={level}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: i * 0.1, type: 'spring', stiffness: 300, damping: 20 }}
            className={cn(
              'flex items-center justify-center rounded-full text-xs font-bold transition-all',
              isActive ? 'h-10 w-10 ring-2' : 'h-7 w-7',
              isActive || isPast ? colors.bg : 'bg-muted',
              isActive || isPast ? colors.text : 'text-muted-foreground',
              isActive ? colors.ring : '',
            )}
          >
            {level}
          </motion.div>
        );
      })}
    </div>
  );
}
