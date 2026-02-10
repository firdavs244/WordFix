// ─── XP & Progress Types ──────────────────────────────────────────────────────

export interface UserProgressData {
  level: number;
  total_xp: number;
  xp_for_current: number;
  xp_for_next: number;
  progress_pct: number;
  xp_progress: number;
  xp_needed: number;
  words_learned_total: number;
  words_mastered_total: number;
  tests_completed: number;
  games_played: number;
  reviews_completed: number;
  perfect_scores: number;
  total_study_time_seconds: number;
}

export interface XPHistoryEntry {
  date: string;
  xp: number;
}

export interface XPResult {
  new_total: number;
  level_up: boolean;
  new_level: number;
  xp_gained: number;
}
