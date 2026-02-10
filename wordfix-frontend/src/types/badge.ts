import type { BadgeRarity, BadgeCategory } from './core';

// ─── Badge Types ───────────────────────────────────────────────────────────────

export interface BadgeData {
  id: string;
  code: string;
  name: string;
  description: string;
  icon: string;
  category: BadgeCategory;
  xp_reward: number;
  rarity: BadgeRarity;
  is_earned: boolean;
  earned_at: string | null;
}

export interface UserBadgesResponse {
  badges: BadgeData[];
  earned_count: number;
  total_count: number;
}

export interface NewBadgeInfo {
  code: string;
  name: string;
  icon: string;
}
