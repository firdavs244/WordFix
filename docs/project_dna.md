# WordFix — Project DNA

> Bu fayl loyihaning to'liq texnik va biznes identifikatsiyasini tavsiflaydi.
> Yangi developer yoki AI agent uchun "bitta fayl — butun loyiha" maqsadida yaratilgan.
> Oxirgi yangilangan: 2026-02-28

### CHANGELOG (2026-02-27 Audit)

- Narxlar to'liq birlashtirildi — Starter/Pro/Premium → Basic/Pro/Enterprise (UZS-asosli, BS bilan bir xil)
- Badge soni 18 → 31 ga tuzatildi (badge_service.py dan tekshirildi)
- Use Case soni ~42 → 87 ga tuzatildi
- Model soni 30 → 31 ga tuzatildi
- Endpoint soni ~96 → 103 ga tuzatildi
- Frontend Route soni 31 → 34 ga tuzatildi
- AI default model `llama-3.3-70b-versatile` deb aniqlandi (Groq)
- Raqobatchilar SR da'volari tuzatildi (Duolingo Birdbrain, Quizlet Learn mode)
- "Self-hosted/privacy" Anki xususiyatdan o'chirildi
- LoginView rate limiting **yo'qligi** hujjatlashtirildi (xavfsizlik muammo)
- Environment Variables bo'limi qo'shildi (27 ta)
- "Ma'lum Texnik Muammolar" bo'limi qo'shildi
- Free tier limitlari barcha hujjatlarga moslandi

### CHANGELOG (2026-02-28 Monetizatsiya Rewrite)

- **Tier nomlar:** Basic → Starter, Enterprise → Premium (individual), yangi Enterprise = B2B
- **Narxlar:** Free/0 → Starter/29K → Pro/59K → Premium/99K UZS + Enterprise B2B $49-99/oy
- **Yillik rejalar:** Starter 249K, Pro 499K, Premium 849K UZS (~29-30% chegirma)
- **AI Model Selection:** User tanlaydi — 🟢 Basic(Groq) / 🟡 Standard(Gemini) / 🔴 Professional(GPT-4o)
- **Falsafa:** Barcha funksiyalar barchaga ochiq — faqat miqdor farq qiladi
- Section 6 to'liq rewrite (3 sub-section: Individual, Enterprise B2B, AI Model)
- AI Stack (2.3) yangilandi — user-selectable model system

---

## 1. LOYIHA IDENTIFIKATSIYASI

| Atribut     | Qiymat                                                     |
| ----------- | ---------------------------------------------------------- |
| Loyiha nomi | WordFix                                                    |
| Versiya     | 1.0.0 (MVP — Sprint 12.5 tugallangan)                      |
| Turi        | AI-Powered Vocabulary Learning Platform                    |
| Maqsad      | O'zbek foydalanuvchilar uchun ingliz tili lug'at o'rganish |
| Til         | O'zbek (UZ) interfeys, Ingliz (EN) o'rganish kontenti      |
| Developer   | Solo developer (Firdavs)                                   |
| Litsenziya  | Private / Proprietary                                      |
| Repository  | Monorepo: wordfix-backend/ + wordfix-frontend/             |

---

## 2. TEXNIK STACK

### 2.1 Backend Stack

| Texnologiya           | Versiya | Vazifasi                           |
| --------------------- | ------- | ---------------------------------- |
| Python                | 3.12+   | Backend tili                       |
| Django                | 5.x     | Web framework                      |
| Django REST Framework | 3.15    | API framework                      |
| PostgreSQL            | 16      | Asosiy database                    |
| Redis                 | 7       | Cache + Celery broker              |
| Celery                | 5.4     | Async task queue                   |
| Celery Beat           | —       | Periodic tasks (DatabaseScheduler) |
| SimpleJWT             | 5.3     | JWT authentication                 |
| django-allauth        | —       | Social auth (Google OAuth)         |
| drf-spectacular       | —       | OpenAPI schema + Swagger UI        |
| structlog             | —       | Structured logging (JSON)          |
| WhiteNoise            | —       | Static files serving               |
| Pillow                | —       | Image processing (avatars)         |
| gunicorn              | —       | Production WSGI server             |

### 2.2 Frontend Stack

| Texnologiya      | Versiya | Vazifasi                             |
| ---------------- | ------- | ------------------------------------ |
| React            | 19      | UI framework                         |
| TypeScript       | 5.6     | Type-safe JavaScript                 |
| Vite             | 6       | Build tool + dev server              |
| React Router DOM | 7.1     | Client-side routing (34 ta route)    |
| TanStack Query   | 5       | Server state management              |
| Zustand          | 5       | Client state management (3 ta store) |
| Tailwind CSS     | 3.4     | Utility-first CSS                    |
| Framer Motion    | —       | Animatsiyalar                        |
| Radix UI         | —       | Accessible UI primitives             |
| Recharts         | —       | Grafiklar va diagrammalar            |
| Lucide React     | —       | Ikonkalar                            |
| Vitest           | —       | Unit testing                         |

### 2.3 AI Stack

> Foydalanuvchi o'zi AI modelni tanlaydi. Subscription tier qaysi modelga ruxsat berishini belgilaydi.

| Provider      | Model                   | AI Tier         | Subscription kerak | API Key Env Var |
| ------------- | ----------------------- | --------------- | ------------------ | --------------- |
| Groq          | llama-3.3-70b-versatile | 🟢 Basic        | Free+              | GROQ_API_KEY    |
| Google Gemini | gemini-2.0-flash        | 🟡 Standard     | Starter+           | GEMINI_API_KEY  |
| OpenAI        | gpt-4o-mini / gpt-4o    | 🔴 Professional | Pro+               | OPENAI_API_KEY  |
| (Hardcoded)   | FallbackAIProvider      | — (last resort) | —                  | —               |

```
Foydalanuvchi model tanlaydi → Ruxsat tekshiriladi (subscription tier) → API call
    │ (fail bo'lsa)
    ▼
Fallback zanjiri: Tanlangan → Groq → Gemini → OpenAI → FallbackAIProvider (hardcoded)
CircuitBreaker: 3 consecutive fail → provider skip → 60s cooldown
```

### 2.4 Infrastructure

| Texnologiya    | Vazifasi                               |
| -------------- | -------------------------------------- |
| Docker Compose | 7 ta service orkestratsiyasi (dev)     |
| Nginx          | Reverse proxy (production)             |
| GitHub Actions | CI/CD (kelajak — Sprint 21)            |
| Sentry         | Error tracking (kelajak — Sprint 13.5) |

---

## 3. ARXITEKTURA

### 3.1 Backend Arxitektura: Clean Architecture (DDD-lite)

```
presentation/          → Views, Serializers, URLs
    │
    ▼
application/           → Use Cases (87 ta), Services
    │
    ▼
domain/                → Entities (dataclasses), Repository Interfaces
    │
    ▼
infrastructure/        → Django Models (31 ta), Repository Implementations
```

**Qoida:** View → UseCase → Repository. View hech qachon to'g'ridan-to'g'ri Model ga murojaat qilmaydi.

### 3.2 Frontend Arxitektura: Feature-Based

```
src/
├── features/          → 19 ta feature module
│   ├── auth/          → components/, hooks/, pages/, api/
│   ├── words/         → components/, hooks/, pages/, api/
│   ├── review/        → components/, hooks/, pages/, api/
│   ├── games/         → components/, hooks/, pages/, api/
│   ├── chat/          → components/, hooks/, pages/, api/
│   └── ... (14 ta boshqa)
├── stores/            → 3 ta Zustand store (auth, app, review)
├── api/               → Axios instance + interceptors
├── routes/            → 34 ta route (index.tsx)
├── components/        → Shared UI components
├── providers/         → React context providers
├── hooks/             → Shared hooks
├── lib/               → Utility functions
├── types/             → Global TypeScript types
└── styles/            → Global CSS
```

### 3.3 Dependency Injection Pattern

```python
# Backend DI pattern (har bir app da)
# presentation/dependencies.py yoki learning_deps.py

def get_word_crud_use_case():
    repository = DjangoWordRepository()    # infrastructure → domain interface
    xp_service = XPService()               # domain service
    badge_service = BadgeService()          # domain service
    return AddWordUseCase(repository, xp_service, badge_service)  # application

# View da:
class WordListCreateView(APIView):
    def post(self, request):
        use_case = get_word_crud_use_case()   # DI
        result = use_case.execute(data)        # use case
        return Response(result)                # presentation
```

> ⚠️ DI pattern rasmiy hujjatlashtirilmagan. "Service = reusable logic, UseCase = single action orchestration" qoidasi qo'llaniladi.

---

## 4. RAQAMLAR XULOSA (Haqiqiy Kod Bazasidan)

| Metrika                  | Soni | Manba                                                                                             |
| ------------------------ | ---- | ------------------------------------------------------------------------------------------------- |
| Database modellari       | 31   | apps/\*/infrastructure/models/ + common/                                                          |
| Abstract model           | 1    | AbstractBaseModel (common/models.py)                                                              |
| API endpointlari         | 103  | apps/\*/presentation/urls.py + config/urls.py                                                     |
| Use Cases                | 87   | apps/\*/application/use_cases/ + learning_use_cases/                                              |
| Celery Tasks (periodic)  | 5    | apps/\*/management/ + tasks.py                                                                    |
| Celery Tasks (on-demand) | 4    | apps/words/infrastructure/tasks.py                                                                |
| Middleware               | 13   | config/settings/base.py MIDDLEWARE                                                                |
| Frontend features        | 19   | src/features/                                                                                     |
| Frontend routes          | 34   | src/routes/index.tsx                                                                              |
| Zustand stores           | 3    | src/stores/                                                                                       |
| Badges                   | 31   | badge_service.py BADGE_DEFINITIONS                                                                |
| Badge kategoriyalar      | 9    | words, streak, review, test, game, mastery, level, combo, challenge                               |
| O'yin turlari            | 7    | speed_round, word_match, word_context, story_builder, listening, synonym_antonym, irregular_verbs |
| AI Providers             | 3+1  | Groq + Gemini + OpenAI + FallbackAIProvider                                                       |
| Docker services          | 7    | docker-compose.yml                                                                                |
| Environment variables    | 27   | config/settings/ (quyida to'liq ro'yxat)                                                          |

---

## 5. BADGE TIZIMI (31 ta badge, 9 kategoriya)

### 5.1 Badge Kategoriyalar

| Kategoriya | Badges soni | Misollar                                                                                  |
| ---------- | ----------- | ----------------------------------------------------------------------------------------- |
| words      | 5           | first_word, word_collector_10, vocabulary_builder_50, word_master_100, lexicon_expert_500 |
| streak     | 4           | streak_starter_3, streak_warrior_7, streak_champion_30, streak_legend_100                 |
| review     | 3           | first_review, review_enthusiast_50, review_master_200                                     |
| test       | 3           | first_test, test_taker_10, test_expert_50                                                 |
| game       | 3           | first_game, game_lover_25, game_master_100                                                |
| mastery    | 4           | first_mastery, mastery_10, mastery_50, mastery_100                                        |
| level      | 4           | level_5, level_10, level_25, level_50                                                     |
| combo      | 3           | combo_5, combo_10, combo_25                                                               |
| challenge  | 2           | first_challenge, challenge_streak_7                                                       |
| **JAMI**   | **31**      |                                                                                           |

### 5.2 Rarity Taqsimoti

| Rarity    | Soni | XP Reward diapazoni |
| --------- | ---- | ------------------- |
| common    | ~12  | 10-25 XP            |
| rare      | ~10  | 25-75 XP            |
| epic      | ~6   | 50-150 XP           |
| legendary | ~3   | 100-250 XP          |

---

## 6. NARX STRATEGIYASI (Yagona — barcha hujjatlarda bir xil)

> **Falsafa:** "BARCHA funksiyalar barchaga ochiq — faqat MIQDOR farq qiladi." Hech qanday funksiya yopilmaydi.

### 6.1 Individual Rejalar

| Reja        | Oylik narx | USD ekvivalent | Yillik narx | Asosiy cheklovlar                                             |
| ----------- | ---------- | -------------- | ----------- | ------------------------------------------------------------- |
| **Free**    | 0 UZS      | $0             | —           | 30 so'z/kun (150 max), 15 AI chat, 🟢 Basic AI faqat          |
| **Starter** | 29,000 UZS | ~$2.29         | 249,000 UZS | 120 so'z/kun (400 max), 60 AI chat, 🟢+🟡 AI                  |
| **Pro**     | 59,000 UZS | ~$4.66         | 499,000 UZS | 500 so'z/kun (1200 max), cheksiz chat, 🟢🟡🔴 AI (50/kun Pro) |
| **Premium** | 99,000 UZS | ~$7.83         | 849,000 UZS | 1000 so'z/kun (2000 max), hammasi cheksiz, 🟢🟡🔴 AI cheksiz  |

### 6.2 Enterprise (alohida B2B tier)

| Xususiyat    | Tafsilot                           |
| ------------ | ---------------------------------- |
| **Narx**     | $49-99/oy per org (50 users)       |
| **Features** | Barcha Premium + Admin Panel + SSO |
| **Maqsad**   | Ta'lim muassasalari, korporativ    |

### 6.3 AI Model Tanlov Tizimi

| AI Tier         | Model                | Free | Starter | Pro         | Premium    |
| --------------- | -------------------- | ---- | ------- | ----------- | ---------- |
| 🟢 Basic        | Groq (llama-3.3-70b) | ✅   | ✅      | ✅          | ✅         |
| 🟡 Standard     | Gemini 2.0 Flash     | ❌   | ✅      | ✅          | ✅         |
| 🔴 Professional | GPT-4o-mini / GPT-4o | ❌   | ❌      | ✅ (50/kun) | ✅ Cheksiz |

> ⚠️ **Kodda holat:** Hozir subscription modeli yo'q. Faqat `is_premium` boolean + `premium_until` DateTimeField. Feature gating Sprint 16, AI Model Selection Sprint 25 da rejalashtirilgan.

---

## 7. RAQOBATCHILAR SOLISHTIRMASI

| Xususiyat                 | WordFix                | Duolingo      | Quizlet          | Anki         | Memrise          |
| ------------------------- | ---------------------- | ------------- | ---------------- | ------------ | ---------------- |
| **SR algoritmi**          | SM-2 + AI Adaptive     | ⚠️ Birdbrain  | ⚠️ Learn mode SR | ✅ SM-2      | ⚠️ O'z algoritmi |
| **AI boyitish**           | ✅ 3 provider          | ❌            | ❌               | ❌           | ❌               |
| **AI Chat**               | ✅                     | ❌            | ❌               | ❌           | ❌               |
| **O'zbek tili**           | ✅ To'liq              | ⚠️ Cheklangan | ❌               | ⚠️ Community | ❌               |
| **O'yin turlari**         | 7 ta                   | 5-6 ta        | 3-4 ta           | 0 ta         | 2-3 ta           |
| **Badge tizimi**          | 31 ta (4 rarity)       | Bor           | Yo'q             | Yo'q         | Bor              |
| **Smart Import**          | ✅ AI-First            | ❌            | ❌               | ❌           | ❌               |
| **Confusing Pairs**       | ✅ AI                  | ❌            | ❌               | ❌           | ❌               |
| **Learning Profile**      | ✅ Adaptive            | ⚠️            | ❌               | ❌           | ❌               |
| **Narx**                  | Free / $2.29 (Starter) | Free / $7.99  | Free / $7.99     | Free         | Free / $8.49     |
| **Mahalliy to'lov (UZS)** | ✅ Payme/Click         | ❌            | ❌               | —            | ❌               |

> **SR izohlar:** Duolingo o'z "Birdbrain" algoritmini ishlatadi (SM-2/SM-5 emas). Quizlet "Learn mode" da yuzaki SR bor (klassik Leitner emas). Memrise o'z proprietar SR algoritmini ishlatadi. Faqat Anki va WordFix haqiqiy SM-2 implementatsiyaga ega.

---

## 8. USE CASE TAQSIMOTI (87 ta)

### Users App — 18 ta

| Guruh    | Soni | Use Cases                                                                                                                                                                                          |
| -------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Auth     | 3    | Register, Login, GoogleLogin                                                                                                                                                                       |
| Profile  | 6    | GetProfile, UpdateProfile, ChangePassword, GetOnboarding, SubmitOnboarding, SkipOnboarding                                                                                                         |
| Learning | 9    | GetLearningProfile, AnalyzeLearningProfile, GetAdaptiveDifficulty, GetMistakePatterns, RecordMistake, GetWordRecommendations, AcceptRecommendation, UpdateDomainCoverage, RecordSessionPerformance |

### Words App — 69 ta

| Guruh            | Soni | Use Cases                                                               |
| ---------------- | ---- | ----------------------------------------------------------------------- |
| CRUD             | 8    | Add, Get, GetDetail, Update, Delete, BulkAdd, GetStats, Search          |
| Archive          | 4    | Archive, Unarchive, GetArchived, BulkArchive                            |
| Enrichment       | 2    | Enrich, BatchEnrich                                                     |
| Import           | 4    | AnalyzeText, ImportWords, ValidateCSV, CSVImport                        |
| Review           | 5    | GetReviewWords, StartSession, SubmitAnswer, CompleteSession, GetSummary |
| Streak           | 1    | UpdateStreak                                                            |
| Tests            | 5    | GenerateTest, SubmitAnswer, CompleteSession, GetHistory, GetDetail      |
| Games            | 20   | 7 o'yin × (Start+Submit/Answer+Complete) + GetHistory + GetStats        |
| Chat             | 5    | StartChat, SendMessage, EndChat, GetHistory, GetSessionDetail           |
| Confusing Pairs  | 6    | Detect, GetPairs, GetDetail, GenerateDrill, Resolve, GetCount           |
| Daily Challenges | 3    | GetChallenges, UpdateProgress, ClaimBonus                               |
| Analytics        | 6    | Overview, Weekly, Monthly, DifficultWords, WordProgress, Calendar       |

---

## 9. ENVIRONMENT VARIABLES (27 ta)

### 9.1 Django Core (7 ta)

| Variable               | Fayl      | Default                     | Izoh                    |
| ---------------------- | --------- | --------------------------- | ----------------------- |
| SECRET_KEY             | base.py   | (random string)             | Django secret key       |
| DEBUG                  | base.py   | True (dev) / False (prod)   | Debug mode              |
| ALLOWED_HOSTS          | base.py   | localhost,127.0.0.1         | Ruxsat berilgan hostlar |
| CORS_ALLOWED_ORIGINS   | base.py   | http://localhost:5173       | CORS origins            |
| DJANGO_SETTINGS_MODULE | manage.py | config.settings.development | Settings module         |
| STATIC_URL             | base.py   | /static/                    | Static files URL        |
| MEDIA_URL              | base.py   | /media/                     | Media files URL         |

### 9.2 Database (5 ta)

| Variable          | Fayl    | Default  | Izoh              |
| ----------------- | ------- | -------- | ----------------- |
| POSTGRES_DB       | base.py | wordfix  | Database nomi     |
| POSTGRES_USER     | base.py | postgres | Database user     |
| POSTGRES_PASSWORD | base.py | postgres | Database password |
| POSTGRES_HOST     | base.py | db       | Database host     |
| POSTGRES_PORT     | base.py | 5432     | Database port     |

### 9.3 Redis (1 ta)

| Variable  | Fayl    | Default              | Izoh             |
| --------- | ------- | -------------------- | ---------------- |
| REDIS_URL | base.py | redis://redis:6379/0 | Redis connection |

### 9.4 AI Providers (5 ta)

| Variable            | Fayl    | Default                 | Izoh                               |
| ------------------- | ------- | ----------------------- | ---------------------------------- |
| GROQ_API_KEY        | base.py | ""                      | Groq API key (primary)             |
| GEMINI_API_KEY      | base.py | ""                      | Google Gemini API key (fallback 1) |
| OPENAI_API_KEY      | base.py | ""                      | OpenAI API key (fallback 2)        |
| AI_DEFAULT_PROVIDER | base.py | groq                    | Default AI provider                |
| AI_DEFAULT_MODEL    | base.py | llama-3.3-70b-versatile | Default AI model                   |

### 9.5 JWT (4 ta)

| Variable                      | Fayl    | Default    | Izoh                      |
| ----------------------------- | ------- | ---------- | ------------------------- |
| ACCESS_TOKEN_LIFETIME_MINUTES | base.py | 60         | Access token muddati      |
| REFRESH_TOKEN_LIFETIME_DAYS   | base.py | 7          | Refresh token muddati     |
| SIGNING_KEY                   | base.py | SECRET_KEY | JWT signing key           |
| AUTH_HEADER_TYPES             | base.py | Bearer     | Authorization header type |

### 9.6 Celery (2 ta)

| Variable              | Fayl      | Default              | Izoh           |
| --------------------- | --------- | -------------------- | -------------- |
| CELERY_BROKER_URL     | celery.py | redis://redis:6379/0 | Celery broker  |
| CELERY_RESULT_BACKEND | celery.py | redis://redis:6379/0 | Result backend |

### 9.7 Other (3 ta)

| Variable             | Fayl    | Default | Izoh                         |
| -------------------- | ------- | ------- | ---------------------------- |
| GOOGLE_CLIENT_ID     | base.py | ""      | Google OAuth client ID       |
| GOOGLE_CLIENT_SECRET | base.py | ""      | Google OAuth client secret   |
| EMAIL_BACKEND        | base.py | console | Email backend (dev: console) |

---

## 10. XAVFSIZLIK HOLATI

### 10.1 Mavjud Himoyalar

| Himoya                  | Holat | Izoh                                                  |
| ----------------------- | ----- | ----------------------------------------------------- |
| JWT Authentication      | ✅    | SimpleJWT: access (60min) + refresh (7 kun)           |
| CORS middleware         | ✅    | Faqat allowed origins                                 |
| CSRF protection         | ✅    | CsrfViewMiddleware                                    |
| Rate Limiting           | ✅    | Anon: 20/min, User: 60/min, Auth: 5/min, CRUD: 30/min |
| Idempotency             | ✅    | POST duplicate prevention                             |
| Input validation        | ✅    | DRF serializers                                       |
| SQL injection           | ✅    | Django ORM                                            |
| XSS protection          | ✅    | Django SecurityMiddleware                             |
| Clickjacking protection | ✅    | X-Frame-Options middleware                            |
| HTTPS (production)      | ✅    | Nginx + SECURE_SSL_REDIRECT                           |
| Request ID              | ✅    | RequestIDMiddleware (X-Request-ID)                    |

### 10.2 Ma'lum Xavfsizlik Muammolari

| Muammo                                   | Xavflilik  | Holat    | Sprint |
| ---------------------------------------- | ---------- | -------- | ------ |
| LoginView rate limiting yo'q             | **YUQORI** | ⚠️ OCHIQ | 14     |
| JWT refresh rotation yo'q                | O'rta      | ⚠️ OCHIQ | 14     |
| Account lockout yo'q (5x noto'g'ri)      | O'rta      | ⚠️ OCHIQ | 14     |
| Password policy enforcement yo'q         | O'rta      | ⚠️ OCHIQ | 14     |
| Security headers (CSP, HSTS) to'liq emas | Past       | ⚠️ OCHIQ | 14     |
| Account deletion funksiyasi yo'q         | O'rta      | ⚠️ OCHIQ | 14     |

> ⚠️ **KRITIK:** `LoginView` da `throttle_classes` hech qanday ko'rsatilmagan. `AuthRateThrottle` class mavjud (rate_limiter.py), lekin LoginView ga **ulanmagan**. Brute-force hujum mumkin. Sprint 14 da BIRINCHI navbatda tuzatilishi kerak.

---

## 11. MA'LUM TEXNIK MUAMMOLAR (16 ta)

### Arxitektura Muammolari

| #   | Muammo                                          | Prioritet | Sprint | Izoh                                                   |
| --- | ----------------------------------------------- | --------- | ------ | ------------------------------------------------------ |
| 1   | Word model — God Model (30+ field)              | O'rta     | 24     | WordCore + WordEnrichment + WordReviewState ga bo'lish |
| 2   | AbstractBaseModel — audit modellarida noto'g'ri | Past      | 24     | XPTransaction, ChatMessage soft-delete mantiqsiz       |
| 3   | GameSession — 1 model 7 o'yin uchun             | Past      | 24+    | Hozircha ishlaydi, lekin game_type switch kerak        |
| 4   | Learning modellari noto'g'ri app da             | Past      | 24+    | users/ dan alohida learning/ app ga ko'chirish         |
| 5   | DailyStreak alohida UUID — ortiqcha             | Past      | 24     | UserProgress ga streak fieldlarni ko'chirish mumkin    |

### Pattern va Hujjat Muammolari

| #   | Muammo                                                             | Prioritet | Sprint | Izoh                                          |
| --- | ------------------------------------------------------------------ | --------- | ------ | --------------------------------------------- |
| 6   | DI pattern hujjatlashtirilmagan                                    | Past      | 21     | CONTRIBUTING.md ga qoidalar qo'shish          |
| 7   | Service vs UseCase farqi hujjatlashtirilmagan                      | Past      | 21     | "Service = reusable, UseCase = orchestration" |
| 8   | Idempotency middleware qaysi endpointlarga ta'sir qilishi noma'lum | Past      | 21     | Hujjatlash kerak                              |

### Infra Muammolari

| #   | Muammo                                           | Prioritet | Sprint | Izoh                                           |
| --- | ------------------------------------------------ | --------- | ------ | ---------------------------------------------- |
| 9   | Caching strategiyasi yo'q                        | O'rta     | 33     | Redis faqat Celery broker sifatida ishlatiladi |
| 10  | Circuit Breaker faqat AI uchun                   | Past      | 25+    | Email, TTS, payment uchun ham kerak            |
| 11  | RequestIDMiddleware #10 → #2 ga ko'chirish kerak | O'rta     | 14     | Auth xatolari request ID siz loglanadi         |
| 12  | Error monitoring (Sentry) yo'q                   | Yuqori    | 13.5   | Production da xatolar ko'rinmaydi              |
| 13  | Backup strategiyasi yo'q                         | Yuqori    | 14     | PostgreSQL dump + Redis snapshot kerak         |

### Testing Muammolari

| #   | Muammo                         | Prioritet | Sprint | Izoh                                     |
| --- | ------------------------------ | --------- | ------ | ---------------------------------------- |
| 14  | Integration test coverage past | O'rta     | 21     | CI/CD pipeline da test coverage qo'shish |
| 15  | Frontend E2E testlar yo'q      | O'rta     | 21     | Playwright/Cypress qo'shish kerak        |
| 16  | Load testing yo'q              | Past      | 25     | k6/Locust bilan stress test              |

---

## 12. GAMIFICATION TIZIMI

### 12.1 XP Tizimi

| Harakat          | XP      | Izoh                           |
| ---------------- | ------- | ------------------------------ |
| So'z qo'shish    | +5      | word_added                     |
| Review to'g'ri   | +10     | review_correct                 |
| Review noto'g'ri | +2      | review_incorrect (consolation) |
| Test tugallash   | +20-50  | score asosida                  |
| O'yin tugallash  | +15-40  | score asosida                  |
| Badge olish      | +10-250 | rarity asosida                 |
| Daily challenge  | +25-100 | challenge turi asosida         |
| Chat sessiya     | +10     | chat_complete                  |
| So'z mastered    | +25     | word_mastered                  |

### 12.2 Combo Tizimi

| Combo | Bonus XP | Trigger                |
| ----- | -------- | ---------------------- |
| 5x    | +5       | 5 ta ketma-ket to'g'ri |
| 10x   | +12      | 10 ta ketma-ket        |
| 15x   | +20      | 15 ta ketma-ket        |
| 20x   | +30      | 20 ta ketma-ket        |
| 25x+  | +50      | 25+ ta ketma-ket       |

### 12.3 Level Tizimi

```
Level = floor(total_xp / 100)
Level 1:   0 XP
Level 5:   500 XP    → Badge: level_5
Level 10:  1,000 XP  → Badge: level_10
Level 25:  2,500 XP  → Badge: level_25
Level 50:  5,000 XP  → Badge: level_50
```

---

## 13. AI INTEGRATION DETAIL

### 13.1 AI Provider Factory

```python
# core/services/ai/ai_factory.py
AIProviderFactory.get_provider(provider_type="groq")  # yoki "gemini", "openai"

# Fallback logikasi:
# 1. Tanlangan provider → call
# 2. Fail → CircuitBreaker → keyingi provider
# 3. Barcha fail → FallbackAIProvider (hardcoded javoblar)
```

### 13.2 AI ishlatilgan joylar

| Feature          | AI Call                               | Provider | Nima uchun                           |
| ---------------- | ------------------------------------- | -------- | ------------------------------------ |
| Word Enrichment  | enrich_word prompt                    | Any      | definition, synonyms, antonyms, etc. |
| Smart Import     | 2x call (extract + validate)          | Any      | Matn → so'zlar + tarjima + CEFR      |
| Test Generation  | generate_test prompt                  | Any      | Multiple choice/fill-blank AI        |
| Word Context     | context story generation              | Any      | O'yin uchun kontekst hikoya          |
| Story Builder    | story continuation + grammar check    | Any      | AI hikoya davomi + tuzatish          |
| Chat             | chat message + grammar correction     | Any      | Suhbat + grammatika tuzatish         |
| Confusing Pairs  | drill generation                      | Any      | Chalkash so'zlar mashqi              |
| Learning Profile | profile analysis                      | Any      | O'rganish profili tahlili            |
| Distractors      | distractor generation (async, Celery) | Any      | Test uchun noto'g'ri javoblar        |

### 13.3 Circuit Breaker Sozlamalari

```python
# apps/common/circuit_breaker.py
FAILURE_THRESHOLD = 3    # 3 ta ketma-ket xato → circuit open
RECOVERY_TIMEOUT = 60    # 60 soniya kutish → half-open state
SUCCESS_THRESHOLD = 1    # 1 ta muvaffaqiyat → circuit closed
```

---

## 14. DEVELOPMENT QOIDALARI

### 14.1 Kod Yozish Qoidalari

| Qoida                              | Izoh                                               |
| ---------------------------------- | -------------------------------------------------- |
| Clean Architecture saqlansin       | View → UseCase → Repository, hech qachon shortcut  |
| Har bir UseCase — bitta fayl emas  | Bitta fayl ichida tegishli use caselar guruhlangan |
| Type hints majburiy (backend)      | Barcha funksiyalar type hint bilan                 |
| TypeScript strict mode (frontend)  | tsconfig.json strict: true                         |
| Har bir feature — alohida papka    | features/word/, features/review/, etc.             |
| API response format standart       | {success, data, message, errors, meta}             |
| Error handling — custom exceptions | apps/common/exceptions.py orqali                   |

### 14.2 Git Qoidalari

```
Branch naming:  feature/sprint-XX-feature-name
                bugfix/issue-description
                hotfix/critical-fix

Commit format:  [Sprint XX] feat: description
                [Sprint XX] fix: description
                [Sprint XX] refactor: description
```

### 14.3 Testing Qoidalari

| Qoida                         | Izoh                                      |
| ----------------------------- | ----------------------------------------- |
| Backend: pytest + factory_boy | TestCase → UseCase test + API test        |
| Frontend: Vitest + RTL        | Component test + hook test                |
| Coverage maqsad: 70%+         | Sprint 21 da CI/CD bilan enforce qilinadi |
| E2E: Playwright (kelajak)     | Sprint 21 da qo'shiladi                   |

---

## 15. DEPLOYMENT

### 15.1 Development

```bash
# Backend
cd wordfix-backend
docker-compose up -d                    # 7 ta service
python manage.py migrate                # Migratsiyalar
python manage.py createsuperuser        # Admin user
python manage.py seed_badges            # 31 ta badge seed

# Frontend
cd wordfix-frontend
npm install
npm run dev                             # Vite dev server :5173
```

### 15.2 Production

```bash
# Docker Compose (production)
docker-compose -f docker-compose.prod.yml up -d

# Nginx reverse proxy
# / → frontend static files
# /api/, /admin/ → gunicorn:8000
```

### 15.3 Production Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY o'zgartirilgan
- [ ] ALLOWED_HOSTS to'g'ri
- [ ] CORS_ALLOWED_ORIGINS production domain
- [ ] HTTPS enforce (SECURE_SSL_REDIRECT)
- [ ] Database password kuchli
- [ ] AI API keys .env da (gitignored)
- [ ] collectstatic bajarilgan
- [ ] migrate bajarilgan
- [ ] seed_badges bajarilgan
- [ ] Celery worker + beat ishlayapti
- [ ] Redis maxmemory sozlangan
- [ ] PostgreSQL backup cron job
- [ ] Nginx rate limiting sozlangan
- [ ] Error monitoring (Sentry) ulangan (Sprint 13.5)

---

## O'ZGARISHLAR TARIXI

| Sana       | Kim      | Nima o'zgardi                                                                                                                                                                                             |
| ---------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-27 | AI Agent | Dastlabki versiya yaratildi                                                                                                                                                                               |
| 2026-02-27 | AI Audit | Narxlar birlashtirildi, badge 18→31, use case ~42→87, model 30→31, endpoint ~96→103, route 31→34, LoginView xavfsizlik muammosi hujjatlashtirildi, env vars qo'shildi, texnik muammolar bo'limi qo'shildi |
| 2026-02-28 | AI Agent | Monetizatsiya rewrite: tier nomlar (Starter/Pro/Premium), AI Model Selection, saxiy free tier, yillik rejalar, Enterprise B2B, Section 6 + AI Stack 2.3 yangilandi                                        |
