import type { ProficiencyLevel } from '@/types/core';

// ─── Onboarding Types ──────────────────────────────────────────────────────────

export interface OnboardingQuestion {
  id: string;
  level: ProficiencyLevel;
  question_text: string;
  options: string[];
  order: number;
}

export interface OnboardingAnswer {
  question_id: string;
  answer: string;
}

export interface OnboardingResult {
  determined_level: ProficiencyLevel;
  total_correct: number;
  total_questions: number;
  message: string;
  xp_earned?: number;
}

export interface OnboardingStatus {
  completed: boolean;
  has_completed_onboarding: boolean;
  determined_level?: ProficiencyLevel;
  total_correct?: number;
  total_questions?: number;
}
