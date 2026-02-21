import type { BadgeData } from '@/types';
import BadgeIcon from './BadgeIcon';

interface BadgeCardLockedProps {
  badge: BadgeData;
}

export default function BadgeCardLocked({ badge }: BadgeCardLockedProps) {
  return (
    <div className="rounded-2xl border border-border/30 p-5 text-center opacity-50 bg-muted/20">
      <div className="flex justify-center">
        <BadgeIcon earned={false} />
      </div>
      <p className="text-sm font-heading font-semibold mt-3 text-muted-foreground">{badge.name}</p>
      <p className="text-xs text-muted-foreground/60 mt-1 line-clamp-2">{badge.description}</p>
      <p className="text-[10px] text-muted-foreground/40 mt-2">+{badge.xp_reward} XP</p>
    </div>
  );
}
