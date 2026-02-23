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

// ─── Story Builder Types ───────────────────────────────────────────────────────

export interface StoryStartResponse {
  session_id: string;
  genre: string;
  ai_text: string;
  target_words: string[];
  total_rounds: number;
  current_round: number;
  all_target_words: string[];
}

export interface StoryRoundResult {
  score: number;
  words_used: string[];
  grammar_corrections: Array<{
    original: string;
    corrected: string;
    explanation: string;
  }>;
  feedback: string;
  is_correct_usage: boolean;
}

export interface StorySubmitResponse {
  round_result: StoryRoundResult;
  next_round: { ai_text: string; target_words: string[]; round_number: number } | null;
  session_stats: { total_score: number; rounds_completed: number };
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface StoryCompleteResponse {
  total_score: number;
  max_score: number;
  rounds: Array<{
    round_number: number;
    score: number;
    words_used: string[];
    corrections: any[];
  }>;
  full_story: string;
  xp_earned: number;
}

// ─── Listening Challenge Types ─────────────────────────────────────────────────

export interface ListeningStartResponse {
  session_id: string;
  total_rounds: number;
  current_round: number;
  first_word: {
    round_number: number;
    audio_url: string;
    hint: string;
    difficulty: string;
    max_attempts: number;
  };
}

export interface ListeningAnswerResponse {
  is_correct: boolean;
  score: number;
  attempts_used: number;
  attempts_remaining: number;
  hint: string;
  correct_answer: string;
  next_round: {
    round_number: number;
    audio_url: string;
    hint: string;
    max_attempts: number;
  } | null;
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface ListeningCompleteResponse {
  total_score: number;
  max_score: number;
  rounds: Array<{
    word: string;
    is_correct: boolean;
    attempts_used: number;
    score: number;
  }>;
  accuracy_pct: number;
  xp_earned: number;
}

// ─── Synonym & Antonym Types ───────────────────────────────────────────────────

export interface SynonymAntonymRound {
  round_number: number;
  word: string;
  question_type: 'synonym' | 'antonym';
  options: string[];
}

export interface SynonymAntonymStartResponse {
  session_id: string;
  total_rounds: number;
  current_round: number;
  rounds: SynonymAntonymRound[];
}

export interface SynonymAntonymAnswerResponse {
  is_correct: boolean;
  correct_answer: string;
  score: number;
  next_round: SynonymAntonymRound | null;
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface SynonymAntonymCompleteResponse {
  total_score: number;
  max_score: number;
  rounds: Array<{
    round_number: number;
    word: string;
    question_type: string;
    correct_answer: string;
    user_answer: string;
    is_correct: boolean;
    score: number;
  }>;
  accuracy_pct: number;
  xp_earned: number;
  badges_earned: Array<{ code: string; name: string; icon: string }>;
}

// ─── Irregular Verbs Types ──────────────────────────────────────────────────────

export interface IrregularVerbRound {
  round_number: number;
  infinitive: string;
  translation: string;
  max_attempts: number;
}

export interface IrregularVerbsStartResponse {
  session_id: string;
  total_rounds: number;
  current_round: number;
  tier: string;
  rounds: IrregularVerbRound[];
}

export interface IrregularVerbAnswerResponse {
  past_simple_correct: boolean;
  past_participle_correct: boolean;
  correct_past_simple: string;
  correct_past_participle: string;
  score: number;
  attempts_used: number;
  attempts_remaining: number;
  hints: Record<string, string>;
  next_round: IrregularVerbRound | null;
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface IrregularVerbsCompleteResponse {
  total_score: number;
  max_score: number;
  rounds: Array<{
    round_number: number;
    infinitive: string;
    translation: string;
    correct_past_simple: string;
    correct_past_participle: string;
    user_past_simple: string;
    user_past_participle: string;
    past_simple_correct: boolean;
    past_participle_correct: boolean;
    score: number;
  }>;
  accuracy_pct: number;
  xp_earned: number;
  badges_earned: Array<{ code: string; name: string; icon: string }>;
}
