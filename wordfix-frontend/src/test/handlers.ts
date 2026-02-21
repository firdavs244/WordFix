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

  http.get(`${API}/tests/history/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z', duration_seconds: 600, created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 20 }], message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: 1, page_size: 10 } });
  }),

  http.get(`${API}/tests/:id/`, () => {
    const session = { id: 'ts-1', test_type: 'multiple_choice', difficulty: 'medium', total_questions: 5, correct_answers: 4, incorrect_answers: 1, score_percentage: 80, is_completed: true, started_at: '2025-01-01T10:00:00Z', completed_at: '2025-01-01T10:10:00Z', duration_seconds: 600, created_at: '2025-01-01', current_combo: 0, max_combo: 3, combo_xp_bonus: 20 };
    const questions = [{ id: 'q1', question_type: 'multiple_choice', question_text: 'What does "hello" mean?', options: ['hola', 'mundo', 'casa', 'perro'], order: 1, user_answer: 'hola', is_correct: true, correct_answer: 'hola', explanation: 'Hello means hola.' }];
    return HttpResponse.json({ success: true, data: { session, questions }, message: 'OK', errors: null, meta: null });
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

  // ─── Chat ──────────────────────────────────────────────────────────────────
  http.post(`${API}/chat/start/`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    return HttpResponse.json({ success: true, data: { session_id: 'chat-1', topic: (body.topic as string) || 'Free Conversation', target_words: ['hello', 'world', 'difficult'], first_message: { role: 'assistant', content: 'Hi! Let\'s practice English together.', corrections: [], words_used: [] } }, message: 'Created', errors: null, meta: null });
  }),

  http.get(`${API}/chat/history/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'chat-1', topic: 'Travel', started_at: '2025-01-01T10:00:00Z', ended_at: null, message_count: 5, target_words: ['hello'], words_practiced: ['hello'], is_active: true, created_at: '2025-01-01', updated_at: '2025-01-01' }, { id: 'chat-2', topic: 'Food', started_at: '2025-01-02T10:00:00Z', ended_at: '2025-01-02T11:00:00Z', message_count: 10, target_words: ['world'], words_practiced: ['world'], is_active: false, created_at: '2025-01-02', updated_at: '2025-01-02' }], message: 'OK', errors: null, meta: { page: 1, total_pages: 1, total_count: 2, page_size: 10 } });
  }),

  http.get(`${API}/chat/sessions/:id/`, () => {
    return HttpResponse.json({ success: true, data: { session: { id: 'chat-1', topic: 'Travel', started_at: '2025-01-01T10:00:00Z', ended_at: null, message_count: 2, target_words: ['hello', 'world'], words_practiced: ['hello'], is_active: true, created_at: '2025-01-01', updated_at: '2025-01-01' }, messages: [{ id: 'm1', session_id: 'chat-1', role: 'assistant', content: 'Hi! Let\'s talk about travel.', corrections: [], words_used: [], order: 0, created_at: '2025-01-01T10:00:00Z' }, { id: 'm2', session_id: 'chat-1', role: 'user', content: 'Hello! I love traveling.', corrections: [], words_used: ['hello'], order: 1, created_at: '2025-01-01T10:01:00Z' }] }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/chat/sessions/:id/message/`, async () => {
    return HttpResponse.json({ success: true, data: { ai_message: 'That sounds great! Where do you like to travel?', corrections: [{ original: 'I goed', corrected: 'I went', explanation: 'Past tense of go is went' }], words_used: ['travel'], encouragement: 'Great job!', xp_earned: 10 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/chat/sessions/:id/end/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'chat-1', topic: 'Travel', started_at: '2025-01-01T10:00:00Z', ended_at: '2025-01-01T11:00:00Z', message_count: 5, target_words: ['hello', 'world'], words_practiced: ['hello', 'world'], is_active: false, created_at: '2025-01-01', updated_at: '2025-01-01' }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Import ────────────────────────────────────────────────────────────────
  http.post(`${API}/words/import/analyze/`, () => {
    return HttpResponse.json({ success: true, data: { suggestions: [{ word: 'adventure', translation: 'приключение', part_of_speech: 'noun', context_sentence: 'The adventure was amazing.', difficulty: 'medium', reason: 'Common B1 word' }, { word: 'journey', translation: 'путешествие', part_of_speech: 'noun', context_sentence: 'A long journey ahead.', difficulty: 'easy', reason: 'Useful travel word' }, { word: 'destination', translation: 'пункт назначения', part_of_speech: 'noun', context_sentence: 'The final destination.', difficulty: 'hard', reason: 'Important vocabulary' }], total_found: 3, already_known: 0, text_length: 200 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/words/import/add/`, () => {
    return HttpResponse.json({ success: true, data: { created: 2, skipped: 1, errors: [] }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/words/import/csv/validate/`, () => {
    return HttpResponse.json({ success: true, data: { headers: ['word', 'translation', 'difficulty'], preview: [{ word: 'apple', translation: 'яблоко', difficulty: 'easy' }, { word: 'banana', translation: 'банан', difficulty: 'easy' }], total_rows: 10, valid_rows: 9, errors: ['Row 5: missing translation'], has_translation: true, has_difficulty: true, has_category: false }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/words/import/csv/`, () => {
    return HttpResponse.json({ success: true, data: { total_in_file: 10, imported: 8, skipped_duplicate: 1, skipped_invalid: 1, errors: [], categories_created: [], xp_earned: 40 }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Analytics ─────────────────────────────────────────────────────────────
  http.get(`${API}/analytics/overview/`, () => {
    return HttpResponse.json({ success: true, data: { total_words: 50, mastered_words: 15, mastered_percentage: 30, total_reviews: 200, total_correct: 160, overall_accuracy: 80, total_study_time_formatted: '12h 30m', total_xp: 1500, current_level: 5, current_streak: 7, longest_streak: 14, tests_completed: 12, games_played: 8, avg_daily_words: 5, avg_daily_time: 25, member_since_days: 45 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/analytics/weekly/`, () => {
    return HttpResponse.json({ success: true, data: [{ date: '2025-01-13', words_reviewed: 8, words_added: 2, correct_answers: 6, incorrect_answers: 2, xp_earned: 40, total_time_seconds: 1200 }, { date: '2025-01-14', words_reviewed: 12, words_added: 3, correct_answers: 10, incorrect_answers: 2, xp_earned: 60, total_time_seconds: 1800 }, { date: '2025-01-15', words_reviewed: 5, words_added: 1, correct_answers: 4, incorrect_answers: 1, xp_earned: 25, total_time_seconds: 900 }, { date: '2025-01-16', words_reviewed: 15, words_added: 4, correct_answers: 13, incorrect_answers: 2, xp_earned: 75, total_time_seconds: 2100 }, { date: '2025-01-17', words_reviewed: 10, words_added: 2, correct_answers: 8, incorrect_answers: 2, xp_earned: 50, total_time_seconds: 1500 }, { date: '2025-01-18', words_reviewed: 3, words_added: 0, correct_answers: 3, incorrect_answers: 0, xp_earned: 15, total_time_seconds: 600 }, { date: '2025-01-19', words_reviewed: 7, words_added: 1, correct_answers: 6, incorrect_answers: 1, xp_earned: 35, total_time_seconds: 1100 }], message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/analytics/calendar/`, () => {
    const days = [];
    for (let i = 0; i < 84; i++) {
      const d = new Date(2025, 0, 1);
      d.setDate(d.getDate() - i);
      days.push({ date: d.toISOString().slice(0, 10), active: Math.random() > 0.3, words_reviewed: Math.floor(Math.random() * 15), xp_earned: Math.floor(Math.random() * 50), goal_completed: Math.random() > 0.5 });
    }
    return HttpResponse.json({ success: true, data: days, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/analytics/difficult-words/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'w3', original_word: 'difficult', translation: 'difícil', accuracy_rate: 25, review_count: 8, incorrect_count: 6, confidence_score: 0.2 }, { id: 'w4', original_word: 'elaborate', translation: 'elaborar', accuracy_rate: 33, review_count: 6, incorrect_count: 4, confidence_score: 0.3 }, { id: 'w5', original_word: 'ambiguous', translation: 'ambiguo', accuracy_rate: 40, review_count: 5, incorrect_count: 3, confidence_score: 0.35 }], message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/analytics/word-progress/`, () => {
    return HttpResponse.json({ success: true, data: { by_confidence: { mastered: 15, confident: 10, learning: 20, new: 5 }, by_difficulty: { easy: 20, medium: 20, hard: 10 }, by_category: [], recently_mastered: [], needs_attention: [] }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Confusing Pairs ──────────────────────────────────────────────────────
  http.get(`${API}/words/confusing-pairs/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'cp-1', word_1: { id: 'w1', original_word: 'affect', translation: 'влиять' }, word_2: { id: 'w2', original_word: 'effect', translation: 'эффект' }, confusion_count: 7, last_confused_at: '2025-01-15', is_resolved: false }, { id: 'cp-2', word_1: { id: 'w3', original_word: 'accept', translation: 'принять' }, word_2: { id: 'w4', original_word: 'except', translation: 'кроме' }, confusion_count: 3, last_confused_at: '2025-01-10', is_resolved: false }, { id: 'cp-3', word_1: { id: 'w5', original_word: 'their', translation: 'их' }, word_2: { id: 'w6', original_word: 'there', translation: 'там' }, confusion_count: 10, last_confused_at: '2025-01-05', is_resolved: true }], message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/words/confusing-pairs/:id/drill/`, () => {
    return HttpResponse.json({ success: true, data: { explanation: 'Affect is a verb meaning to influence. Effect is a noun meaning a result.', word_1_examples: [{ sentence: 'The weather affects my mood.', translation: 'Погода влияет на моё настроение.' }], word_2_examples: [{ sentence: 'The effect was immediate.', translation: 'Эффект был мгновенным.' }], mnemonic: 'Affect = Action (verb), Effect = End result (noun)', test_questions: [{ sentence: 'The rain will ___ the game.', correct_answer: 'affect', wrong_answer: 'effect', explanation: 'Affect is used as a verb here.' }, { sentence: 'The ___ of the medicine was quick.', correct_answer: 'effect', wrong_answer: 'affect', explanation: 'Effect is used as a noun here.' }, { sentence: 'How does pollution ___ the environment?', correct_answer: 'affect', wrong_answer: 'effect', explanation: 'Affect is a verb meaning to influence.' }] }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/words/confusing-pairs/:id/resolve/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'cp-1', word_1: { id: 'w1', original_word: 'affect', translation: 'влиять' }, word_2: { id: 'w2', original_word: 'effect', translation: 'эффект' }, confusion_count: 7, last_confused_at: '2025-01-15', is_resolved: true }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/words/confusing-pairs/count/`, () => {
    return HttpResponse.json({ success: true, data: { count: 2 }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Progress / Badges ─────────────────────────────────────────────────────
  http.get(`${API}/users/progress/`, () => {
    return HttpResponse.json({ success: true, data: { level: 5, total_xp: 1500, xp_for_current: 1200, xp_for_next: 2000, progress_pct: 37, xp_progress: 300, xp_needed: 800, words_learned_total: 50, words_mastered_total: 15, tests_completed: 12, games_played: 8, reviews_completed: 100, perfect_scores: 3, total_study_time_seconds: 45000 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/users/xp-history/`, () => {
    return HttpResponse.json({ success: true, data: [{ date: '2025-01-13', xp: 40 }, { date: '2025-01-14', xp: 60 }, { date: '2025-01-15', xp: 25 }], message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/users/badges/`, () => {
    return HttpResponse.json({ success: true, data: { badges: [{ id: 'b1', code: 'first_word', name: 'First Word', description: 'Add your first word', icon: '📝', category: 'words', xp_reward: 10, rarity: 'common', is_earned: true, earned_at: '2025-01-01' }, { id: 'b2', code: 'streak_7', name: 'Week Warrior', description: '7 day streak', icon: '🔥', category: 'streak', xp_reward: 50, rarity: 'rare', is_earned: true, earned_at: '2025-01-10' }], earned_count: 2, total_count: 5 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/badges/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'b1', code: 'first_word', name: 'First Word', description: 'Add your first word', icon: '📝', category: 'words', xp_reward: 10, rarity: 'common', is_earned: false, earned_at: null }, { id: 'b2', code: 'streak_7', name: 'Week Warrior', description: '7 day streak', icon: '🔥', category: 'streak', xp_reward: 50, rarity: 'rare', is_earned: false, earned_at: null }, { id: 'b3', code: 'master_10', name: 'Word Master', description: 'Master 10 words', icon: '⭐', category: 'mastery', xp_reward: 100, rarity: 'epic', is_earned: false, earned_at: null }, { id: 'b4', code: 'legend', name: 'Legend', description: 'Reach level 50', icon: '👑', category: 'level', xp_reward: 500, rarity: 'legendary', is_earned: false, earned_at: null }, { id: 'b5', code: 'test_ace', name: 'Test Ace', description: 'Score 100% on a test', icon: '🎯', category: 'test', xp_reward: 75, rarity: 'rare', is_earned: false, earned_at: null }], message: 'OK', errors: null, meta: null });
  }),

  // ─── Notifications ─────────────────────────────────────────────────────────
  http.get(`${API}/notifications/`, () => {
    return HttpResponse.json({ success: true, data: { notifications: [{ id: 'n1', type: 'badge_earned', title: 'Badge Earned!', message: 'You earned the First Word badge', is_read: false, data: {}, created_at: '2025-01-15T10:00:00Z' }, { id: 'n2', type: 'streak_warning', title: 'Streak Warning', message: 'Practice today to keep your streak', is_read: false, data: {}, created_at: '2025-01-14T08:00:00Z' }, { id: 'n3', type: 'level_up', title: 'Level Up!', message: 'You reached level 5', is_read: true, data: {}, created_at: '2025-01-13T15:00:00Z' }], unread_count: 2 }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/notifications/read/`, () => {
    return HttpResponse.json({ success: true, data: { marked_count: 1 }, message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/notifications/unread-count/`, () => {
    return HttpResponse.json({ success: true, data: { count: 2 }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Profile ───────────────────────────────────────────────────────────────
  http.get(`${API}/auth/profile/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'user-1', email: 'test@example.com', username: 'testuser', full_name: 'Test User', avatar: '', native_language: 'uz', learning_language: 'en', proficiency_level: 'B1', daily_goal: 10, timezone: 'Asia/Tashkent', is_premium: false, premium_until: null, is_premium_active: false, is_active: true, date_joined: '2025-01-01', last_login: '2025-01-15', has_completed_onboarding: true }, message: 'OK', errors: null, meta: null });
  }),

  http.patch(`${API}/auth/profile/`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    return HttpResponse.json({ success: true, data: { id: 'user-1', email: 'test@example.com', username: 'testuser', full_name: (body.full_name as string) || 'Test User', avatar: '', native_language: 'uz', learning_language: 'en', proficiency_level: (body.proficiency_level as string) || 'B1', daily_goal: (body.daily_goal as number) || 10, timezone: (body.timezone as string) || 'Asia/Tashkent', is_premium: false, premium_until: null, is_premium_active: false, is_active: true, date_joined: '2025-01-01', last_login: '2025-01-15', has_completed_onboarding: true }, message: 'Updated', errors: null, meta: null });
  }),

  http.post(`${API}/auth/change-password/`, () => {
    return HttpResponse.json({ success: true, data: null, message: 'Password changed successfully', errors: null, meta: null });
  }),

  // ─── Learning Profile ──────────────────────────────────────────────────────
  http.get(`${API}/learning-profile/`, () => {
    return HttpResponse.json({ success: true, data: { preferred_style: 'visual', style_confidence: { visual: 0.75, auditory: 0.45, reading_writing: 0.60, kinesthetic: 0.35 }, best_time: { hours: [9, 10, 11], days: ['Monday', 'Wednesday', 'Friday'] }, session_stats: { avg_duration: 1200, avg_words: 8, total_sessions: 45 }, skills: { vocabulary: 72, grammar: 55, reading: 80, listening: 45, writing: 60 }, difficulty_level: 'B1', last_analyzed: '2025-01-15' }, message: 'OK', errors: null, meta: null });
  }),

  http.post(`${API}/learning-profile/analyze/`, () => {
    return HttpResponse.json({ success: true, data: { learning_style: 'visual', optimal_time: { hours: [9, 10, 11], days: ['Monday', 'Wednesday', 'Friday'] }, skills: { vocabulary: 72, grammar: 55, reading: 80, listening: 45, writing: 60 }, recommendations: ['Focus on listening exercises', 'Practice grammar daily'] }, message: 'Analysis complete', errors: null, meta: null });
  }),

  http.get(`${API}/learning-profile/mistake-patterns/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'mp1', type: 'grammar', description: 'Mixing up past tense forms', examples: ['goed instead of went'], occurrence_count: 12, is_resolved: false, related_words: [] }, { id: 'mp2', type: 'spelling', description: 'Common vowel confusion', examples: ['recieve instead of receive'], occurrence_count: 8, is_resolved: false, related_words: [] }, { id: 'mp3', type: 'meaning', description: 'Confusing similar words', examples: ['affect vs effect'], occurrence_count: 5, is_resolved: true, related_words: [] }], message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/learning-profile/recommendations/`, () => {
    return HttpResponse.json({ success: true, data: [{ id: 'r1', word: 'accomplish', translation: 'bajarmoq', reason: 'Common B1 academic word', reason_type: 'academic', priority: 1, is_accepted: false, ai_confidence: 0.85 }, { id: 'r2', word: 'frequently', translation: 'tez-tez', reason: 'High frequency word', reason_type: 'frequency', priority: 2, is_accepted: false, ai_confidence: 0.78 }], message: 'OK', errors: null, meta: null });
  }),

  http.get(`${API}/learning-profile/domain-coverage/`, () => {
    return HttpResponse.json({ success: true, data: { academic: { total: 100, coverage: 35, mastered: 20 }, business: { total: 80, coverage: 25, mastered: 10 }, technology: { total: 60, coverage: 40, mastered: 15 }, daily_life: { total: 120, coverage: 65, mastered: 50 }, science: { total: 50, coverage: 20, mastered: 5 } }, message: 'OK', errors: null, meta: null });
  }),

  // ─── Review Daily Progress ─────────────────────────────────────────────────
  http.get(`${API}/review/daily-progress/`, () => {
    return HttpResponse.json({ success: true, data: { id: 'dp-1', words_reviewed: 7, words_added: 2, words_mastered: 1, correct_answers: 6, incorrect_answers: 1, total_time_seconds: 1200, goal_completed: false, xp_earned: 35, date: '2025-01-15' }, message: 'OK', errors: null, meta: null });
  }),
];
