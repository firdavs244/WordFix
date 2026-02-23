import type { DifficultyLevel, EnrichmentStatus } from './core';

// ─── Word Types ────────────────────────────────────────────────────────────────

export interface WordCategory {
  id: string;
  user_id: string;
  name: string;
  color: string;
  icon: string;
  words_count: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Word {
  id: string;
  user_id: string;
  original_word: string;
  translation: string;
  pronunciation: string;
  part_of_speech: string;
  definition: string;
  example_sentence: string;
  example_translation: string;
  synonyms: string[];
  antonyms: string[];
  collocations: string[];
  word_family: string[];
  image_url: string;
  audio_url: string;
  notes: string;
  category_id: string | null;
  category: WordCategory | null;
  tags: string[];
  difficulty_level: DifficultyLevel;
  is_enriched: boolean;
  confidence_score: number;
  next_review_at: string | null;
  review_count: number;
  correct_count: number;
  incorrect_count: number;
  last_reviewed_at: string | null;
  is_mastered: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  accuracy_rate: number;
  // Sprint 3: Enrichment & SR fields
  mnemonic: string;
  usage_notes: string;
  enrichment_status: EnrichmentStatus;
  enrichment_error: string;
  enriched_at: string | null;
  easiness_factor: number;
  repetition_number: number;
  interval_days: number;
  // Archive fields
  is_archived: boolean;
  archived_at: string | null;
}

export interface WordCreateData {
  original_word: string;
  translation?: string;
  pronunciation?: string;
  part_of_speech?: string;
  definition?: string;
  example_sentence?: string;
  notes?: string;
  difficulty_level?: DifficultyLevel;
  category_id?: string;
  tags?: string[];
}

export interface WordUpdateData {
  translation?: string;
  pronunciation?: string;
  part_of_speech?: string;
  definition?: string;
  example_sentence?: string;
  notes?: string;
  difficulty_level?: DifficultyLevel;
  category_id?: string | null;
  tags?: string[];
  confidence_score?: number;
  is_mastered?: boolean;
}

export interface BulkWordCreateData {
  words: WordCreateData[];
}

export interface WordStats {
  total: number;
  mastered: number;
  learning: number;
  new: number;
  by_difficulty: {
    easy: number;
    medium: number;
    hard: number;
  };
  by_category: {
    name: string;
    color: string;
    icon: string;
    count: number;
  }[];
  average_confidence: number;
}

export interface WordFilters {
  difficulty_level?: DifficultyLevel;
  category_id?: string;
  is_mastered?: boolean;
  part_of_speech?: string;
  search?: string;
  ordering?: string;
  page?: number;
  page_size?: number;
}
