// ─── Daily Challenge Types ─────────────────────────────────────────────────────

export interface Challenge {
  type: string;
  target: number;
  current: number;
  xp_reward: number;
  completed: boolean;
  title: string;
  icon: string;
}

export interface DailyChallenges {
  date: string;
  challenges: Challenge[];
  all_completed: boolean;
  bonus_claimed: boolean;
}
