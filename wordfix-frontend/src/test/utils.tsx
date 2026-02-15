import React, { type ReactElement } from 'react';
import { render, type RenderOptions, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '@/providers/ThemeProvider';
import type { Word, ReviewSession, ReviewSummary, WordStats, User, TestQuestion, TestSession, GameSession } from '@/types';

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

export {
  customRender as render, screen, userEvent, waitFor, within,
  renderWithRoute, createMockUser, createMockWord, createMockReviewSession,
  createMockWordStats, createMockReviewSummary, createMockTestQuestion,
  createMockTestSession, createMockGameSession,
};
