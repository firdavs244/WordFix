# WordFix — Sprint Roadmap

> Bu fayl loyihaning sprint rejasini batafsil tavsiflaydi.
> Har sprint tugagandan so'ng yangilanadi.
> Oxirgi yangilangan: 2026-02-27

### CHANGELOG (2026-02-27 Audit)

- Endpoint soni ~96 → 103 ga tuzatildi
- Model soni 30 → 31 ga tuzatildi
- Frontend route soni 31 → 34 ga tuzatildi
- Use Case soni ~42 → 87 ga tuzatildi
- Sprint 12.3 (Skip Onboarding) natijasi hujjatlashtirildi
- Sprint 13.5 (Emergency Monitoring — Sentry) qo'shildi
- Sprint 14 kengaytirildi: +6 xavfsizlik vazifasi, muddat 5→7-8 kun
- Sprint 14 ga backup strategiya qo'shildi
- i18n sprint muddati 5→8-10 kun ga tuzatildi
- PWA sprint muddati 5→8-10 kun ga tuzatildi
- Mobile sprint 15-20→35-45 kun + sub-sprintlar
- Sprint Dependencies diagramma qo'shildi
- Buffer/stabilization sprintlar qo'shildi (18.5, 24.5, 29.5)
- Feature Gating Sprint 30 → Sprint 16 ga ko'chirildi
- Rollback strategiya bo'limi qo'shildi
- UX vazifalar tegishli sprintlarga qo'shildi
- KPI va metriklar bo'limi yangilandi
- Narxlar BS bilan birlashtirildi (Free/Basic/Pro/Enterprise — UZS)

---

## UMUMIY KO'RINISH

### Tugallangan Sprintlar (1-12.5)

| Sprint | Nomi                      | Natija                                              | Holat         |
| ------ | ------------------------- | --------------------------------------------------- | ------------- |
| 1      | Project Setup             | Django + React + Docker + PostgreSQL + Redis        | ✅ Tugallandi |
| 2      | Auth System               | Register + Login + JWT + Google OAuth               | ✅ Tugallandi |
| 3      | Word CRUD                 | So'z CRUD + Categories + Bulk add                   | ✅ Tugallandi |
| 4      | AI Enrichment             | 3 provider fallback + Circuit Breaker + Celery      | ✅ Tugallandi |
| 5      | Review System             | SM-2 + Sessions + Combo + Streak                    | ✅ Tugallandi |
| 6      | Tests                     | 4 test turi + AI generatsiya + scoring              | ✅ Tugallandi |
| 7      | Dashboard + Analytics     | Dashboard widgets + Weekly/Monthly stats + Calendar | ✅ Tugallandi |
| 8      | Games (Part 1)            | Speed Round + Word Match + Word Context             | ✅ Tugallandi |
| 9      | Games (Part 2)            | Story Builder + Listening Challenge                 | ✅ Tugallandi |
| 10     | XP + Badge + Gamification | 31 badge + XP + Level + Combo + Notification        | ✅ Tugallandi |
| 11     | Onboarding + Profile      | Assessment + CEFR level + Profile management        | ✅ Tugallandi |
| 12.1   | AI Chat                   | Context-aware chat + Grammar correction             | ✅ Tugallandi |
| 12.2   | Confusing Pairs           | Auto-detect + AI Drill + Resolve                    | ✅ Tugallandi |
| 12.3   | Skip Onboarding           | OnboardingSkipView + SkipOnboardingUseCase          | ✅ Tugallandi |
| 12.4   | Smart Import              | AI-First pipeline + CSV import + validation         | ✅ Tugallandi |
| 12.5   | Games (Part 3)            | Synonym-Antonym + Irregular Verbs + Game Stats      | ✅ Tugallandi |

### Hozirgi Raqamlar (Sprint 12.5 tugashi)

| Metrika            | Soni |
| ------------------ | ---- |
| Database modellari | 31   |
| API endpointlari   | 103  |
| Use Cases          | 87   |
| Frontend routes    | 34   |
| Frontend features  | 19   |
| Badges             | 31   |
| O'yin turlari      | 7    |

---

## SPRINT DEPENDENCIES DIAGRAMMA

```
Sprint 13 (Daily Challenges) ─────────────────────────────────────┐
Sprint 13.5 (Sentry/Monitoring) ─────────────────────────────┐    │
Sprint 14 (Security) ──────────┐                              │    │
Sprint 15 (Contact/Feedback) ──┤                              │    │
Sprint 16 (Feature Gating) ────┤                              │    │
                                ▼                              │    │
Sprint 16-17 (Admin Panel) ────────────────────────────┐      │    │
                                                        ▼      ▼    ▼
Sprint 18.5 (Buffer/Stabilization) ───── MILESTONE 1: Production-Ready MVP
                                                        │
Sprint 19-20 (Archive + Learning Profile) ──────────────┤
Sprint 21 (CI/CD + Testing) ────────────────────────────┤
Sprint 22 (i18n) ──────────────────────────────────────┤
Sprint 23 (PWA + Offline) ─────────────────────────────┤
                                                        ▼
Sprint 24.5 (Buffer/Stabilization) ───── MILESTONE 2: Multi-language PWA
                                                        │
Sprint 25 (Payment) ───────────────────────────────────┤
Sprint 26 (Advanced Features) ─────────────────────────┤
Sprint 27 (Leaderboard + Social) ──────────────────────┤
Sprint 28-29 (Mobile App) ─────────────────────────────┤
                                                        ▼
Sprint 29.5 (Buffer/Stabilization) ───── MILESTONE 3: Mobile + Monetization
                                                        │
Sprint 30-35 (Growth Features) ────────────────────────┤
                                                        ▼
Sprint 36 ──────────────────────────────── MILESTONE 4: Full Platform
```

---

## KELAJAK SPRINTLAR

### Sprint 13: Daily Challenges Kengaytirish (3-4 kun)

**Maqsad:** Mavjud Daily Challenges tizimini kengaytirish

**Backend (2 kun):**

- [ ] Challenge turlari kengaytirish (review, test, game, import, chat)
- [ ] Challenge difficulty scaling (CEFR asosida)
- [ ] Weekly challenge streak + bonus
- [ ] Challenge notification (Celery Beat)

**Frontend (1-2 kun):**

- [ ] Challenge widget redesign (Dashboard da)
- [ ] Challenge progress bar animatsiya (Framer Motion)
- [ ] Challenge completion celebration UI

**UX vazifa:** Dashboard da challenge widget joylanishini optimizatsiya qilish

---

### Sprint 13.5: Emergency Monitoring (2-3 kun) ⚠️ YANGI

**Maqsad:** Production xatolarini kuzatish tizimi

**Sabab:** Hozir backend xatolari faqat `logs/` papkaga yoziladi. Production da real-time xato kuzatish **yo'q**.

**Backend (1-2 kun):**

- [ ] Sentry SDK integratsiya (sentry-sdk[django])
- [ ] Environment-based DSN configuration
- [ ] Custom error context (user_id, request_id, sprint_version)
- [ ] Performance monitoring (transaction sampling)
- [ ] Celery task error tracking

**Frontend (1 kun):**

- [ ] Sentry React SDK integratsiya
- [ ] Error boundary + Sentry reporting
- [ ] Source map upload (Vite plugin)

**Natija:** 2 ta yangi env variable: `SENTRY_DSN_BACKEND`, `SENTRY_DSN_FRONTEND`

---

### Sprint 14: Security Hardening (7-8 kun) ⚠️ KENGAYTIRILDI

**Maqsad:** Barcha ma'lum xavfsizlik muammolarni tuzatish + backup

**Kritik xavfsizlik vazifalari (3 kun):**

- [ ] **[P0] LoginView rate limiting** — AuthRateThrottle qo'shish (`throttle_classes = [AuthRateThrottle]`)
- [ ] **[P0] Account lockout** — 5x noto'g'ri parol → 15 min qulflash
- [ ] **[P1] JWT refresh rotation** — ROTATE_REFRESH_TOKENS = True
- [ ] **[P1] Password policy** — minimum 8 char, 1 upper, 1 digit, 1 special
- [ ] **[P1] Account deletion** — GDPR-like: user ma'lumotlarini to'liq o'chirish
- [ ] **[P1] Security headers** — CSP, HSTS, X-Content-Type-Options, Referrer-Policy

**Middleware tuzatish (0.5 kun):**

- [ ] RequestIDMiddleware ni #10 → #2 ga ko'chirish (SecurityMiddleware dan keyin)
- [ ] Barcha request/response loglarini X-Request-ID bilan ta'minlash

**Backup strategiyasi (1 kun):**

- [ ] PostgreSQL automated backup script (pg_dump, kundalik)
- [ ] Redis RDB snapshot sozlash
- [ ] Backup to external storage (S3/Backblaze/local)
- [ ] Backup restore test skripti
- [ ] docker-compose.yml ga backup service qo'shish

**Testing (1-2 kun):**

- [ ] Brute-force himoya testi
- [ ] JWT expiry testi
- [ ] Account lockout testi
- [ ] Security header testi
- [ ] Backup/restore testi

**Frontend (1 kun):**

- [ ] Password strength indicator (ChangePassword, Register)
- [ ] Account deletion confirmation modal
- [ ] "Session expired" toast + auto-redirect

**UX vazifalari:**

- [ ] Login form da "Parol unutdingizmi?" link (placeholder, Sprint 25+ da to'liq)
- [ ] Error message da request ID ko'rsatish (debug uchun)

> **Eslatma:** Bu sprint original 5 kundan 7-8 kunga cho'zildi chunki:
>
> - LoginView rate limiting (P0) — hujum mumkin
> - Account deletion — GDPR talabi
> - Backup — production uchun majburiy
> - RequestIDMiddleware ko'chirish — logging uchun zarur

---

### Sprint 15: Contact & Feedback System (5-6 kun)

**Maqsad:** Foydalanuvchi aloqa tizimi (Contact, Feedback, Bug Report)

**Backend (3 kun):**

```
apps/contact/
├── domain/entities.py          # ContactMessage, Feedback, BugReport
├── application/use_cases/
│   ├── contact.py              # SendContact, GetMyContacts
│   ├── feedback.py             # SendFeedback, GetMyFeedbacks
│   └── bug_report.py           # SendBugReport, GetMyBugs
├── infrastructure/models.py    # 4 model: Contact, Feedback, BugReport, Attachment
└── presentation/
    ├── views/, serializers/, urls.py
    └── throttles.py            # ContactRateThrottle, FeedbackRateThrottle
```

**Yangi modellar:** ContactMessage, Feedback, BugReport, Attachment (4 ta → model jami 35 ga oshadi)

**Yangi endpointlar:** ~8-10 ta → endpoint jami ~113 ga oshadi

**Frontend (2-3 kun):**

```
features/contact/
├── components/ContactForm.tsx, FeedbackModal.tsx, BugReportForm.tsx
├── hooks/useContact.ts, useFeedback.ts
└── pages/ContactPage.tsx, MyMessagesPage.tsx
```

**UX vazifalari:**

- [ ] FeedbackModal — floating action button → modal (har qanday sahifadan)
- [ ] Bug report da screenshot attachment qo'shish imkoniyati
- [ ] "Xabar yuborildi!" success toast

---

### Sprint 16: Feature Gating (3-4 kun) ⚠️ YANGI — ko'chirildi Sprint 30 dan

**Maqsad:** Free/Basic/Pro/Enterprise limitlarni implement qilish

**Sabab:** Feature gating Sprint 30 ga rejalashtirilgan edi, lekin Admin Panel (Sprint 16-17) dan OLDIN bo'lishi mantiqiy. Admin panelda foydalanuvchi rejasini boshqarish kerak.

**Backend (2 kun):**

- [ ] Feature Gating middleware yoki decorator yaratish
- [ ] Plan-based permission checks (DRF permissions)
- [ ] Usage tracking (kundalik limit hisobi)
- [ ] Limit configuration (settings yoki database)

```python
# Misol:
class PremiumRequiredPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_premium_active

class RateLimitedFeature:
    LIMITS = {
        'free': {'words': 50, 'reviews_per_day': 5, 'tests_per_day': 1},
        'basic': {'words': 500, 'reviews_per_day': -1, 'tests_per_day': 3},
        'pro': {'words': -1, 'reviews_per_day': -1, 'tests_per_day': -1},
        'enterprise': {'words': -1, 'reviews_per_day': -1, 'tests_per_day': -1},
    }
```

**Frontend (1-2 kun):**

- [ ] Upgrade prompt component (limit reached → "Upgrade to Basic")
- [ ] Feature lock UI (grayed out + lock icon)
- [ ] Plan badge (Header da: "Free", "Basic", "Pro", "Enterprise")

**Limitlar (narxlar Business Strategy bilan bir xil):**

| Xususiyat    | Free | Basic (29K UZS) | Pro (59K UZS) | Enterprise (149K UZS) |
| ------------ | ---- | --------------- | ------------- | --------------------- |
| So'zlar      | 50   | 500             | Cheksiz       | Cheksiz               |
| Review / kun | 5    | Cheksiz         | Cheksiz       | Cheksiz               |
| Test / kun   | 1    | 3               | Cheksiz       | Cheksiz               |
| AI Chat      | ❌   | 3 / kun         | Cheksiz       | Cheksiz               |
| Smart Import | ❌   | 3 / kun         | Cheksiz       | Cheksiz               |
| CSV Import   | ❌   | ❌              | ✅            | ✅                    |

---

### Sprint 16-17: Admin Panel (10-12 kun)

> ℹ️ Sprint raqami 13-14 dan 16-17 ga o'zgardi (Security va Contact sprintlari qo'shilganligi sababli)

**Sprint 16 — Backend (5-6 kun):**

```
apps/admin_panel/
├── domain/
│   ├── entities.py          # AdminRole, AuditLogEntry
│   └── repositories.py      # Abstract repos
├── application/use_cases/
│   ├── dashboard.py         # GetDashboardStats, GetDashboardCharts
│   ├── user_management.py   # ListUsers, BanUser, ChangeUserPlan
│   ├── word_moderation.py   # ListAllWords, FlagWord, DeleteWord
│   ├── ai_monitoring.py     # GetAIStats, SwitchProvider
│   └── system_health.py     # GetSystemHealth
├── infrastructure/
│   ├── models.py            # AdminRole, AdminPermission, AuditLog
│   └── repositories.py
└── presentation/
    ├── views/, serializers/, urls.py
    └── permissions.py       # IsAdmin, IsModerator, IsSupport, IsAnalyst
```

**Yangi endpointlar:** ~15-20 ta (admin namespace)

**Sprint 17 — Frontend (5-6 kun):**

```
features/admin/
├── api/adminApi.ts
├── components/ (AdminLayout, AdminSidebar, DashboardStats, UserTable, ...)
├── hooks/ (useAdminDashboard, useAdminUsers, useAdminContacts)
└── pages/ (AdminDashboard, AdminUsers, AdminUserDetail, AdminWords,
            AdminContacts, AdminFeedbacks, AdminBugReports,
            AdminAIMonitoring, AdminSystemHealth)
```

**Yangi routelar:** ~8-10 ta (/admin/\*)

---

### Sprint 18.5: Buffer & Stabilization (3-4 kun) ⚠️ YANGI

**Maqsad:** MILESTONE 1 — Production-Ready MVP tayyorlash

**Vazifalari:**

- [ ] Barcha Sprint 13-17 bugfixlar
- [ ] Performance profiling (Django Debug Toolbar review)
- [ ] Database index optimization (EXPLAIN ANALYZE)
- [ ] API response time audit (target: p95 < 500ms)
- [ ] Frontend bundle size audit (target: < 500KB gzipped)
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsiveness audit
- [ ] Documentation update (barcha 4 doc)
- [ ] Smoke test checklist yaratish

**Milestone 1 Checklist:**

- [ ] LoginView rate limited ✅
- [ ] Backup ishlayapti ✅
- [ ] Sentry ulangan ✅
- [ ] Security headers to'liq ✅
- [ ] Admin panel ishlayapti ✅
- [ ] Feature gating ishlayapti ✅
- [ ] Contact/Feedback ishlayapti ✅

---

### Sprint 19: Word Archive Feature Kengaytirish (3-4 kun)

**Maqsad:** Archive funksionalligini kengaytirish

**Backend (2 kun):**

- [ ] Archive filters (date range, category, mastered status)
- [ ] Bulk unarchive
- [ ] Archive auto-cleanup (6 oy eski → permanent delete option)
- [ ] Archive export (CSV)

**Frontend (1-2 kun):**

- [ ] Archive page redesign (filters, search, bulk select)
- [ ] Archive/Unarchive animatsiya
- [ ] "X ta so'z arxivlandi" toast bilan undo option

---

### Sprint 20: Learning Profile Advanced (4-5 kun)

**Maqsad:** Learning Profile tizimini kengaytirish

**Backend (2-3 kun):**

- [ ] Haftalik o'rganish tahlili (Celery periodic task)
- [ ] Study pattern optimization (eng yaxshi vaqt, eng yaxshi tur)
- [ ] Adaptive quiz difficulty (Learning Profile asosida)
- [ ] Mistake pattern insights (AI tahlil)

**Frontend (2 kun):**

- [ ] Learning Profile page redesign
- [ ] Study schedule visualization (heatmap)
- [ ] Mistake pattern chart
- [ ] Adaptive difficulty indicator (har bir feature da)

---

### Sprint 21: CI/CD + Testing (5-6 kun)

**Maqsad:** Automated testing va deployment pipeline

**CI/CD (2-3 kun):**

- [ ] GitHub Actions workflow (lint + test + build + deploy)
- [ ] Backend: pytest + coverage (minimum 70%)
- [ ] Frontend: vitest + coverage (minimum 60%)
- [ ] Docker image build + push
- [ ] Auto-deploy to staging (PR merge)
- [ ] Auto-deploy to production (release tag)

**Testing (2-3 kun):**

- [ ] Backend integration test yakunlash (API endpoint tests)
- [ ] Frontend E2E tests (Playwright) — critical path
- [ ] Contract testing (API schema validation)
- [ ] CONTRIBUTING.md yaratish (DI pattern, Service vs UseCase qoidasi, etc.)
- [ ] Idempotency middleware hujjatlash

---

### Sprint 22: Internationalization — i18n (8-10 kun) ⚠️ TUZATILDI: 5→8-10 kun

**Maqsad:** Ko'p tilli qo'llab-quvvatlash

> **Sabab (muddat oshganligi):** i18n faqat "string o'zgartirish" emas. 19 ta feature module, 200+ component, backend error messages, API responses, email templates — barchasiga tegish kerak. 5 kun yetarsiz.

**Backend (3-4 kun):**

- [ ] django.utils.translation integratsiya
- [ ] API response messages i18n (errors, success, validation)
- [ ] Database content i18n (challenge texts, badge descriptions)
- [ ] Locale middleware
- [ ] gettext .po files (uz, ru, en)

**Frontend (5-6 kun):**

- [ ] i18next + react-i18next setup
- [ ] Barcha 19 feature module da string extraction
- [ ] Language switcher component (Header da)
- [ ] RTL support check (kelajakda Arab tili uchun)
- [ ] Date/number format localization (Intl API)
- [ ] Translation files: uz.json, ru.json, en.json

**Qo'llab-quvvatlanadigan tillar (bosqichma-bosqich):**

1. 🇺🇿 O'zbek (default) — Sprint 22
2. 🇷🇺 Rus — Sprint 22
3. 🇬🇧 Ingliz — Sprint 22
4. 🇰🇿 Qozoq — Sprint 26+

---

### Sprint 23: PWA + Offline Mode (8-10 kun) ⚠️ TUZATILDI: 5→8-10 kun

**Maqsad:** Progressive Web App + asosiy offline funksionallik

> **Sabab (muddat oshganligi):** PWA faqat manifest.json emas. Service Worker, offline cache strategiya, sync queue, IndexedDB, push notification — barchasi kerak. 5 kun yetarsiz.

**Service Worker (3-4 kun):**

- [ ] Vite PWA plugin setup (vite-plugin-pwa)
- [ ] Cache strategiya: Stale-While-Revalidate (API) + Cache-First (static)
- [ ] Offline fallback page
- [ ] Background sync queue (review, test answers)
- [ ] Cache invalidation strategiya

**IndexedDB (2-3 kun):**

- [ ] Dexie.js setup (IndexedDB wrapper)
- [ ] Offline word storage (foydalanuvchi so'zlari cache)
- [ ] Offline review sessiya (sync later)
- [ ] Conflict resolution (online/offline merge)

**Push Notification (1-2 kun):**

- [ ] Web Push API integratsiya
- [ ] Notification permission UX
- [ ] Push topics: review_reminder, streak_warning, badge_earned, daily_challenge

**PWA Infrastructure (1 kun):**

- [ ] manifest.json (icons, theme, shortcuts)
- [ ] App install banner
- [ ] Splash screen

**Testing (1 kun):**

- [ ] Offline mode testing
- [ ] Sync testing
- [ ] Lighthouse PWA audit (target: 90+ score)

---

### Sprint 24: Refactoring (5-7 kun)

**Maqsad:** Texnik qarzni kamaytirish

**Backend Refactoring:**

- [ ] Word model split: Word → WordCore + WordEnrichment + WordReviewState
- [ ] AbstractAuditModel yaratish (XPTransaction, ReviewLog, ChatMessage uchun)
- [ ] DailyStreak → UserProgress ga birlashtirish (optional)
- [ ] Database migration yaratish va test qilish
- [ ] Backward compatibility ta'minlash (API response o'zgarmaydi)

**Documentation:**

- [ ] Barcha 4 doc yangilash (yangi model soni, yangi structure)
- [ ] CONTRIBUTING.md yakunlash
- [ ] API documentation yangilash (drf-spectacular)

---

### Sprint 24.5: Buffer & Stabilization (3-4 kun) ⚠️ YANGI

**Maqsad:** MILESTONE 2 — Multi-language PWA

**Vazifalari:**

- [ ] Sprint 19-24 bugfixlar
- [ ] i18n QA (barcha tillar visual tekshiruv)
- [ ] PWA offline scenario testing
- [ ] Performance regression check
- [ ] Bundle size re-audit
- [ ] Documentation update

---

### Sprint 25: Payment Integration (7-8 kun)

**Maqsad:** To'lov tizimi va subscription management

**Backend (4-5 kun):**

```
apps/payments/
├── domain/entities.py          # Subscription, Payment, Invoice
├── application/use_cases/
│   ├── subscribe.py            # CreateSubscription, CancelSubscription
│   ├── payment.py              # ProcessPayment, RefundPayment
│   └── invoice.py              # GenerateInvoice, GetPaymentHistory
├── infrastructure/
│   ├── models.py               # Subscription, Payment, Invoice, PaymentMethod
│   ├── providers/
│   │   ├── payme.py            # Payme integration
│   │   └── click.py            # Click integration
│   └── repositories.py
└── presentation/
    ├── views/, serializers/, urls.py
    └── webhooks.py             # Payme/Click webhook handlers
```

**Frontend (2-3 kun):**

- [ ] Pricing page
- [ ] Checkout flow (plan select → payment → confirmation)
- [ ] Subscription management page (upgrade, downgrade, cancel)
- [ ] Payment history page

**Narxlar (BS bilan bir xil):**

- Free: 0 UZS
- Basic: 29,000 UZS/oy (~$2.29)
- Pro: 59,000 UZS/oy (~$4.66)
- Enterprise: 149,000 UZS/oy (~$11.79)

---

### Sprint 26: Advanced Features (5-6 kun)

**Maqsad:** Qo'shimcha xususiyatlar

- [ ] Word of the Day (Celery daily task)
- [ ] Vocabulary themes / curated lists (travel, business, IELTS, etc.)
- [ ] Enhanced Analytics (word cloud, difficulty heatmap, study trends)
- [ ] Export data (CSV, PDF report)
- [ ] Qozoq tili qo'shish (i18n extension)

---

### Sprint 27: Leaderboard + Social (5-6 kun)

**Maqsad:** Ijtimoiy xususiyatlar va reyting

**Backend:**

```
apps/social/
├── domain/entities.py          # LeaderboardEntry, Friend, Achievement
├── application/use_cases/
│   ├── leaderboard.py          # GetWeeklyLeaderboard, GetMonthlyLeaderboard
│   └── friends.py              # SendFriendRequest, AcceptFriend, GetFriendProgress
├── infrastructure/models.py    # Leaderboard, Friendship, SharedAchievement
└── presentation/
```

**Frontend:**

- [ ] Leaderboard page (haftalik/oylik)
- [ ] Friend system (qo'shish, ko'rish, taqqoslash)
- [ ] Achievement sharing (telegram, link)
- [ ] Challenge a friend (1v1 test/game)

---

### Sprint 28-29: Mobile App (35-45 kun) ⚠️ TUZATILDI: 15-20→35-45 kun

**Maqsad:** React Native mobil ilova

> **Sabab (muddat oshganligi):** React Native app — bu faqat "web kodni mobile ga ko'chirish" emas. 7 o'yin, AI chat, offline mode, push notification, TTS, app store submission — barchasi alohida ish talab qiladi. 15-20 kun butunlay yetarsiz.

**Sub-Sprint 28.1 — Core (10-12 kun):**

- [ ] React Native + Expo setup
- [ ] Navigation (React Navigation)
- [ ] Auth flow (Secure storage, biometric)
- [ ] API layer (React Query mobile setup)
- [ ] UI component library (NativeWind / Tamagui)
- [ ] Word CRUD + Review + Dashboard

**Sub-Sprint 28.2 — Features (12-15 kun):**

- [ ] 7 ta o'yin mobile adaptation
- [ ] AI Chat mobile UI
- [ ] Test mobile UI
- [ ] Analytics (Recharts → react-native-chart-kit)
- [ ] Push notifications (Expo Notifications)
- [ ] Smart Import (camera OCR + text input)

**Sub-Sprint 29.1 — Polish + Release (8-10 kun):**

- [ ] Offline mode (MMKV + sync)
- [ ] TTS integration (expo-speech)
- [ ] Deep linking
- [ ] App store assets (screenshots, description)
- [ ] iOS TestFlight + Android Internal Testing
- [ ] Performance optimization (Hermes, lazy loading)

**Sub-Sprint 29.2 — Store Submission (5-8 kun):**

- [ ] App Store review (Apple — 1-3 kun review)
- [ ] Google Play review (1-7 kun review)
- [ ] Privacy policy + Terms of Service
- [ ] COPPA compliance check
- [ ] Bug fixing from beta feedback

---

### Sprint 29.5: Buffer & Stabilization (3-4 kun) ⚠️ YANGI

**Maqsad:** MILESTONE 3 — Mobile + Monetization

**Vazifalari:**

- [ ] Sprint 25-29 bugfixlar
- [ ] Mobile app crash rate < 1% ta'minlash
- [ ] Payment flow end-to-end testing
- [ ] Subscription billing cycle testing
- [ ] Performance audit (mobile + web)
- [ ] Documentation update

---

### Sprint 30-35: Growth Features

| Sprint | Nomi                  | Muddat  | Asosiy vazifalar                                   |
| ------ | --------------------- | ------- | -------------------------------------------------- |
| 30     | B2B / Korporativ      | 7-8 kun | Team accounts, admin panel, bulk licensing         |
| 31     | Content Marketplace   | 6-7 kun | User-created courses, sharing, rating              |
| 32     | Advanced AI           | 5-6 kun | AI tutor, pronunciation checker, writing assistant |
| 33     | Caching + Performance | 4-5 kun | Redis view cache, query optimization, CDN          |
| 34     | Boshqa tillar         | 7-8 kun | Rus-Ingliz, Qozoq-Ingliz kontenti                  |
| 35     | Enterprise SSO + API  | 5-6 kun | SAML/OAuth SSO, public API, API key management     |

---

## ROLLBACK STRATEGIYASI ⚠️ YANGI

### Har bir sprint uchun:

**Backend Rollback:**

```bash
# 1. Migration rollback
python manage.py migrate app_name PREVIOUS_MIGRATION_NUMBER

# 2. Code rollback
git revert SPRINT_MERGE_COMMIT

# 3. Docker rollback
docker-compose -f docker-compose.prod.yml pull  # eski image
docker-compose -f docker-compose.prod.yml up -d

# 4. Database restore (worst case)
pg_restore -h localhost -U postgres -d wordfix backup_YYYYMMDD.dump
```

**Frontend Rollback:**

```bash
# 1. Build rollback
git revert SPRINT_MERGE_COMMIT
npm run build
# 2. CDN cache invalidation (agar CDN ishlatilsa)
```

**Rollback Trigger:**

- p95 response time > 2s (15 daqiqadan ko'p)
- Error rate > 5% (5 daqiqadan ko'p)
- Critical functionality broken (login, review, word add)
- Data loss yoki corruption

**Rollback Window:** Har bir sprint deploy dan keyin 48 soat monitoring. Muammo bo'lmasa — stable deb belgilanadi.

---

## KPI VA METRIKLAR

### Sprint-dan-Sprint KPIlar

| KPI                      | Hozir (Sprint 12.5) | Sprint 18.5 Maqsad | Sprint 24.5 Maqsad | Sprint 36 Maqsad |
| ------------------------ | ------------------- | ------------------ | ------------------ | ---------------- |
| Database modellari       | 31                  | ~40                | ~45                | ~55              |
| API endpointlari         | 103                 | ~130               | ~145               | ~170             |
| Use Cases                | 87                  | ~110               | ~130               | ~160             |
| Frontend routes          | 34                  | ~45                | ~50                | ~60              |
| Test coverage (backend)  | ~30%                | 50%                | 70%                | 80%              |
| Test coverage (frontend) | ~20%                | 40%                | 60%                | 70%              |
| p95 response time        | ~300ms              | <500ms             | <400ms             | <300ms           |
| Error rate               | ?% (Sentry yo'q)    | <2%                | <1%                | <0.5%            |
| Bundle size (gzipped)    | ~450KB              | <500KB             | <400KB             | <350KB           |

### Biznes KPIlar

| KPI                    | Sprint 18.5 | Sprint 24.5 | Sprint 36 |
| ---------------------- | ----------- | ----------- | --------- |
| MAU (Monthly Active)   | 500         | 5,000       | 100,000   |
| DAU/MAU ratio          | 15%         | 25%         | 30%       |
| Free → Paid konversiya | 2%          | 5%          | 8%        |
| Day 7 Retention        | 35%         | 50%         | 60%       |
| Day 30 Retention       | 15%         | 30%         | 40%       |
| MRR (USD)              | $50         | $919        | $85,059   |
| NPS                    | 20+         | 40+         | 50+       |

---

## VAQT JADVALI (UMUMIY)

| Bosqich               | Sprintlar | Kunlar (taxminiy) | Kalendar (taxminiy) |
| --------------------- | --------- | ----------------- | ------------------- |
| Security + Admin      | 13-18.5   | 35-45 kun         | ~2 oy               |
| i18n + PWA + Refactor | 19-24.5   | 35-45 kun         | ~2 oy               |
| Payment + Mobile      | 25-29.5   | 60-75 kun         | ~3 oy               |
| Growth Features       | 30-35     | 35-45 kun         | ~2 oy               |
| **JAMI**              | **13-35** | **165-210 kun**   | **~9-10 oy**        |

> **Eslatma:** Bu jami ~9-10 oy (solo developer, full-time). Part-time bo'lsa 1.5-2x ko'proq vaqt oladi. Buffer sprintlar (18.5, 24.5, 29.5) hisobga olingan.

---

## O'ZGARISHLAR TARIXI

| Sana       | Kim      | Nima o'zgardi                                                                                                                                                                                                     |
| ---------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-27 | AI Agent | Dastlabki versiya yaratildi                                                                                                                                                                                       |
| 2026-02-27 | AI Audit | Raqamlar tuzatildi (103 EP, 31 model, 87 UC, 34 route), Sprint 13.5/16/18.5/24.5/29.5 qo'shildi, Sprint 14 kengaytirildi, vaqt baholar tuzatildi, rollback strategiya qo'shildi, dependencies diagramma qo'shildi |
