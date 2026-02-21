import React, { type ReactElement } from 'react';
import { render, type RenderOptions, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '@/providers/ThemeProvider';
import type { Word, ReviewSession, ReviewSummary, WordStats, User, TestQuestion, TestSession, GameSession, ChatSession, ChatMessage, AnalyticsOverview, CSVImportResult, BadgeData, NotificationData, LearningProfile, UserProgressData, DailyProgress } from '@/types';
import type { ConfusingPair } from '@/features/confusing-pairs/types';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 }, mutations: { retry: false } },
  });
}

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="light" storageKey="test-theme">
        <BrowserRouter>{children}</BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

function customRender(ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, { wrapper: AllProviders, ...options });
}

function renderWithRoute(ui: ReactElement, _route = '/') {
  window.history.pushState({}, '', _route);
  return customRender(ui);
}

// ─── Factory Functions ─────────────────────────────────────────────────────────

function createMockUser(overrides?: Partial<User>): User {
  return {
    id: 'user-1', email: 'test@example.com', username: 'testuser', full_name: 'Test User',
    avatar: '', native_language: 'en', learning_language: 'es', proficiency_level: 'B1',
    daily_goal: 10, timezone: 'UTC', is_premium: false, premium_until: null, is_premium_active: false,
    is_active: true, date_joined: '2025-01-01', last_login: null, has_completed_onboarding: true,
    ...overrides,
  };
}

function createMockWord(overrides?: Partial<Word>): Word {
  return {
    id: 'word-1', user_id: 'user-1', original_word: 'hello', translation: 'hola',
    pronunciation: '/həˈloʊ/', part_of_speech: 'interjection', definition: 'A greeting',
    example_sentence: 'Hello, how are you?', example_translation: 'Hola, ¿cómo estás?',
    synonyms: ['hi', 'hey'], antonyms: ['goodbye'], collocations: [], word_family: [],
    image_url: '', audio_url: '', notes: '', category_id: null, category: null, tags: [],
    difficulty_level: 'easy', is_enriched: true, confidence_score: 0.8,
    next_review_at: null, review_count: 5, correct_count: 4, incorrect_count: 1,
    last_reviewed_at: null, is_mastered: false, is_active: true,
    created_at: '2025-01-01', updated_at: '2025-01-01', accuracy_rate: 80,
    mnemonic: 'Think of waving hello', usage_notes: '', enrichment_status: 'enriched',
    enrichment_error: '', enriched_at: '2025-01-01', easiness_factor: 2.5,
    repetition_number: 3, interval_days: 7, ...overrides,
  };
}

function createMockReviewSession(overrides?: Partial<ReviewSession>): ReviewSession {
  return {
    id: 'session-1', user_id: 'user-1', session_type: 'review', total_words: 10,
    correct_count: 7, incorrect_count: 3, average_quality: 3.5,
    started_at: '2025-01-01T10:00:00Z', completed_at: null, is_completed: false,
    created_at: '2025-01-01', updated_at: '2025-01-01',
    current_combo: 0, max_combo: 5, combo_xp_bonus: 20, ...overrides,
  };
}

function createMockWordStats(overrides?: Partial<WordStats>): WordStats {
  return {
    total: 50, mastered: 15, learning: 25, new: 10,
    by_difficulty: { easy: 20, medium: 20, hard: 10 },
    by_category: [], average_confidence: 0.65, ...overrides,
  };
}

function createMockReviewSummary(overrides?: Partial<ReviewSummary>): ReviewSummary {
  return {
    total_reviews: 100, total_sessions: 20, words_due: 12,
    average_accuracy: 78, reviews_today: 5, streak_days: 7, ...overrides,
  };
}

function createMockTestQuestion(overrides?: Partial<TestQuestion>): TestQuestion {
  return {
    id: 'q-1', question_type: 'multiple_choice', question_text: 'What does "hello" mean?',
    options: ['hola', 'mundo', 'casa', 'perro'], order: 1, user_answer: '',
    is_correct: null, correct_answer: null, explanation: null, ...overrides,
  };
}

function createMockTestSession(overrides?: Partial<TestSession>): TestSession {
  return {
    id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5,
    correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true,
    started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z',
    duration_seconds: 600, created_at: '2025-01-01',
    current_combo: 0, max_combo: 3, combo_xp_bonus: 20, ...overrides,
  };
}

function createMockGameSession(overrides?: Partial<GameSession>): GameSession {
  return {
    id: 'gs-1', game_type: 'speed_round', score: 80, max_score: 100,
    correct_answers: 4, incorrect_answers: 1, total_questions: 5,
    duration_seconds: 45, level: 1, xp_earned: 50, is_completed: true,
    started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:01:00Z',
    created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 10,
    ...overrides,
  };
}

function createMockChatSession(overrides?: Partial<ChatSession>): ChatSession {
  return {
    id: 'chat-1', topic: 'Travel', started_at: '2025-01-01T10:00:00Z',
    ended_at: null, message_count: 5, target_words: ['hello', 'world'],
    words_practiced: ['hello'], is_active: true,
    created_at: '2025-01-01', updated_at: '2025-01-01', ...overrides,
  };
}

function createMockMessage(overrides?: Partial<ChatMessage>): ChatMessage {
  return {
    id: 'msg-1', session_id: 'chat-1', role: 'user', content: 'Hello!',
    corrections: [], words_used: ['hello'], order: 0,
    created_at: '2025-01-01T10:00:00Z', ...overrides,
  };
}

function createMockAnalytics(overrides?: Partial<AnalyticsOverview>): AnalyticsOverview {
  return {
    total_words: 50, mastered_words: 15, mastered_percentage: 30,
    total_reviews: 200, total_correct: 160, overall_accuracy: 80,
    total_study_time_formatted: '12h 30m', total_xp: 1500,
    current_level: 5, current_streak: 7, longest_streak: 14,
    tests_completed: 12, games_played: 8, avg_daily_words: 5,
    avg_daily_time: 25, member_since_days: 45, ...overrides,
  };
}

function createMockConfusingPair(overrides?: Partial<ConfusingPair>): ConfusingPair {
  return {
    id: 'cp-1', word_1: { id: 'w1', original_word: 'affect', translation: 'влиять' },
    word_2: { id: 'w2', original_word: 'effect', translation: 'эффект' },
    confusion_count: 7, last_confused_at: '2025-01-15', is_resolved: false,
    ...overrides,
  };
}

function createMockImportResult(overrides?: Partial<CSVImportResult>): CSVImportResult {
  return {
    total_in_file: 10, imported: 8, skipped_duplicate: 1,
    skipped_invalid: 1, errors: [], categories_created: [],
    xp_earned: 40, ...overrides,
  };
}

function createMockBadge(overrides?: Partial<BadgeData>): BadgeData {
  return {
    id: 'b1', code: 'first_word', name: 'First Word', description: 'Add your first word',
    icon: '📝', category: 'words', xp_reward: 10, rarity: 'common',
    is_earned: false, earned_at: null, ...overrides,
  };
}

function createMockNotification(overrides?: Partial<NotificationData>): NotificationData {
  return {
    id: 'n1', type: 'badge_earned', title: 'Badge Earned!',
    message: 'You earned the First Word badge', is_read: false,
    data: {}, created_at: '2025-01-15T10:00:00Z', ...overrides,
  };
}

function createMockLearningProfile(overrides?: Partial<LearningProfile>): LearningProfile {
  return {
    preferred_style: 'visual',
    style_confidence: 0.75,
    best_time: { start_hour: 9, end_hour: 11, best_days: [0, 2, 4] },
    session_stats: { avg_duration: 20, optimal_words: 8, retention_rate: 0.78 },
    skills: { strongest: ['vocabulary'], weakest: ['listening'], scores: { reading: 80, vocabulary: 90, listening: 40, context: 60, speed: 70 } },
    difficulty_level: 3, last_analyzed: '2025-01-15', ...overrides,
  } as LearningProfile;
}

function createMockUserProgress(overrides?: Partial<UserProgressData>): UserProgressData {
  return {
    level: 5, total_xp: 1500, xp_for_current: 1200, xp_for_next: 2000,
    progress_pct: 37, xp_progress: 300, xp_needed: 800,
    words_learned_total: 50, words_mastered_total: 15, tests_completed: 12,
    games_played: 8, reviews_completed: 100, perfect_scores: 3,
    total_study_time_seconds: 45000, ...overrides,
  };
}

function createMockDailyProgress(overrides?: Partial<DailyProgress>): DailyProgress {
  return {
    id: 'dp-1', words_reviewed: 7, words_added: 2, words_mastered: 1,
    correct_answers: 6, incorrect_answers: 1, total_time_seconds: 1200,
    goal_completed: false, xp_earned: 35, date: '2025-01-15', ...overrides,
  };
}

export {
  customRender as render, screen, userEvent, waitFor, within,
  renderWithRoute, createMockUser, createMockWord, createMockReviewSession,
  createMockWordStats, createMockReviewSummary, createMockTestQuestion,
  createMockTestSession, createMockGameSession, createMockChatSession,
  createMockMessage, createMockAnalytics, createMockConfusingPair, createMockImportResult,
  createMockBadge, createMockNotification, createMockLearningProfile,
  createMockUserProgress, createMockDailyProgress,
};
