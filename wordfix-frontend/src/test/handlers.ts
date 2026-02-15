import { http, HttpResponse } from 'msw';

const API = 'http://localhost:8000/api/v1';

const mockWords = [
  { id: 'w1', user_id: 'u1', original_word: 'hello', translation: 'hola', pronunciation: '/həˈloʊ/', part_of_speech: 'interjection', definition: 'A greeting', example_sentence: 'Hello!', example_translation: '¡Hola!', synonyms: ['hi'], antonyms: ['goodbye'], collocations: [], word_family: [], image_url: '', audio_url: '', notes: '', category_id: null, category: null, tags: [], difficulty_level: 'easy', is_enriched: true, confidence_score: 0.8, next_review_at: null, review_count: 5, correct_count: 4, incorrect_count: 1, last_reviewed_at: null, is_mastered: false, is_active: true, created_at: '2025-01-01', updated_at: '2025-01-01', accuracy_rate: 80, mnemonic: '', usage_notes: '', enrichment_status: 'enriched', enrichment_error: '', enriched_at: null, easiness_factor: 2.5, repetition_number: 3, interval_days: 7 },
  { id: 'w2', user_id: 'u1', original_word: 'world', translation: 'mundo', pronunciation: '/wɜːrld/', part_of_speech: 'noun', definition: 'The earth', example_sentence: 'The world is big.', example_translation: 'El mundo es grande.', synonyms: ['globe'], antonyms: [], collocations: [], word_family: [], image_url: '', audio_url: '', notes: '', category_id: null, category: null, tags: [], difficulty_level: 'medium', is_enriched: true, confidence_score: 0.6, next_review_at: '2025-02-01', review_count: 3, correct_count: 2, incorrect_count: 1, last_reviewed_at: null, is_mastered: false, is_active: true, created_at: '2025-01-01', updated_at: '2025-01-01', accuracy_rate: 67, mnemonic: '', usage_notes: '', enrichment_status: 'enriched', enrichment_error: '', enriched_at: null, easiness_factor: 2.2, repetition_number: 2, interval_days: 3 },
  { id: 'w3', user_id: 'u1', original_word: 'difficult', translation: 'difícil', pronunciation: '', part_of_speech: 'adjective', definition: 'Not easy', example_sentence: '', example_translation: '', synonyms: [], antonyms: ['easy'], collocations: [], word_family: [], image_url: '', audio_url: '', notes: '', category_id: null, category: null, tags: [], difficulty_level: 'hard', is_enriched: false, confidence_score: 0.3, next_review_at: '2025-01-20', review_count: 1, correct_count: 0, incorrect_count: 1, last_reviewed_at: null, is_mastered: false, is_active: true, created_at: '2025-01-01', updated_at: '2025-01-01', accuracy_rate: 0, mnemonic: '', usage_notes: '', enrichment_status: 'pending', enrichment_error: '', enriched_at: null, easiness_factor: 2.5, repetition_number: 0, interval_days: 1 },
];

const mockStats = { total: 50, mastered: 15, learning: 25, new: 10, by_difficulty: { easy: 20, medium: 20, hard: 10 }, by_category: [], average_confidence: 0.65 };

const mockSummary = { total_reviews: 100, total_sessions: 20, words_due: 12, average_accuracy: 78, reviews_today: 5, streak_days: 7 };

const mockSession = { id: 'ses-1', user_id: 'u1', session_type: 'review', total_words: 3, correct_count: 0, incorrect_count: 0, average_quality: 0, started_at: '2025-01-01T10:00:00Z', completed_at: null, is_completed: false, created_at: '2025-01-01', updated_at: '2025-01-01', current_combo: 0, max_combo: 0, combo_xp_bonus: 0 };

export const handlers = [
  // Words
  http.get(`${API}/words/`, ({ request }) => {
    const url = new URL(request.url);
    const search = url.searchParams.get('search') || '';
    const difficulty = url.searchParams.get('difficulty_level') || '';
    let filtered = [...mockWords];
    if (search) filtered = filtered.filter((w) => w.original_word.includes(search.toLowerCase()));
    if (difficulty) filtered = filtered.filter((w) => w.difficulty_level === difficulty);
    return HttpResponse.json({ success: true, data: filtered, message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: filtered.length, page_size: 20 } });
  }),

  http.post(`${API}/words/`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const newWord = { ...mockWords[0], id: 'w-new', original_word: body.original_word as string, translation: (body.translation as string) || '', difficulty_level: (body.difficulty_level as string) || 'medium' };
    return HttpResponse.json({ success: true, data: newWord, message: 'Created', errors: null, meta: null });
  }),

  http.delete(`${API}/words/:id/`, () => {
    return new HttpResponse(null, { status: 204 });
  }),

  http.get(`${API}/words/stats/`, () => {
    return HttpResponse.json({ success: true, data: mockStats, message: 'OK', errors: null, meta: null });
  }),

  // Review
  http.get(`${API}/review/summary/`, () => {
    return HttpResponse.json({ success: true, data: mockSummary, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/review/words/`, () => {
    return HttpResponse.json({ success: true, data: mockWords, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/review/sessions/`, () => {
    return HttpResponse.json({ success: true, data: mockSession, message: 'Created', errors: null, meta: null });
  }),

  http.get(`${API}/review/sessions/:id/`, () => {
    return HttpResponse.json({ success: true, data: mockSession, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/review/sessions/:id/answer/`, () => {
    return HttpResponse.json({ success: true, data: { word: mockWords[0], session: mockSession, is_correct: true, combo: 2, multiplier: 1.5, xp_earned: 15 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/review/sessions/:id/complete/`, () => {
    return HttpResponse.json({ success: true, data: { ...mockSession, is_completed: true, completed_at: '2025-01-01T10:10:00Z', correct_count: 7, incorrect_count: 3, average_quality: 3.5, max_combo: 5, combo_xp_bonus: 20 }, message: 'Completed', errors: null, meta: null });
  }),

  http.get(`${API}/review/history/`, () => {
    return HttpResponse.json({ success: true, data: [{ ...mockSession, is_completed: true, completed_at: '2025-01-01T10:10:00Z', correct_count: 7, incorrect_count: 3 }], message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: 1, page_size: 10 } });
  }),

  http.get(`${API}/review/streak/`, () => {
    return HttpResponse.json({ success: true, data: { id: 's1', current_streak: 7, longest_streak: 14, last_activity_date: '2025-01-15', streak_frozen_until: null, total_review_days: 30 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/words/categories/`, () => {
    return HttpResponse.json({ success: true, data: [], message: 'OK', errors: null, meta: null });
  }),

  // ─── Tests ─────────────────────────────────────────────────────────────────
  http.post(`${API}/tests/generate/`, () => {
    const session = { id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 0, incorrect_answers: 0, score_percentage: 0, is_completed: false, started_at: '2025-01-01T10:00:00Z', completed_at: null, duration_seconds: 0, created_at: '2025-01-01', current_combo: 0, max_combo: 0, combo_xp_bonus: 0 };
    const questions = [{ id: 'q1', question_type: 'multiple_choice', question_text: 'What does "hello" mean?', options: ['hola', 'mundo', 'casa', 'perro'], order: 1, user_answer: '', is_correct: null, correct_answer: null, explanation: null }];
    return HttpResponse.json({ success: true, data: { session, questions }, message: 'Created', errors: null, meta: null });
  }),

  http.post(`${API}/tests/:id/answer/`, () => {
    return HttpResponse.json({ success: true, data: { is_correct: true, correct_answer: 'hola', explanation: 'Hello means hola in Spanish.', combo: 1, multiplier: 1.5, xp_earned: 15 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/tests/:id/complete/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z', duration_seconds: 600, created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 20 }, message: 'Completed', errors: null, meta: null });
  }),

  http.get(`${API}/tests/:id/`, () => {
    const session = { id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z', duration_seconds: 600, created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 20 };
    const questions = [{ id: 'q1', question_type: 'multiple_choice', question_text: 'What does "hello" mean?', options: ['hola', 'mundo', 'casa', 'perro'], order: 1, user_answer: 'hola', is_correct: true, correct_answer: 'hola', explanation: 'Hello means hola.' }];
    return HttpResponse.json({ success: true, data: { session, questions }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/tests/history/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z', duration_seconds: 600, created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 20 }], message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: 1, page_size: 10 } });
  }),

  // ─── Games ─────────────────────────────────────────────────────────────────
  http.post(`${API}/games/speed-round/start/`, () => {
    return HttpResponse.json({ success: true, data: { session_id: 'gs-1', words: [{ word_id: 'w1', word: 'hello', options: ['hola', 'mundo', 'casa', 'perro'], correct_translation: 'hola' }], time_limit: 60 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/speed-round/submit/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'gs-1', game_type: 'speed_round', score: 80, max_score: 100, correct_answers: 4, incorrect_answers: 1, total_questions: 5, duration_seconds: 45, level: 1, xp_earned: 50, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:01:00Z', created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 10 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/word-match/start/`, () => {
    return HttpResponse.json({ success: true, data: { session_id: 'gs-2', words: [{ word_id: 'w1', word: 'hello' }, { word_id: 'w2', word: 'world' }], translations: ['hola', 'mundo'], pair_count: 2 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/word-match/submit/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'gs-2', game_type: 'word_match', score: 100, max_score: 100, correct_answers: 2, incorrect_answers: 0, total_questions: 2, duration_seconds: 30, level: 1, xp_earned: 40, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:00:30Z', created_at: '2025-01-01', current_combo: 0, max_combo: 2, combo_xp_bonus: 5 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/word-context/start/`, () => {
    return HttpResponse.json({ success: true, data: { session_id: 'gs-3', questions: [{ word_id: 'w1', context: 'She said ___ to her friend.', correct_answer: 'hello', options: ['hello', 'world', 'house', 'dog'], hint: 'A greeting', explanation: 'Hello is a common greeting.' }] }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/word-context/submit/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'gs-3', game_type: 'word_context', score: 80, max_score: 100, correct_answers: 4, incorrect_answers: 1, total_questions: 5, duration_seconds: 120, level: 1, xp_earned: 45, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:02:00Z', created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 8 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/story-builder/start/`, () => {
    return HttpResponse.json({ success: true, data: { session_id: 'gs-4', genre: 'adventure', ai_text: 'The brave explorer ventured into the mysterious forest.', target_words: ['brave', 'forest'], total_rounds: 3, current_round: 1, all_target_words: ['brave', 'forest', 'river', 'mountain', 'treasure', 'ancient'] }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/story-builder/submit/`, () => {
    return HttpResponse.json({ success: true, data: { round_result: { score: 8, words_used: ['brave'], grammar_corrections: [], feedback: 'Great use of vocabulary!', is_correct_usage: true }, next_round: { ai_text: 'They crossed the river.', target_words: ['river', 'mountain'], round_number: 2 }, session_stats: { total_score: 8, rounds_completed: 1 }, combo: 1, multiplier: 1.5, xp_earned: 12 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/story-builder/complete/`, () => {
    return HttpResponse.json({ success: true, data: { total_score: 24, max_score: 30, rounds: [], full_story: 'The brave explorer ventured...', xp_earned: 50 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/listening/start/`, () => {
    return HttpResponse.json({ success: true, data: { session_id: 'gs-5', total_rounds: 5, current_round: 1, first_word: { round_number: 1, audio_url: '/audio/hello.mp3', hint: 'A greeting', difficulty: 'easy', max_attempts: 3 } }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/listening/answer/`, () => {
    return HttpResponse.json({ success: true, data: { is_correct: true, score: 10, attempts_used: 1, attempts_remaining: 2, hint: 'A greeting', correct_answer: 'hello', next_round: { round_number: 2, audio_url: '/audio/world.mp3', hint: 'Earth', max_attempts: 3 }, combo: 1, multiplier: 1.5, xp_earned: 15 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/games/listening/complete/`, () => {
    return HttpResponse.json({ success: true, data: { total_score: 40, max_score: 50, rounds: [{ word: 'hello', is_correct: true, attempts_used: 1, score: 10 }], accuracy_pct: 80, xp_earned: 40 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/games/history/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'gs-1', game_type: 'speed_round', score: 80, max_score: 100, correct_answers: 4, incorrect_answers: 1, total_questions: 5, duration_seconds: 45, level: 1, xp_earned: 50, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:01:00Z', created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 10 }], message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: 1, page_size: 10 } });
  }),

  http.get(`${API}/games/stats/`, () => {
    return HttpResponse.json({ success: true, data: { total_games: 10, total_xp: 500, favorite_game: 'speed_round', by_type: { speed_round: { games_played: 5, best_score: 95, total_xp: 250 } } }, message: 'OK', errors: null, meta: null });
  }),
];
