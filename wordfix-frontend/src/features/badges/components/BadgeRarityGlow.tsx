import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import type { BadgeRarity } from '@/types';

interface BadgeRarityGlowProps {
  rarity: BadgeRarity;
  active?: boolean;
  children: ReactNode;
}

const glowColors: Record<BadgeRarity, string> = {
  common: '',
  rare: 'bg-blue-500/10',
  epic: 'bg-violet-500/10',
  legendary: 'bg-amber-500/15',
};

export default function BadgeRarityGlow({ rarity, active = false, children }: BadgeRarityGlowProps) {
  const showGlow = active && rarity !== 'common';

  return (
    <div className="relative">
      {showGlow && (
        <div
          className={cn(
            'absolute inset-0 z-0 rounded-2xl blur-[20px] transition-opacity duration-500',
            glowColors[rarity],
            rarity === 'legendary' ? 'opacity-40 animate-pulse' : 'opacity-30',
          )}
        />
      )}
      <div className="relative z-10">{children}</div>
    </div>
  );
}
