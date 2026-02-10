// ─── Core Types ────────────────────────────────────────────────────────────────

export type Theme = 'light' | 'dark' | 'system';

export type DifficultyLevel = 'easy' | 'medium' | 'hard';

export type ProficiencyLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';

export type ReviewQuality = 0 | 1 | 2 | 3 | 4 | 5;

export type SessionType = 'review' | 'learn' | 'mixed';

export type EnrichmentStatus = 'pending' | 'processing' | 'enriched' | 'failed';

export type TestType = 'multiple_choice' | 'fill_blank' | 'context_guess' | 'mixed';
export type TestDifficulty = 'easy' | 'medium' | 'hard' | 'adaptive';

export type GameType = 'speed_round' | 'word_match' | 'word_context';

export type BadgeRarity = 'common' | 'rare' | 'epic' | 'legendary';
export type BadgeCategory = 'words' | 'streak' | 'review' | 'test' | 'game' | 'mastery' | 'level';

export type NotificationType =
  | 'review_reminder'
  | 'streak_warning'
  | 'badge_earned'
  | 'level_up'
  | 'daily_goal_complete'
  | 'word_mastered'
  | 'weekly_report';
