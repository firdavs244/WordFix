import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { BadgeData, BadgeRarity } from '@/types';
import BadgeRarityGlow from './BadgeRarityGlow';
import BadgeIcon from './BadgeIcon';

interface BadgeCardEarnedProps {
  badge: BadgeData;
}

const rarityBorders: Record<BadgeRarity, string> = {
  common: 'border border-border/50',
  rare: 'border border-blue-500/30',
  epic: 'border border-violet-500/30',
  legendary: 'border border-amber-500/30',
};

const rarityLabels: Record<BadgeRarity, string> = {
  common: 'text-slate-400',
  rare: 'text-blue-400',
  epic: 'text-violet-400',
  legendary: 'text-amber-400',
};

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const days = Math.floor(diff / 86400000);
  if (days < 1) return 'Today';
  if (days === 1) return '1 day ago';
  if (days < 30) return `${days} days ago`;
  return `${Math.floor(days / 30)}mo ago`;
}

export default function BadgeCardEarned({ badge }: BadgeCardEarnedProps) {
  return (
    <BadgeRarityGlow rarity={badge.rarity} active>
      <motion.div
        className={cn('rounded-2xl p-5 text-center relative overflow-hidden bg-card', rarityBorders[badge.rarity])}
        whileHover={{ scale: 1.03 }}
        transition={{ type: 'spring', stiffness: 400, damping: 25 }}
      >
        <span className={cn('absolute top-3 right-3 text-[8px] uppercase tracking-widest font-bold', rarityLabels[badge.rarity])}>
          {badge.rarity}
        </span>
        <div className="flex justify-center">
          <BadgeIcon earned />
        </div>
        <p className="text-sm font-heading font-semibold mt-3">{badge.name}</p>
        <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{badge.description}</p>
        <p className="text-[10px] font-semibold text-accent mt-2">+{badge.xp_reward} XP</p>
        {badge.earned_at && (
          <p className="text-[9px] text-muted-foreground/40 mt-1">{timeAgo(badge.earned_at)}</p>
        )}
      </motion.div>
    </BadgeRarityGlow>
  );
}
