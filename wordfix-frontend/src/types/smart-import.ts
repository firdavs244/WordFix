import type { DifficultyLevel } from './core';

// ─── Smart Import Types ────────────────────────────────────────────────────────

export interface WordSuggestion {
  word: string;
  translation: string;
  part_of_speech: string;
  context_sentence: string;
  difficulty: DifficultyLevel;
  reason: string;
  selected?: boolean;
}

export interface AnalyzeTextRequest {
  text: string;
  max_words?: number;
}

export interface AnalyzeTextResponse {
  suggestions: WordSuggestion[];
  total_found: number;
  already_known: number;
  text_length: number;
}

export interface ImportWordsRequest {
  words: {
    original_word: string;
    translation?: string;
    part_of_speech?: string;
    difficulty_level?: DifficultyLevel;
    context_sentence?: string;
    category_id?: string;
  }[];
}

export interface ImportWordsResponse {
  created: number;
  skipped: number;
  errors: { word: string; error: string }[];
}

// ─── CSV Import Types ──────────────────────────────────────────────────────────

export interface CSVValidateResult {
  headers: string[];
  preview: Array<Record<string, string>>;
  total_rows: number;
  valid_rows: number;
  errors: string[];
  has_translation: boolean;
  has_difficulty: boolean;
  has_category: boolean;
}

export interface CSVImportResult {
  total_in_file: number;
  imported: number;
  skipped_duplicate: number;
  skipped_invalid: number;
  errors: string[];
  categories_created: string[];
  xp_earned?: number;
}
