import type { GameType } from './core';

// ─── Game Types ────────────────────────────────────────────────────────────────

export interface GameSession {
  id: string;
  game_type: GameType;
  score: number;
  max_score: number;
  correct_answers: number;
  incorrect_answers: number;
  total_questions: number;
  duration_seconds: number;
  level: number;
  xp_earned: number;
  is_completed: boolean;
  started_at: string;
  completed_at: string | null;
  created_at: string;
  // Combo system
  current_combo: number;
  max_combo: number;
  combo_xp_bonus: number;
}

export interface SpeedRoundWord {
  word_id: string;
  word: string;
  options: string[];
  correct_translation: string;
}

export interface SpeedRoundStartResponse {
  session_id: string;
  words: SpeedRoundWord[];
  time_limit: number;
}

export interface SpeedRoundAnswer {
  word_id: string;
  selected_answer: string;
}

export interface WordMatchStartResponse {
  session_id: string;
  words: { word_id: string; word: string }[];
  translations: string[];
  pair_count: number;
}

export interface WordMatchPair {
  word_id: string;
  matched_translation: string;
}

export interface WordContextQuestion {
  word_id: string;
  context: string;
  correct_answer: string;
  options: string[];
  hint?: string;
  explanation?: string;
}

export interface WordContextStartResponse {
  session_id: string;
  questions: WordContextQuestion[];
}

export interface WordContextAnswer {
  word_id: string;
  selected_answer: string;
}

export interface GameStats {
  total_games: number;
  total_xp: number;
  favorite_game: string;
  by_type: Record<string, { games_played: number; best_score: number; total_xp: number }>;
}
