// ─── Core Types ────────────────────────────────────────────────────────────────

export type Theme = 'light' | 'dark' | 'system';

export type DifficultyLevel = 'easy' | 'medium' | 'hard';

export type ProficiencyLevel = 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';

// ─── User Types ────────────────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  avatar: string;
  native_language: string;
  learning_language: string;
  proficiency_level: ProficiencyLevel;
  daily_goal: number;
  timezone: string;
  is_premium: boolean;
  premium_until: string | null;
  is_premium_active: boolean;
  is_active: boolean;
  date_joined: string;
  last_login: string | null;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  full_name?: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface UpdateProfileData {
  full_name?: string;
  native_language?: string;
  learning_language?: string;
  proficiency_level?: ProficiencyLevel;
  daily_goal?: number;
  timezone?: string;
}

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

// ─── API Types ─────────────────────────────────────────────────────────────────

export interface ApiResponse<T = unknown> {
  success: boolean;
  data: T;
  message: string;
  errors: Record<string, string[]> | null;
  meta: PaginationMeta | null;
}

export interface PaginationMeta {
  page: number;
  total_pages: number;
  total_count: number;
  page_size: number;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'degraded';
  version: string;
  services: { db: 'up' | 'down'; redis: 'up' | 'down'; celery: 'up' | 'down' };
}

// ─── Review & Spaced Repetition Types ──────────────────────────────────────────

export type ReviewQuality = 0 | 1 | 2 | 3 | 4 | 5;

export type SessionType = 'review' | 'learn' | 'mixed';

export type EnrichmentStatus = 'pending' | 'processing' | 'enriched' | 'failed';

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

// ─── Test Types ────────────────────────────────────────────────────────────────

export type TestType = 'multiple_choice' | 'fill_blank' | 'context_guess' | 'mixed';
export type TestDifficulty = 'easy' | 'medium' | 'hard' | 'adaptive';

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
}

export interface TestDetailResponse {
  session: TestSession;
  questions: TestQuestion[];
}

// ─── Game Types ────────────────────────────────────────────────────────────────

export type GameType = 'speed_round' | 'word_match' | 'word_context';

export interface GameSession {
  id: string;
  game_type: GameType;
  score: number;
  max_score: number;
  correct_answers: number;
  total_questions: number;
  duration_seconds: number;
  level: number;
  xp_earned: number;
  is_completed: boolean;
  created_at: string;
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

// ─── Badge Types ───────────────────────────────────────────────────────────────

export type BadgeRarity = 'common' | 'rare' | 'epic' | 'legendary';
export type BadgeCategory = 'words' | 'streak' | 'review' | 'test' | 'game' | 'mastery' | 'level';

export interface BadgeData {
  id: string;
  code: string;
  name: string;
  description: string;
  icon: string;
  category: BadgeCategory;
  xp_reward: number;
  rarity: BadgeRarity;
  is_earned: boolean;
  earned_at: string | null;
}

export interface UserBadgesResponse {
  badges: BadgeData[];
  earned_count: number;
  total_count: number;
}

export interface NewBadgeInfo {
  code: string;
  name: string;
  icon: string;
}

// ─── Notification Types ────────────────────────────────────────────────────────

export type NotificationType =
  | 'review_reminder'
  | 'streak_warning'
  | 'badge_earned'
  | 'level_up'
  | 'daily_goal_complete'
  | 'word_mastered'
  | 'weekly_report';

export interface NotificationData {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  is_read: boolean;
  data: Record<string, unknown>;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: NotificationData[];
  unread_count: number;
}
