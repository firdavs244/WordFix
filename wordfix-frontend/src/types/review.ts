import type { ReviewQuality, SessionType, EnrichmentStatus } from './core';
import type { Word } from './word';

// ─── Review & Spaced Repetition Types ──────────────────────────────────────────

export interface ReviewSession {
  id: string;
  user_id: string;
  session_type: SessionType;
  total_words: number;
  correct_count: number;
  incorrect_count: number;
  average_quality: number;
  started_at: string;
  completed_at: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
  // Combo system
  current_combo: number;
  max_combo: number;
  combo_xp_bonus: number;
}

export interface ReviewAnswer {
  word_id: string;
  quality: ReviewQuality;
  response_time_ms?: number;
}

export interface ReviewAnswerResult {
  word: Word;
  session: ReviewSession;
  is_correct: boolean;
  // Combo system
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface ReviewSummary {
  total_reviews: number;
  total_sessions: number;
  words_due: number;
  average_accuracy: number;
  reviews_today: number;
  streak_days: number;
}

export interface DailyStreak {
  id: string;
  current_streak: number;
  longest_streak: number;
  last_activity_date: string | null;
  streak_frozen_until: string | null;
  total_review_days: number;
}

export interface DailyProgress {
  id: string;
  words_reviewed: number;
  words_added: number;
  words_mastered: number;
  correct_answers: number;
  incorrect_answers: number;
  total_time_seconds: number;
  goal_completed: boolean;
  xp_earned: number;
  date: string;
}

export interface EnrichmentStatusResponse {
  enrichment_status: EnrichmentStatus;
  enrichment_error: string;
  is_enriched: boolean;
  enriched_at: string | null;
}

export interface PredictedIntervals {
  [quality: number]: string;
}
