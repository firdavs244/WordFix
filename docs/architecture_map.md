# WordFix — Architecture Map

> Bu fayl loyihaning texnik arxitekturasini batafsil tavsiflaydi.
> Har sprint oxirida yangilanadi.
> Oxirgi yangilangan: 2026-02-27

### CHANGELOG (2026-02-27 Audit)

- Model soni 30 → 31 ga tuzatildi (haqiqiy kod bazasidan sanaldi)
- Endpoint soni ~96 → 103 ga tuzatildi (barcha urls.py fayllaridan sanaldi)
- Use Case soni ~42 → 87 ga tuzatildi (barcha use_cases/ papkalaridan sanaldi)
- Use Case Map to'liq qayta yozildi — Games bo'limiga Synonym-Antonym va Irregular Verbs qo'shildi
- Badge soni 18 → 31 ga tuzatildi (badge_service.py dan tekshirildi)
- Frontend Route Map 31 → 34 ga tuzatildi (routes/index.tsx dan sanaldi)
- Middleware Stack da RequestIDMiddleware #10 → #2 ga ko'chirish TAVSIYA qilindi
- Admin Panel sprint raqami 13-14 → 16-17 ga tuzatildi (Sprint Roadmap ga moslandi)
- Contact/Feedback sprint raqami 14 → 15 ga tuzatildi
- API Documentation endpointlari qo'shildi (SpectacularSwaggerView, SpectacularAPIView)
- Yangi Section 11: "Ma'lum Arxitektura Muammolar (Texnik Qarz)" qo'shildi

---

## 1. DATABASE MODELLARI (31 ta model, ~1,400 qator)

### Common App

```
AbstractBaseModel (apps/common/models.py) [ABSTRACT]
├── id          (UUIDField, pk, uuid4)
├── created_at  (DateTimeField, auto_now_add)
├── updated_at  (DateTimeField, auto_now)
└── is_active   (BooleanField, default=True)
Methods: soft_delete(), restore()
```

### Users App — Auth & Profile

```
CustomUser (apps/users/infrastructure/models/user_models.py)
├── id                        (UUIDField, pk)
├── email                     (EmailField, unique, db_index)
├── username                  (CharField(30), unique)
├── full_name                 (CharField(100), blank)
├── avatar                    (ImageField, upload_to=avatars/)
├── native_language           (CharField(10), default="uz")
├── learning_language         (CharField(10), default="en")
├── proficiency_level         (CharField(2), choices=A1-C2, default="A1")
├── daily_goal                (PositiveIntegerField, default=10)
├── timezone                  (CharField(50), default="Asia/Tashkent")
├── is_premium                (BooleanField, default=False)
├── premium_until             (DateTimeField, null)
├── is_active                 (BooleanField, default=True)
├── is_staff                  (BooleanField, default=False)
├── has_completed_onboarding  (BooleanField, default=False)
├── date_joined               (DateTimeField, auto_now_add)
└── last_login                (DateTimeField, null)
Extends: AbstractBaseUser, PermissionsMixin
Property: is_premium_active → bool
```

### Users App — Progress & Gamification

```
UserProgress (1:1 → CustomUser)
├── total_xp, level, words_learned_total, words_mastered_total
├── tests_completed, games_played, reviews_completed, perfect_scores
└── total_study_time_seconds

XPTransaction (FK → CustomUser)
├── amount (int, + yoki -)
├── reason (16 ta choices: word_added, review_correct, test_complete, etc.)
└── description

Badge
├── code (unique), name, description, icon
├── category (words/streak/review/test/game/mastery/level/combo/challenge)
├── xp_reward, rarity (common/rare/epic/legendary)

UserBadge (FK → CustomUser, FK → Badge)
├── earned_at
└── unique_together: [user, badge]

Notification (FK → CustomUser)
├── type (7 ta: review_reminder, streak_warning, badge_earned, level_up, daily_goal_complete, word_mastered, weekly_report)
├── title, message, is_read, data (JSON)

OnboardingQuestion
├── level (A1-C2), question_text, correct_answer, options (JSON), order

OnboardingResult (1:1 → CustomUser)
├── answers (JSON), determined_level, total_correct, total_questions
```

### Users App — Learning

```
LearningProfile (1:1 → CustomUser)
├── preferred_style (visual/auditory/reading/kinesthetic)
├── style_confidence, best_hour_start, best_hour_end, best_days (JSON)
├── avg_session_duration, optimal_words_per_session, avg_retention_rate
├── strongest_skills (JSON), weakest_skills (JSON)
├── current_difficulty_level, difficulty_adjustment_rate
└── last_analyzed_at, analysis_data (JSON)

MistakePattern (FK → CustomUser)
├── pattern_type (7 ta: l1_interference, morphological, semantic, phonological, spelling, collocation, grammar)
├── description, examples (JSON), occurrence_count
├── is_resolved, drills_completed, success_rate_after_drills, related_words (JSON)

DomainCoverage (FK → CustomUser)
├── domain (10 ta: academic, business, technology, daily_life, ...)
├── total_words_in_domain, coverage_percentage, mastered_count, learning_count
└── unique_together: [user, domain]

WordRecommendation (FK → CustomUser)
├── recommended_word, translation, reason, reason_type
├── priority_score, is_accepted, is_dismissed, ai_confidence, source_data (JSON)

SessionPerformance (FK → CustomUser)
├── session_type (review/test/game/chat)
├── started_at, ended_at, hour_of_day, day_of_week
├── accuracy, completion_rate, engagement_score, effectiveness_score
```

### Words App — Core

```
WordCategory (extends AbstractBaseModel, FK → User)
├── name (CharField(50)), color (CharField(7), hex), icon, words_count
└── unique_together: [user, name]

Word (extends AbstractBaseModel, FK → User, FK → WordCategory nullable)
├── original_word (CharField(100), db_index)
├── translation, pronunciation, part_of_speech (10 choices)
├── definition, example_sentence, example_translation
├── synonyms (JSON), antonyms (JSON), collocations (JSON), word_family (JSON)
├── image_url, audio_url, notes, mnemonic, usage_notes
├── tags (JSON), difficulty_level (easy/medium/hard)
├── is_enriched, enrichment_status (pending/enriching/enriched/failed), enrichment_error, enriched_at
├── confidence_score (0-100), next_review_at, review_count, correct_count, incorrect_count
├── last_reviewed_at, is_mastered, easiness_factor (SM-2), repetition_number, interval_days
├── is_archived, archived_at
└── unique_together: [user, original_word]
Indexes: [user+is_mastered], [user+confidence_score], [user+next_review_at], [user+category], [user+is_archived]

WordDistractor (extends AbstractBaseModel, FK → Word)
├── distractors (JSON), language (default="uz"), generated_by (ai/fallback)
└── unique_together: [word, language]
```

### Words App — Review

```
ReviewSession (extends AbstractBaseModel, FK → User)
├── started_at, completed_at, total_words, correct_count, incorrect_count
├── average_quality, duration_seconds, session_type (5 choices), is_completed
├── current_combo, max_combo, combo_xp_bonus

ReviewLog (extends AbstractBaseModel, FK → ReviewSession nullable, FK → User, FK → Word)
├── quality (0-5), response_time_ms, is_correct, reviewed_at
├── previous_confidence, new_confidence, previous_interval, new_interval

DailyStreak (extends AbstractBaseModel, 1:1 → User)
├── current_streak, longest_streak, last_activity_date, streak_frozen_until, total_review_days

DailyActivity (extends AbstractBaseModel, FK → User)
├── date, words_reviewed, words_added, words_mastered
├── correct_answers, incorrect_answers, total_time_seconds, goal_completed, xp_earned
└── unique_together: [user, date]
```

### Words App — Tests

```
TestSession (extends AbstractBaseModel, FK → User, M2M → Word through TestQuestion)
├── test_type (multiple_choice/fill_blank/context_guess/mixed)
├── difficulty (easy/medium/hard/adaptive)
├── total_questions, correct_answers, incorrect_answers, score_percentage
├── started_at, completed_at, duration_seconds, is_completed
├── current_combo, max_combo, combo_xp_bonus

TestQuestion (extends AbstractBaseModel, FK → TestSession, FK → Word)
├── question_type (6 choices), question_text, correct_answer
├── options (JSON), user_answer, is_correct, response_time_ms, explanation, order
```

### Words App — Games

```
GameSession (extends AbstractBaseModel, FK → User)
├── game_type (7 ta: speed_round, word_match, word_context, story_builder, listening_challenge, synonym_antonym, irregular_verbs)
├── score, max_score, correct_answers, incorrect_answers
├── duration_seconds, started_at, completed_at, is_completed
├── level, xp_earned, current_combo, max_combo, combo_xp_bonus

StoryRound (FK → GameSession)
├── round_number, ai_text, user_text, target_words (JSON), words_used (JSON)
├── grammar_corrections (JSON), is_correct_usage, score

ListeningRound (FK → GameSession, FK → Word)
├── round_number, correct_answer, user_answers (JSON)
├── attempts_used, max_attempts (3), is_correct, hints_shown (JSON), score

SynonymAntonymRound (FK → GameSession)
├── round_number, question_type (synonym/antonym), word_text
├── correct_answer, options (JSON), user_answer, is_correct, score

IrregularVerbRound (FK → GameSession)
├── round_number, infinitive, translation
├── correct_past_simple, correct_past_participle
├── user_past_simple, user_past_participle
├── past_simple_correct, past_participle_correct
├── attempts_used, hints_shown (JSON), score
```

### Words App — Chat

```
ChatSession (FK → User, M2M → Word)
├── topic, started_at, ended_at, message_count
├── target_words (JSON), is_active

ChatMessage (FK → ChatSession)
├── role (user/assistant), content, corrections (JSON), words_used (JSON), order
```

### Words App — Other

```
ConfusingPair (extends AbstractBaseModel, FK → User, FK → Word x2)
├── confusion_count, last_confused_at, is_resolved, drill_data (JSON)
└── unique_together: [user, word_1, word_2]

DailyChallenge (extends AbstractBaseModel, FK → User)
├── date, challenges (JSON), all_completed, bonus_claimed
└── unique_together: [user, date]
```

---

## 2. API ENDPOINT MAP (103 ta endpoint)

### API DOCUMENTATION (2 ta endpoint)

```
GET    /api/schema/                         → SpectacularAPIView      [AllowAny]
GET    /api/docs/                           → SpectacularSwaggerView  [AllowAny]
```

> ℹ️ Redoc endpoint hozircha yo'q. Kerak bo'lsa config/urls.py ga `SpectacularRedocView` qo'shish mumkin.

### AUTH (9 ta endpoint)

```
POST   /api/v1/auth/register/              → RegisterView           [AllowAny]
POST   /api/v1/auth/login/                 → LoginView              [AllowAny]
POST   /api/v1/auth/logout/                → LogoutView             [Auth]
POST   /api/v1/auth/token/refresh/         → TokenRefreshView       [AllowAny]
GET|PATCH /api/v1/auth/profile/            → ProfileView            [Auth]
POST   /api/v1/auth/change-password/       → ChangePasswordView     [Auth]
POST   /api/v1/auth/google/               → GoogleLoginView         [AllowAny]
GET    /api/v1/auth/providers/             → GoogleAuthStatusView    [AllowAny]
GET    /api/v1/health/                     → HealthCheckView         [AllowAny]
```

### ONBOARDING (4 ta endpoint)

```
GET    /api/v1/auth/onboarding/questions/  → OnboardingQuestionsView [AllowAny]
POST   /api/v1/auth/onboarding/submit/     → OnboardingSubmitView   [Auth]
POST   /api/v1/auth/onboarding/skip/       → OnboardingSkipView     [Auth]
GET    /api/v1/auth/onboarding/status/     → OnboardingStatusView   [Auth]
```

### PROGRESS (4 ta endpoint)

```
GET    /api/v1/users/progress/             → UserProgressView       [Auth]
GET    /api/v1/users/xp-history/           → XPHistoryView          [Auth]
GET    /api/v1/users/badges/               → UserBadgesView         [Auth]
GET    /api/v1/badges/                     → AllBadgesView          [Auth]
```

### NOTIFICATIONS (3 ta endpoint)

```
GET    /api/v1/notifications/              → NotificationListView        [Auth]
POST   /api/v1/notifications/read/         → NotificationMarkReadView    [Auth]
GET    /api/v1/notifications/unread-count/ → NotificationUnreadCountView [Auth]
```

### LEARNING PROFILE (6 ta endpoint)

```
GET    /api/v1/learning-profile/               → LearningProfileView        [Auth]
POST   /api/v1/learning-profile/analyze/       → AnalyzeLearningProfileView [Auth]
GET    /api/v1/learning-profile/mistake-patterns/ → MistakePatternsView     [Auth]
GET|POST /api/v1/learning-profile/recommendations/ → WordRecommendationsView [Auth]
GET    /api/v1/learning-profile/domain-coverage/ → DomainCoverageView       [Auth]
GET    /api/v1/learning-profile/difficulty/     → AdaptiveDifficultyView    [Auth]
```

### WORDS (19 ta endpoint)

```
GET|POST /api/v1/words/                        → WordListCreateView        [Auth]
POST   /api/v1/words/bulk/                     → WordBulkCreateView        [Auth]
GET    /api/v1/words/stats/                    → WordStatsView             [Auth]
GET    /api/v1/words/review/                   → WordReviewView            [Auth]
POST   /api/v1/words/enrich-all/               → EnrichAllView             [Auth]
POST   /api/v1/words/import/analyze/           → AnalyzeTextView           [Auth]
POST   /api/v1/words/import/add/               → ImportAddWordsView        [Auth]
POST   /api/v1/words/import/csv/validate/      → CSVValidateView           [Auth]
POST   /api/v1/words/import/csv/               → CSVImportView             [Auth]
GET|PATCH|DELETE /api/v1/words/<id>/            → WordDetailView            [Auth]
POST   /api/v1/words/<id>/enrich/              → EnrichWordView            [Auth]
GET    /api/v1/words/<id>/enrichment-status/   → EnrichmentStatusView      [Auth]
POST   /api/v1/words/<id>/enrichment-retry/    → EnrichmentRetryView       [Auth]
GET|POST /api/v1/words/categories/             → WordCategoryListCreateView [Auth]
DELETE /api/v1/words/categories/<id>/          → WordCategoryDeleteView    [Auth]
POST   /api/v1/words/<id>/archive/             → ArchiveWordView           [Auth]
POST   /api/v1/words/<id>/unarchive/           → UnarchiveWordView         [Auth]
GET    /api/v1/words/archived/                 → ArchivedWordsListView     [Auth]
POST   /api/v1/words/archive/bulk/             → BulkArchiveView           [Auth]
```

### CONFUSING PAIRS (5 ta endpoint)

```
GET    /api/v1/words/confusing-pairs/          → ConfusingPairsListView   [Auth]
GET    /api/v1/words/confusing-pairs/count/    → ConfusingPairCountView   [Auth]
GET    /api/v1/words/confusing-pairs/<id>/     → ConfusingPairDetailView  [Auth]
POST   /api/v1/words/confusing-pairs/<id>/drill/ → ConfusingPairDrillView [Auth]
POST   /api/v1/words/confusing-pairs/<id>/resolve/ → ConfusingPairResolveView [Auth]
```

### REVIEW (10 ta endpoint)

```
GET    /api/v1/review/words/                       → ReviewWordsView          [Auth]
POST   /api/v1/review/sessions/                    → ReviewSessionCreateView  [Auth]
GET    /api/v1/review/sessions/<id>/               → ReviewSessionDetailView  [Auth]
POST   /api/v1/review/sessions/<id>/answer/        → SubmitAnswerView         [Auth]
POST   /api/v1/review/sessions/<id>/complete/      → CompleteSessionView      [Auth]
GET    /api/v1/review/summary/                     → ReviewSummaryView        [Auth]
GET    /api/v1/review/history/                     → ReviewHistoryView        [Auth]
GET    /api/v1/review/streak/                      → StreakView               [Auth]
GET    /api/v1/review/daily-progress/              → DailyProgressView        [Auth]
GET    /api/v1/review/words/<id>/predict/          → PredictedIntervalsView   [Auth]
```

### TESTS (5 ta endpoint)

```
POST   /api/v1/tests/generate/                 → TestGenerateView        [Auth]
GET    /api/v1/tests/history/                  → TestHistoryView         [Auth]
GET    /api/v1/tests/<id>/                     → TestSessionDetailView   [Auth]
POST   /api/v1/tests/<id>/answer/              → TestSubmitAnswerView    [Auth]
POST   /api/v1/tests/<id>/complete/            → TestCompleteView        [Auth]
```

### GAMES (20 ta endpoint)

```
POST   /api/v1/games/speed-round/start/        → SpeedRoundStartView     [Auth]
POST   /api/v1/games/speed-round/submit/       → SpeedRoundSubmitView    [Auth]
POST   /api/v1/games/word-match/start/         → WordMatchStartView      [Auth]
POST   /api/v1/games/word-match/submit/        → WordMatchSubmitView     [Auth]
POST   /api/v1/games/word-context/start/       → WordContextStartView    [Auth]
POST   /api/v1/games/word-context/submit/      → WordContextSubmitView   [Auth]
POST   /api/v1/games/story-builder/start/      → StoryBuilderStartView   [Auth]
POST   /api/v1/games/story-builder/submit/     → StoryBuilderSubmitView  [Auth]
POST   /api/v1/games/story-builder/complete/   → StoryBuilderCompleteView [Auth]
POST   /api/v1/games/listening/start/          → ListeningStartView      [Auth]
POST   /api/v1/games/listening/answer/         → ListeningAnswerView     [Auth]
POST   /api/v1/games/listening/complete/       → ListeningCompleteView   [Auth]
POST   /api/v1/games/synonym-antonym/start/    → SynonymAntonymStartView [Auth]
POST   /api/v1/games/synonym-antonym/answer/   → SynonymAntonymAnswerView [Auth]
POST   /api/v1/games/synonym-antonym/complete/ → SynonymAntonymCompleteView [Auth]
POST   /api/v1/games/irregular-verbs/start/    → IrregularVerbsStartView [Auth]
POST   /api/v1/games/irregular-verbs/answer/   → IrregularVerbsAnswerView [Auth]
POST   /api/v1/games/irregular-verbs/complete/ → IrregularVerbsCompleteView [Auth]
GET    /api/v1/games/history/                  → GameHistoryView         [Auth]
GET    /api/v1/games/stats/                    → GameStatsView           [Auth]
```

### CHAT (5 ta endpoint)

```
POST   /api/v1/chat/start/                     → ChatStartView           [Auth]
GET    /api/v1/chat/history/                   → ChatHistoryView         [Auth]
GET    /api/v1/chat/sessions/<id>/             → ChatSessionDetailView   [Auth]
POST   /api/v1/chat/sessions/<id>/message/     → ChatSendMessageView     [Auth]
POST   /api/v1/chat/sessions/<id>/end/         → ChatEndView             [Auth]
```

### ANALYTICS (6 ta endpoint)

```
GET    /api/v1/analytics/overview/             → AnalyticsOverviewView       [Auth]
GET    /api/v1/analytics/weekly/               → AnalyticsWeeklyView         [Auth]
GET    /api/v1/analytics/monthly/              → AnalyticsMonthlyView        [Auth]
GET    /api/v1/analytics/difficult-words/      → AnalyticsDifficultWordsView [Auth]
GET    /api/v1/analytics/word-progress/        → AnalyticsWordProgressView   [Auth]
GET    /api/v1/analytics/calendar/             → AnalyticsCalendarView       [Auth]
```

### CHALLENGES (2 ta endpoint)

```
GET    /api/v1/challenges/today/               → DailyChallengesView     [Auth]
POST   /api/v1/challenges/claim/               → ClaimDailyBonusView     [Auth]
```

### SYSTEM (4 ta endpoint)

```
GET    /api/v1/system/health/detailed/         → DetailedHealthCheckView  [AllowAny]
GET    /api/v1/system/config/status/           → ConfigStatusView         [AllowAny]
GET    /api/v1/system/ai-status/               → AIStatusView             [Auth]
POST   /api/v1/system/ai-ping/                 → AIPingView               [Auth]
```

---

## 3. USE CASE MAP (87 ta use case)

### Users — Auth (3 ta)

| Use Case            | Fayl              | Nima qiladi                      |
| ------------------- | ----------------- | -------------------------------- |
| RegisterUserUseCase | auth_use_cases.py | Yangi user yaratish + JWT token  |
| LoginUserUseCase    | auth_use_cases.py | Email/pass login + JWT token     |
| GoogleLoginUseCase  | auth_use_cases.py | Google OAuth login yoki register |

### Users — Profile (6 ta)

| Use Case                      | Fayl                 | Nima qiladi                       |
| ----------------------------- | -------------------- | --------------------------------- |
| GetUserProfileUseCase         | profile_use_cases.py | Profil olish                      |
| UpdateUserProfileUseCase      | profile_use_cases.py | Profil yangilash (allowed fields) |
| ChangePasswordUseCase         | profile_use_cases.py | Parol o'zgartirish                |
| GetOnboardingQuestionsUseCase | profile_use_cases.py | Assessment savollar               |
| SubmitOnboardingResultUseCase | profile_use_cases.py | Javob tekshirish → CEFR level     |
| SkipOnboardingUseCase         | profile_use_cases.py | Onboarding skip → A1              |

### Users — Learning (9 ta)

| Use Case                        | Fayl                | Nima qiladi                           |
| ------------------------------- | ------------------- | ------------------------------------- |
| GetLearningProfileUseCase       | learning_profile.py | Learning profil olish (get_or_create) |
| AnalyzeLearningProfileUseCase   | learning_profile.py | Tahlil: style, schedule, skills       |
| GetAdaptiveDifficultyUseCase    | learning_profile.py | Qiyinlik tavsiyasi                    |
| GetMistakePatternsUseCase       | mistake_patterns.py | Xato patternlar ro'yxati              |
| RecordMistakeUseCase            | mistake_patterns.py | Yangi xato yozish                     |
| GetWordRecommendationsUseCase   | recommendations.py  | AI tavsiyalar generate                |
| AcceptRecommendationUseCase     | recommendations.py  | Tavsiyani qabul → so'z qo'shish       |
| UpdateDomainCoverageUseCase     | domain_coverage.py  | Domain qoplanish hisobi               |
| RecordSessionPerformanceUseCase | performance.py      | Sessiya natijasi yozish               |

### Words — CRUD (8 ta)

| Use Case             | Fayl         | Nima qiladi                             |
| -------------------- | ------------ | --------------------------------------- |
| AddWordUseCase       | word_crud.py | So'z qo'shish + XP + enrichment trigger |
| GetWordsUseCase      | word_crud.py | So'zlar ro'yxati (filtered, paginated)  |
| GetWordDetailUseCase | word_crud.py | Bitta so'z detail                       |
| UpdateWordUseCase    | word_crud.py | So'z yangilash                          |
| DeleteWordUseCase    | word_crud.py | So'z o'chirish                          |
| BulkAddWordsUseCase  | word_crud.py | Bulk so'z qo'shish                      |
| GetWordStatsUseCase  | word_crud.py | So'z statistikasi                       |
| SearchWordsUseCase   | word_crud.py | So'z qidirish                           |

### Words — Archive (4 ta)

| Use Case                | Fayl            | Nima qiladi        |
| ----------------------- | --------------- | ------------------ |
| ArchiveWordUseCase      | word_archive.py | So'z arxivlash     |
| UnarchiveWordUseCase    | word_archive.py | Arxivdan qaytarish |
| GetArchivedWordsUseCase | word_archive.py | Arxiv ro'yxati     |
| BulkArchiveUseCase      | word_archive.py | Bulk arxivlash     |

### Words — Enrichment (2 ta)

| Use Case           | Fayl          | Nima qiladi                           |
| ------------------ | ------------- | ------------------------------------- |
| EnrichWordUseCase  | enrichment.py | AI bilan so'z boyitish (Celery async) |
| BatchEnrichUseCase | enrichment.py | Ko'p so'zlarni boyitish               |

### Words — Import (4 ta)

| Use Case           | Fayl            | Nima qiladi                                 |
| ------------------ | --------------- | ------------------------------------------- |
| AnalyzeTextUseCase | smart_import.py | AI-First matn tahlil (2-bosqichli pipeline) |
| ImportWordsUseCase | smart_import.py | Import so'zlarni qo'shish                   |
| ValidateCSVUseCase | smart_import.py | CSV fayl tekshirish                         |
| CSVImportUseCase   | smart_import.py | CSV dan import                              |

### Words — Review (5 ta)

| Use Case                     | Fayl      | Nima qiladi               |
| ---------------------------- | --------- | ------------------------- |
| GetReviewWordsUseCase        | review.py | Due words for review      |
| StartReviewSessionUseCase    | review.py | Yangi review sessiya      |
| SubmitReviewAnswerUseCase    | review.py | Javob + SM-2 + combo + XP |
| CompleteReviewSessionUseCase | review.py | Sessiya tugatish + badge  |
| GetReviewSummaryUseCase      | review.py | Review summary            |

### Words — Streak (1 ta)

| Use Case            | Fayl      | Nima qiladi      |
| ------------------- | --------- | ---------------- |
| UpdateStreakUseCase | streak.py | Streak yangilash |

### Words — Tests (5 ta)

| Use Case                   | Fayl               | Nima qiladi                |
| -------------------------- | ------------------ | -------------------------- |
| GenerateTestUseCase        | test_generation.py | AI test generatsiya        |
| SubmitTestAnswerUseCase    | test_session.py    | Test javob berish          |
| CompleteTestSessionUseCase | test_session.py    | Test tugatish + XP + badge |
| GetTestHistoryUseCase      | test_session.py    | Test tarixi                |
| GetTestDetailUseCase       | test_session.py    | Test detail                |

### Words — Games (20 ta)

| Use Case                          | Fayl               | O'yin           | Nima qiladi            |
| --------------------------------- | ------------------ | --------------- | ---------------------- |
| StartSpeedRoundUseCase            | speed_round.py     | Speed Round     | Boshlash               |
| SubmitSpeedRoundUseCase           | speed_round.py     | Speed Round     | Natija                 |
| StartWordMatchUseCase             | word_match.py      | Word Match      | Boshlash               |
| SubmitWordMatchUseCase            | word_match.py      | Word Match      | Natija                 |
| StartWordContextUseCase           | word_context.py    | Word Context    | Boshlash (AI)          |
| SubmitWordContextUseCase          | word_context.py    | Word Context    | Natija                 |
| StartStoryBuilderUseCase          | story_builder.py   | Story Builder   | Boshlash (AI hikoya)   |
| SubmitStoryRoundUseCase           | story_builder.py   | Story Builder   | Round submit (AI eval) |
| CompleteStoryBuilderUseCase       | story_builder.py   | Story Builder   | Tugatish + XP          |
| StartListeningChallengeUseCase    | listening.py       | Listening       | Boshlash (TTS)         |
| SubmitListeningAnswerUseCase      | listening.py       | Listening       | Javob                  |
| CompleteListeningChallengeUseCase | listening.py       | Listening       | Tugatish + XP          |
| StartSynonymAntonymUseCase        | synonym_antonym.py | Synonym-Antonym | Boshlash               |
| SubmitSynonymAntonymUseCase       | synonym_antonym.py | Synonym-Antonym | Javob                  |
| CompleteSynonymAntonymUseCase     | synonym_antonym.py | Synonym-Antonym | Tugatish + XP          |
| StartIrregularVerbsUseCase        | irregular_verbs.py | Irregular Verbs | Boshlash               |
| SubmitIrregularVerbUseCase        | irregular_verbs.py | Irregular Verbs | Javob                  |
| CompleteIrregularVerbsUseCase     | irregular_verbs.py | Irregular Verbs | Tugatish + XP          |
| GetGameHistoryUseCase             | game_stats.py      | Barcha          | O'yin tarixi           |
| GetGameStatsUseCase               | game_stats.py      | Barcha          | O'yin statistikasi     |

### Words — Chat (5 ta)

| Use Case                    | Fayl    | Nima qiladi               |
| --------------------------- | ------- | ------------------------- |
| StartChatUseCase            | chat.py | AI chat sessiya boshlash  |
| SendChatMessageUseCase      | chat.py | Xabar yuborish (AI javob) |
| EndChatUseCase              | chat.py | Chat tugatish             |
| GetChatHistoryUseCase       | chat.py | Chat tarixi               |
| GetChatSessionDetailUseCase | chat.py | Chat sessiya detail       |

### Words — Confusing Pairs (6 ta)

| Use Case                      | Fayl               | Nima qiladi          |
| ----------------------------- | ------------------ | -------------------- |
| DetectConfusionUseCase        | confusing_pairs.py | Chalkash aniqlash    |
| GetConfusingPairsUseCase      | confusing_pairs.py | Juftliklar ro'yxati  |
| GetConfusingPairDetailUseCase | confusing_pairs.py | Juftlik detail       |
| GenerateConfusionDrillUseCase | confusing_pairs.py | Mashq generatsiya    |
| ResolveConfusingPairUseCase   | confusing_pairs.py | Juftlikni hal qilish |
| GetConfusingPairCountUseCase  | confusing_pairs.py | Juftliklar soni      |

### Words — Daily Challenges (3 ta)

| Use Case                       | Fayl                | Nima qiladi     |
| ------------------------------ | ------------------- | --------------- |
| GetDailyChallengesUseCase      | daily_challenges.py | Bugungi         |
| UpdateChallengeProgressUseCase | daily_challenges.py | Progress yozish |
| ClaimDailyBonusUseCase         | daily_challenges.py | Bonus XP        |

### Words — Analytics (6 ta)

| Use Case                    | Fayl         | Nima qiladi           |
| --------------------------- | ------------ | --------------------- |
| GetAnalyticsOverviewUseCase | analytics.py | Umumiy statistika     |
| GetWeeklyStatsUseCase       | analytics.py | Haftalik statistika   |
| GetMonthlyStatsUseCase      | analytics.py | Oylik statistika      |
| GetDifficultWordsUseCase    | analytics.py | Qiyin so'zlar         |
| GetWordProgressUseCase      | analytics.py | So'z progress data    |
| GetStudyCalendarUseCase     | analytics.py | Calendar heatmap data |

---

## 4. SERVICE DEPENDENCIES

### AI Provider Flow

```
Views → Use Cases → AIProviderFactory.get_provider()
                         │
                    ┌────┴────┐
                    │ Circuit │
                    │ Breaker │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    GroqProvider   GeminiProvider   OpenAIProvider
    (PRIMARY)      (FALLBACK 1)    (FALLBACK 2)
         │               │               │
         └───────────────┼───────────────┘
                         │ (barcha fail)
                         ▼
                FallbackAIProvider
                (hardcoded responses)
```

### XP → Badge → Notification Flow

```
User harakati (review, test, game...)
    │
    ▼
XPService.award_xp()          → XPTransaction yaratiladi
    │                           → UserProgress.total_xp yangilanadi
    │                           → Level up tekshiriladi
    ▼
BadgeService.check_and_award() → Barcha 31 ta badge sharti tekshiriladi
    │                           → UserBadge yaratiladi (agar sharti bajarilsa)
    ▼
NotificationService.create()   → Notification yaratiladi (in-app)
```

### Review SM-2 Flow

```
SubmitReviewAnswerUseCase
    │
    ├── SpacedRepetitionService.calculate_review()
    │       → quality → EF, interval, repetition → confidence, is_mastered
    │
    ├── ComboService.update_combo()
    │       → is_correct → current_combo++ / reset
    │       → combo XP bonus (5/12/20/30/50)
    │
    ├── XPService.award_xp()
    │       → review_correct/incorrect XP
    │       → combo_bonus_xp
    │
    ├── BadgeService.check_and_award()
    │
    └── ConfusingPair auto-detect
            → 2+ xato → ConfusingPair yaratiladi
```

### Import AI-First Pipeline (Sprint 12.4)

```
User matn kiritadi
    │
    ▼
_minimal_clean()         → URL, email, BOM tozalash
    │
    ▼
_full_ai_pipeline()
    ├── _ai_extract()    → AI Call #1: so'z ajratish + tarjima + CEFR + IPA
    │                      → JSON schema validation, dedup, normalize
    │
    └── _ai_validate()   → AI Call #2: tarjima to'g'riligini tekshirish
                           → non-English filtr, tuzatilganlarni belgilash
    │
    ▼
_format_suggestions()    → translation_source (user/ai/corrected/fallback)
    │                      → User library check (in_user_library flag)
    ▼
Frontend ga qaytarish
    │
    ▼ (fail bo'lsa)
_last_resort_fallback()  → import_helpers/ pipeline (regex-based)
```

---

## 5. FRONTEND FEATURE MAP

### Feature Modules (19 ta)

| Feature          | Components | Hooks                           | Pages                                | Tests | API           |
| ---------------- | ---------- | ------------------------------- | ------------------------------------ | ----- | ------------- |
| analytics        | 13         | useAnalytics                    | 1 (AnalyticsPage)                    | 5     | analyticsApi  |
| auth             | 13         | usePasswordValidation           | 2 (Login, Register)                  | —     | authApi       |
| badges           | 8          | useBadges                       | 1 (BadgesPage)                       | 5     | —             |
| challenges       | 3          | useChallenges                   | — (widget)                           | —     | challengeApi  |
| chat             | 17         | useChat                         | 3 (Chat, Session, History)           | 9     | chatApi       |
| confusing-pairs  | 8          | useConfusingPairs               | 1 (ConfusingPairsPage)               | 7     | confusingApi  |
| dashboard        | 29         | useDashboardData                | 1 (DashboardPage)                    | —     | —             |
| games            | 40+        | 6 hooks                         | 8 (Main + 7 games + Result)          | 13    | —             |
| import           | 13         | useCSVImport, useTextImport     | 1 (ImportPage)                       | 7     | importApi     |
| landing          | 12         | —                               | 1 (LandingPage)                      | —     | —             |
| learning-profile | 13         | useLearning, useLearningProfile | 1 (LearningProfilePage)              | 6     | learningApi   |
| notifications    | 6          | useNotifications                | 1 (NotificationsPage)                | 6     | —             |
| onboarding       | 11         | useOnboarding                   | 1 (OnboardingPage)                   | —     | onboardingApi |
| profile          | 9          | useProfile                      | 1 (ProfilePage)                      | 6     | —             |
| progress         | 6          | useProgress                     | 2 (Badges, Notifications)            | 1     | progressApi   |
| review           | 24         | useReview                       | 4 (Main, Session, Complete, History) | 10    | reviewApi     |
| system           | 4          | useSystemHealth                 | 1 (SystemStatusPage)                 | —     | systemApi     |
| tests            | 19         | useTests                        | 3 (Main, Session, Result)            | 12    | —             |
| words            | 20+        | useWords                        | 1 (WordsPage)                        | 5     | wordApi       |

### Zustand Stores (3 ta)

| Store          | State                                                   | Asosiy Actions                                   |
| -------------- | ------------------------------------------------------- | ------------------------------------------------ |
| useAuthStore   | user, isAuthenticated, isLoading                        | login, register, googleLogin, logout, initialize |
| useAppStore    | sidebarCollapsed                                        | toggleSidebar                                    |
| useReviewStore | currentSession, words, currentIndex, isFlipped, answers | flipCard, recordAnswer, nextWord, reset          |

### Route Map (34 ta)

| Route                       | Page                | Guard      | Feature          |
| --------------------------- | ------------------- | ---------- | ---------------- |
| /welcome                    | LandingPage         | Public     | landing          |
| /login                      | LoginPage           | Public     | auth             |
| /register                   | RegisterPage        | Public     | auth             |
| /onboarding                 | OnboardingPage      | Onboarding | onboarding       |
| /                           | DashboardPage       | Protected  | dashboard        |
| /words                      | WordsPage           | Protected  | words            |
| /review                     | ReviewPage          | Protected  | review           |
| /review/session/:sessionId  | ReviewSessionPage   | Protected  | review           |
| /review/complete/:sessionId | ReviewCompletePage  | Protected  | review           |
| /review/history             | ReviewHistoryPage   | Protected  | review           |
| /profile                    | ProfilePage         | Protected  | profile          |
| /tests                      | TestPage            | Protected  | tests            |
| /tests/session/:sessionId   | TestSessionPage     | Protected  | tests            |
| /tests/result/:sessionId    | TestResultPage      | Protected  | tests            |
| /games                      | GamesPage           | Protected  | games            |
| /games/speed-round          | SpeedRoundPage      | Protected  | games            |
| /games/word-match           | WordMatchPage       | Protected  | games            |
| /games/word-context         | WordContextPage     | Protected  | games            |
| /games/story-builder        | StoryBuilderPage    | Protected  | games            |
| /games/listening            | ListeningPage       | Protected  | games            |
| /games/synonym-antonym      | SynonymAntonymPage  | Protected  | games            |
| /games/irregular-verbs      | IrregularVerbsPage  | Protected  | games            |
| /games/result/:sessionId    | GameResultPage      | Protected  | games            |
| /badges                     | BadgesPage          | Protected  | progress         |
| /notifications              | NotificationsPage   | Protected  | progress         |
| /import                     | ImportPage          | Protected  | import           |
| /chat                       | ChatPage            | Protected  | chat             |
| /chat/session/:sessionId    | ChatSessionPage     | Protected  | chat             |
| /chat/history               | ChatHistoryPage     | Protected  | chat             |
| /analytics                  | AnalyticsPage       | Protected  | analytics        |
| /confusing-pairs            | ConfusingPairsPage  | Protected  | confusing-pairs  |
| /learning-profile           | LearningProfilePage | Protected  | learning-profile |
| /system                     | SystemStatusPage    | Protected  | system           |
| \*                          | NotFoundPage        | —          | shared           |

---

## 6. DOCKER SERVICE MAP (7 ta service)

```
┌─────────────────────────────────────────────────────────────┐
│                   docker-compose.yml (dev)                  │
├─────────────┬──────────────────┬────────────────────────────┤
│   db        │  postgres:16     │  :5433 → localhost         │
│   pgadmin   │  pgadmin4:9.8    │  :5050 → localhost         │
│   redis     │  redis:7-alpine  │  :6379 → localhost         │
│   web       │  Django/DRF      │  :8000, healthcheck        │
│   celery_w  │  celery worker   │  depends: web              │
│   celery_b  │  celery beat     │  DatabaseScheduler         │
│   frontend  │  Vite dev server │  :5173                     │
└─────────────┴──────────────────┴────────────────────────────┘

Production (docker-compose.prod.yml):
┌─────────────────────────────────────────────────────────────┐
│  nginx → / (frontend static) → gunicorn:8000 (/api, /admin)│
│  Bitta origin, CORS muammo yo'q                             │
└─────────────────────────────────────────────────────────────┘
```

### Volumes

| Volume        | Vazifasi                          |
| ------------- | --------------------------------- |
| postgres_data | PostgreSQL data persistence       |
| redis_data    | Redis data persistence            |
| media_data    | User uploaded files               |
| pgadmin_data  | PgAdmin configuration             |
| static_data   | (production) collectstatic output |
| backend_logs  | (production) log files            |

---

## 7. CELERY TASKS MAP

### Periodic Tasks (Celery Beat — DatabaseScheduler)

| Task                        | Schedule        | Nima qiladi                                           |
| --------------------------- | --------------- | ----------------------------------------------------- |
| update_streaks_task         | Har kuni        | Streak yangilash (faol bo'lmagan userlar uchun reset) |
| cleanup_stale_sessions_task | Har soatda      | Eskirgan review/test/game sessiyalarni tozalash       |
| review_reminder_task        | Har 12 soatda   | Due words bor userlarga in-app notification           |
| streak_warning_task         | Har kuni        | Bugun faol bo'lmagan userlarga ogohlantirish          |
| weekly_report_task          | Haftada 1 marta | Haftalik hisobot in-app notification                  |

### On-Demand Tasks (Celery Worker)

| Task                      | Trigger                   | Nima qiladi                    |
| ------------------------- | ------------------------- | ------------------------------ |
| enrich_word_task          | So'z qo'shilganda         | AI bilan so'z boyitish (async) |
| batch_enrich_words_task   | "Enrich All" bosilganda   | Ko'p so'zlarni boyitish        |
| generate_audio_task       | (mavjud, kam ishlatiladi) | TTS audio generatsiya          |
| generate_distractors_task | (mavjud)                  | AI distractor generatsiya      |

---

## 8. MIDDLEWARE / SIGNAL MAP

### Middleware Stack (hozirgi tartib — config/settings/base.py)

| #   | Middleware               | Vazifasi                 |
| --- | ------------------------ | ------------------------ |
| 1   | SecurityMiddleware       | Django security headers  |
| 2   | WhiteNoiseMiddleware     | Static files serving     |
| 3   | CorsMiddleware           | CORS headers (dev)       |
| 4   | SessionMiddleware        | Session handling         |
| 5   | CommonMiddleware         | Common Django middleware |
| 6   | CsrfViewMiddleware       | CSRF protection          |
| 7   | AuthenticationMiddleware | User authentication      |
| 8   | MessageMiddleware        | Django messages          |
| 9   | XFrameOptionsMiddleware  | Clickjacking protection  |
| 10  | RequestIDMiddleware      | X-Request-ID generation  |
| 11  | IdempotencyMiddleware    | POST idempotency         |
| 12  | RequestLoggingMiddleware | Request/response logging |
| 13  | AccountMiddleware        | django-allauth           |

> ⚠️ **MUAMMO:** RequestIDMiddleware hozir #10 o'rinda. Auth xatolari (401, 403) request ID siz loglanadi. Sprint 14 da #2 o'ringa ko'chirish kerak.

### Enterprise Patterns

| Pattern           | Fayl                             | Vazifasi                               |
| ----------------- | -------------------------------- | -------------------------------------- |
| Circuit Breaker   | apps/common/circuit_breaker.py   | AI provider failover                   |
| Rate Limiter      | apps/common/rate_limiter.py      | API throttling (anon/user/auth/CRUD)   |
| Idempotency       | apps/common/idempotency.py       | Duplicate POST prevention              |
| Custom Renderer   | apps/common/renderers.py         | {success, data, message, errors, meta} |
| Exception Handler | apps/common/exception_handler.py | Unified error response                 |

---

## 9. ADMIN PANEL ARXITEKTURA LOYIHASI (KELAJAK — Sprint 16-17)

### Backend Tuzilma (Sprint 16)

```
apps/admin_panel/
├── domain/
│   ├── entities.py          # AdminRole, AuditLogEntry dataclasses
│   └── repositories.py      # AbstractAdminRepo, AbstractAuditRepo
├── application/
│   ├── use_cases/
│   │   ├── dashboard.py     # GetDashboardStatsUseCase, GetDashboardChartsUseCase
│   │   ├── user_management.py # ListUsersUseCase, BanUserUseCase, etc.
│   │   ├── word_moderation.py # ListAllWordsUseCase, FlagWordUseCase
│   │   ├── ai_monitoring.py  # GetAIStatsUseCase, SwitchProviderUseCase
│   │   └── system_health.py  # GetSystemHealthUseCase
│   └── services/
│       └── audit_service.py  # AuditLogService
├── infrastructure/
│   ├── models.py            # AdminRole, AdminPermission, AuditLog models
│   └── repositories.py      # DjangoAdminRepo, DjangoAuditRepo
└── presentation/
    ├── views/
    │   ├── dashboard.py
    │   ├── users.py
    │   ├── words.py
    │   ├── ai_monitoring.py
    │   └── system_health.py
    ├── serializers/
    ├── urls.py
    └── permissions.py       # IsAdmin, IsModerator, IsSupport, IsAnalyst
```

### Frontend Tuzilma (Sprint 17)

```
features/admin/
├── api/adminApi.ts
├── components/
│   ├── AdminLayout.tsx, AdminSidebar.tsx
│   ├── DashboardStats.tsx, UserTable.tsx, UserDetail.tsx
│   ├── WordModerationTable.tsx
│   ├── AIMonitoringPanel.tsx, SystemHealthPanel.tsx
│   ├── ContactsTable.tsx, FeedbacksTable.tsx, BugReportsTable.tsx
├── hooks/
│   ├── useAdminDashboard.ts, useAdminUsers.ts, useAdminContacts.ts
└── pages/
    ├── AdminDashboardPage.tsx, AdminUsersPage.tsx, AdminUserDetailPage.tsx
    ├── AdminWordsPage.tsx, AdminContactsPage.tsx
    ├── AdminFeedbacksPage.tsx, AdminBugReportsPage.tsx
    ├── AdminAIMonitoringPage.tsx, AdminSystemHealthPage.tsx
```

---

## 10. CONTACT/FEEDBACK ARXITEKTURA LOYIHASI (KELAJAK — Sprint 15)

### Backend Tuzilma

```
apps/contact/
├── domain/
│   ├── entities.py          # ContactMessage, Feedback, BugReport dataclasses
│   └── repositories.py      # Abstract repos
├── application/
│   ├── use_cases/
│   │   ├── contact.py       # SendContactUseCase, GetMyContactsUseCase
│   │   ├── feedback.py      # SendFeedbackUseCase, GetMyFeedbacksUseCase
│   │   └── bug_report.py    # SendBugReportUseCase, GetMyBugsUseCase
│   └── services/
│       └── notification_service.py  # Email + admin alert
├── infrastructure/
│   ├── models.py            # ContactMessage, Feedback, BugReport, Attachment
│   └── repositories.py      # Django repos
└── presentation/
    ├── views/
    │   ├── contact.py, feedback.py, bug_report.py
    ├── serializers/
    ├── urls.py
    └── throttles.py         # ContactRateThrottle, FeedbackRateThrottle
```

### Frontend Tuzilma

```
features/contact/
├── api/contactApi.ts
├── components/
│   ├── ContactForm.tsx, FeedbackModal.tsx (floating button → modal)
│   ├── BugReportForm.tsx, MyMessages.tsx, MessageDetail.tsx
├── hooks/
│   ├── useContact.ts, useFeedback.ts, useBugReport.ts
└── pages/
    ├── ContactPage.tsx, MyMessagesPage.tsx
```

---

## 11. MA'LUM ARXITEKTURA MUAMMOLAR (Texnik Qarz)

### 1. Word Model — God Model (30+ field)

- **Holat:** Hozircha ishlaydi, lekin scaling da muammo bo'lishi mumkin
- **Yechim:** Sprint 24 Refactoring da Word → WordCore + WordEnrichment + WordReviewState ga bo'lish
- **Prioritet:** O'rta
- **Sprint:** 24

### 2. AbstractBaseModel — barcha modellarga mos emas

- **Holat:** XPTransaction, ReviewLog, ChatMessage soft-delete (is_active) mantiqsiz — audit trail modellar o'chirilmasligi kerak
- **Yechim:** Audit trail modellar uchun alohida `AbstractAuditModel` (is_active yo'q) yaratish
- **Prioritet:** Past
- **Sprint:** 24

### 3. GameSession — bitta model 7 o'yin uchun

- **Holat:** Ishlaydi, lekin game_type switch/case kerak bo'ladi
- **Yechim:** AbstractGameSession → ConcreteGameSession (har bir o'yin turi uchun)
- **Prioritet:** Past (hozircha ishlaydi)
- **Sprint:** 24+

### 4. Learning modellari noto'g'ri app da

- **Holat:** LearningProfile, MistakePattern, etc. `users/` ichida, lekin `words/` ga yaqinroq
- **Yechim:** Refactoring da alohida `learning/` app yaratish
- **Prioritet:** Past
- **Sprint:** 24+

### 5. DailyStreak alohida UUID — ortiqcha

- **Holat:** DailyStreak alohida model, `UserProgress` ichiga qo'shilishi mumkin
- **Yechim:** UserProgress ga streak fieldlarni ko'chirish yoki hozircha qoldirish
- **Prioritet:** Past
- **Sprint:** 24

### 6. DI pattern hujjatlashtirilmagan

- **Holat:** Dependency Injection `dependencies.py` / `learning_deps.py` fayllarida ishlaydi, lekin pattern rasmiy hujjatlashtirilmagan
- **Yechim:** CONTRIBUTING.md yoki Project DNA ga DI pattern qoidalarini qo'shish
- **Prioritet:** Past
- **Sprint:** 21 (CI/CD)

### 7. Caching strategiyasi yo'q

- **Holat:** Redis mavjud, lekin faqat Celery broker sifatida ishlatiladi. View/query cache yo'q
- **Yechim:** Sprint 33 da to'liq caching strategiya (view-level, query-level, session cache)
- **Prioritet:** O'rta
- **Sprint:** 33

### 8. Idempotency middleware detallari yo'q

- **Holat:** IdempotencyMiddleware mavjud, lekin qaysi endpointlarga ta'sir qilishi hujjatlashtirilmagan
- **Yechim:** Middleware da POST endpoints ro'yxatini aniqlashtirish va hujjatlash
- **Prioritet:** Past
- **Sprint:** 21

### 9. Circuit Breaker faqat AI uchun

- **Holat:** CircuitBreaker faqat AI providerlar uchun ishlaydi
- **Yechim:** External service calls (email, TTS, payment) uchun ham qo'llash
- **Prioritet:** Past
- **Sprint:** 25+

### 10. Service vs Use Case farqi hujjatlashtirilmagan

- **Holat:** Domain services (SpacedRepetitionService, XPService, BadgeService) va Application use cases o'rtasida farq aniqlangan, lekin qoida hujjatlashtirilmagan
- **Yechim:** "Service = reusable logic, UseCase = single action orchestration" qoidasini CONTRIBUTING.md ga qo'shish
- **Prioritet:** Past
- **Sprint:** 21

---

## O'ZGARISHLAR TARIXI

| Sana       | Kim      | Nima o'zgardi                                                                                                |
| ---------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| 2026-02-27 | AI Agent | Dastlabki versiya yaratildi — to'liq arxitektura map                                                         |
| 2026-02-27 | AI Audit | To'liq audit: model 30→31, endpoint ~96→103, use case ~42→87, badge 18→31, route 31→34, Section 11 qo'shildi |
