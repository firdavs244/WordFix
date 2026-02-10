import type { TestType, TestDifficulty } from './core';

// ─── Test Types ────────────────────────────────────────────────────────────────

export interface TestQuestion {
  id: string;
  question_type: string;
  question_text: string;
  options: string[];
  order: number;
  user_answer: string;
  is_correct: boolean | null;
  correct_answer: string | null;
  explanation: string | null;
}

export interface TestSession {
  id: string;
  test_type: TestType;
  difficulty: string;
  total_questions: number;
  correct_answers: number;
  incorrect_answers: number;
  score_percentage: number;
  is_completed: boolean;
  started_at: string;
  completed_at: string | null;
  duration_seconds: number;
  created_at: string;
  // Combo system
  current_combo: number;
  max_combo: number;
  combo_xp_bonus: number;
}

export interface TestGenerateRequest {
  test_type: TestType;
  question_count: number;
  difficulty: TestDifficulty;
}

export interface TestGenerateResponse {
  session: TestSession;
  questions: TestQuestion[];
}

export interface TestAnswerRequest {
  question_id: string;
  answer: string;
  response_time_ms?: number;
}

export interface TestAnswerResponse {
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
  // Combo system
  combo: number;
  multiplier: number;
  xp_earned: number;
}

export interface TestDetailResponse {
  session: TestSession;
  questions: TestQuestion[];
}
