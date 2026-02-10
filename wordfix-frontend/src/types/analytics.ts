// ─── Analytics Types ───────────────────────────────────────────────────────────

export interface AnalyticsOverview {
  total_words: number;
  mastered_words: number;
  mastered_percentage: number;
  total_reviews: number;
  total_correct: number;
  overall_accuracy: number;
  total_study_time_formatted: string;
  total_xp: number;
  current_level: number;
  current_streak: number;
  longest_streak: number;
  tests_completed: number;
  games_played: number;
  avg_daily_words: number;
  avg_daily_time: number;
  member_since_days: number;
}

export interface DailyStatsEntry {
  date: string;
  words_reviewed: number;
  words_added: number;
  correct_answers: number;
  incorrect_answers: number;
  xp_earned: number;
  total_time_seconds: number;
}

export interface DifficultWord {
  id: string;
  original_word: string;
  translation: string;
  accuracy_rate: number;
  review_count: number;
  incorrect_count: number;
  confidence_score: number;
}

export interface WordProgressData {
  by_confidence: Record<string, number>;
  by_difficulty: Record<string, number>;
  by_category: { name: string; count: number; color: string }[];
  recently_mastered: { word: string; mastered_at: string }[];
  needs_attention: { word: string; accuracy: number }[];
}

export interface CalendarDay {
  date: string;
  active: boolean;
  words_reviewed: number;
  xp_earned: number;
  goal_completed: boolean;
}
