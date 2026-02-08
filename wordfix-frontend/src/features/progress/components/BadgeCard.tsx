import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { BadgeData, BadgeRarity } from '@/types';

const rarityColors: Record<BadgeRarity, { bg: string; border: string; text: string }> = {
  common: { bg: 'bg-slate-100 dark:bg-slate-800', border: 'border-slate-300 dark:border-slate-600', text: 'text-slate-600 dark:text-slate-400' },
  rare: { bg: 'bg-blue-50 dark:bg-blue-950', border: 'border-blue-300 dark:border-blue-700', text: 'text-blue-600 dark:text-blue-400' },
  epic: { bg: 'bg-purple-50 dark:bg-purple-950', border: 'border-purple-300 dark:border-purple-700', text: 'text-purple-600 dark:text-purple-400' },
  legendary: { bg: 'bg-amber-50 dark:bg-amber-950', border: 'border-amber-300 dark:border-amber-700', text: 'text-amber-600 dark:text-amber-400' },
};

const rarityLabels: Record<BadgeRarity, string> = {
  common: 'Common',
  rare: 'Rare',
  epic: 'Epic',
  legendary: 'Legendary',
};

interface BadgeCardProps {
  badge: BadgeData;
}

export function BadgeCard({ badge }: BadgeCardProps) {
  const colors = rarityColors[badge.rarity];
  const isEarned = badge.is_earned;

  return (
    <motion.div
      className={cn(
        'relative flex flex-col items-center rounded-xl border-2 p-4 transition-all',
        isEarned
          ? `${colors.bg} ${colors.border}`
          : 'border-border/50 bg-muted/30 opacity-50 grayscale',
      )}
      whileHover={isEarned ? { scale: 1.03, y: -2 } : undefined}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      {/* Rarity indicator */}
      <div className={cn('absolute -top-2 right-2 rounded-full px-2 py-0.5 text-[10px] font-bold uppercase', colors.bg, colors.text)}>
        {rarityLabels[badge.rarity]}
      </div>

      {/* Icon */}
      <div className={cn(
        'flex h-14 w-14 items-center justify-center rounded-2xl text-2xl',
        isEarned ? colors.bg : 'bg-muted',
      )}>
        {isEarned ? '🏆' : '🔒'}
      </div>

      {/* Name */}
      <h3 className="mt-3 text-center text-sm font-semibold">{badge.name}</h3>

      {/* Description */}
      <p className="mt-1 text-center text-xs text-muted-foreground">{badge.description}</p>

      {/* XP Reward */}
      <div className="mt-2 flex items-center gap-1 text-xs">
        <span className={cn('font-medium', isEarned ? 'text-primary' : 'text-muted-foreground')}>
          +{badge.xp_reward} XP
        </span>
      </div>

      {/* Earned date */}
      {isEarned && badge.earned_at && (
        <p className="mt-1 text-[10px] text-muted-foreground">
          {new Date(badge.earned_at).toLocaleDateString()}
        </p>
      )}
    </motion.div>
  );
}
