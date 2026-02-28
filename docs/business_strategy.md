# WordFix — Business Strategy

> Bu fayl loyihaning biznes strategiyasini, bozor tahlilini va monetizatsiya rejasini tavsiflaydi.
> Barcha raqamlar haqiqiy bozor ma'lumotlari va kod bazasidan olingan.
> Oxirgi yangilangan: 2026-02-27

### CHANGELOG (2026-02-27 Audit)

- Narxlar to'liq qayta ko'rib chiqildi — Barcha 4 hujjat uchun yagona narx: UZS-asosli
- MRR hisoblari qayta kalkulyatsiya qilindi (real formula bilan)
- Server xarajatlari realga moslandi ($20/$50/$100/$300/$800)
- Raqobatchilar SR da'volari tuzatildi (Duolingo Birdbrain, Quizlet Learn mode)
- "Self-hosted/privacy" xususiyat jadvalidan olib tashlandi
- Enterprise "dedicated manager" → "Priority email support (24h)" ga o'zgartirildi
- TAM/SAM/SOM manbalari qo'shildi
- Developer xarajat eslatmasi qo'shildi
- Marketing byudjet qo'shildi
- Mahalliy raqobatchilar qo'shildi
- Free tier limitlari barcha hujjatlarda birlashtirildi
- Badge soni 18 → 31 ga tuzatildi

---

## 1. BOZOR TAHLILI

### 1.1 TAM / SAM / SOM

| Metric | Hajm    | Izoh                                                                           | Manba                                              |
| ------ | ------- | ------------------------------------------------------------------------------ | -------------------------------------------------- |
| TAM    | ~$65.5B | Global til o'rganish bozori (2025)                                             | Grand View Research, 2024 Report                   |
| SAM    | ~$200M  | Markaziy Osiyo + MDH ingliz tili o'rganuvchilar (app orqali)                   | Baholash: O'zbekiston + Qozog'iston + Qirg'iziston |
| SOM    | ~$2-5M  | O'zbekiston premium app orqali ingliz tili o'rganuvchilar (realistik baholash) | O'zbekiston internet foydalanuvchilar: ~25M (2025) |

> **Muhim:** SOM ning $2-5M diapazoni O'zbekistonda ~25M internet foydalanuvchi, ~5M activ ingliz tili o'rganuvchi va ~2-5% premium konversiya asosida hisoblangan. Bu aggressiv emas, konservativ baholash.

### 1.2 O'zbekiston Bozor Konteksti

| Faktor           | Holat                                                   |
| ---------------- | ------------------------------------------------------- |
| Aholi            | ~36M, median yosh 27.8                                  |
| Internet         | ~25M foydalanuvchi (70%+ penetratsiya)                  |
| Smartphone       | ~85% internet foydalanuvchilar orasida                  |
| Ingliz tili      | Davlat siyosati: 2030 yilgacha ingliz tili majburiy     |
| To'lov tizimlari | Payme, Click, Uzum — keng tarqalgan                     |
| Raqobat          | Past — mahalliy ixtisoslashgan app yo'q (quyida qarang) |

### 1.3 Raqobatchilar Tahlili

| Raqobatchi  | Turi         | SR Texnologiyasi                                | O'zbek tili     | Narx (oylik)       | Kuchli tomoni            | Zaif tomoni                          |
| ----------- | ------------ | ----------------------------------------------- | --------------- | ------------------ | ------------------------ | ------------------------------------ |
| Duolingo    | Global       | ⚠️ O'z algoritmi (Birdbrain) — SM-2 EMAS        | Ha (cheklangan) | Free / $7.99       | Gamification, brend      | O'zbek kontenti past sifat           |
| Quizlet     | Global       | ⚠️ Learn mode SR — klassik Leitner EMAS         | Yo'q            | Free / $7.99       | Flashcard, foydalanuvchi | SR algoritmi yuzaki                  |
| Memrise     | Global       | ⚠️ O'z SR algoritmi — SM-2 EMAS                 | Yo'q            | Free / $8.49       | Native video             | O'zbek tili yo'q                     |
| Anki        | Open Source  | ✅ SM-2 (asl implementatsiya)                   | Community       | Free (desktop)     | SR standarti, tekin      | UI eskirgan, texnik bilim kerak      |
| **WordFix** | **Mahalliy** | **✅ SM-2 + AI Adaptive (3 provider fallback)** | **To'liq**      | **Free / 29K UZS** | **AI, gamification, UZ** | **Yangi, kichik foydalanuvchi baza** |

### 1.4 Mahalliy Raqobatchilar (O'zbekiston)

| Raqobatchi       | Turi           | Holat                                         | Farqimiz                                |
| ---------------- | -------------- | --------------------------------------------- | --------------------------------------- |
| Kitapp           | Kitob/audio    | Umumiy ta'lim, ingliz tiliga ixtisoslashmagan | Biz: faqat ingliz tili, AI-powered      |
| Preply tutors    | Tutor platform | 1:1 darslar, qimmat ($15-30/soat)             | Biz: self-paced, 100x arzon             |
| Telegram botlar  | Bot            | Oddiy flashcard, SR yo'q                      | Biz: to'liq SR + 7 o'yin + AI chat      |
| YouTube kanallar | Video          | Passiv o'rganish, tracking yo'q               | Biz: aktiv o'rganish, progress tracking |

### 1.5 Raqobat Ustunligi (Competitive Moat)

| Ustunlik                   | Izoh                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| AI-First arxitektura       | 3 AI provider fallback (Groq → Gemini → OpenAI → Hardcoded)                                       |
| SM-2 + Adaptive difficulty | Klassik SM-2 + AI-based qiyinlik moslash                                                          |
| O'zbek tili lokalizatsiya  | To'liq UZ interfeys + UZ-EN tarjima optimizatsiya                                                 |
| 7 ta o'yin turi            | Speed Round, Word Match, Word Context, Story Builder, Listening, Synonym-Antonym, Irregular Verbs |
| 31 ta badge + XP tizimi    | Gamification: 9 kategoriya, 4 rarity darajasi                                                     |
| AI Chat                    | Kontekstli suhbat: target words + grammar correction                                              |
| Smart Import               | AI-First: matn → so'z ajratish + tarjima + CEFR + IPA (2-bosqichli)                               |
| Confusing Pairs            | AI-powered: chalkash so'zlarni avtomatik aniqlash + mashq                                         |

---

## 2. MONETIZATSIYA STRATEGIYASI

### 2.1 Narx Rejalari (Yagona — barcha hujjatlarda bir xil)

| Reja           | Narx (oylik) | Narx (USD ekvivalent) | Maqsadli auditoriya                       |
| -------------- | ------------ | --------------------- | ----------------------------------------- |
| **Free**       | 0 UZS        | $0                    | Barcha — funnel boshi                     |
| **Basic**      | 29,000 UZS   | ~$2.29                | Talabalar, o'z-o'zini rivojlantiruvchilar |
| **Pro**        | 59,000 UZS   | ~$4.66                | Faol o'rganuvchilar                       |
| **Enterprise** | 149,000 UZS  | ~$11.79               | Professional / korporativ                 |

> **Kurs:** 1 USD ≈ 12,650 UZS (2025-Q4 o'rtacha)

### 2.2 Reja Xususiyatlari

| Xususiyat           | Free          | Basic           | Pro         | Enterprise     |
| ------------------- | ------------- | --------------- | ----------- | -------------- |
| So'zlar limiti      | 50 ta         | 500 ta          | Cheksiz     | Cheksiz        |
| Review / kun        | 5 ta          | Cheksiz         | Cheksiz     | Cheksiz        |
| Test / kun          | 1 ta          | 3 ta            | Cheksiz     | Cheksiz        |
| O'yinlar            | 3 ta (asosiy) | Barcha 7 ta     | Barcha 7 ta | Barcha 7 ta    |
| AI Enrichment       | 5 / kun       | 20 / kun        | Cheksiz     | Cheksiz        |
| AI Chat             | ❌            | 3 sessiya/kun   | Cheksiz     | Cheksiz        |
| Smart Import (matn) | ❌            | 3 / kun         | Cheksiz     | Cheksiz        |
| CSV Import          | ❌            | ❌              | ✅          | ✅             |
| Analytics           | Asosiy        | Asosiy          | To'liq      | To'liq         |
| Confusing Pairs     | Ko'rish       | Ko'rish + Drill | To'liq      | To'liq         |
| Learning Profile    | ❌            | Asosiy          | To'liq + AI | To'liq + AI    |
| Priority support    | ❌            | ❌              | ❌          | ✅ (24h email) |
| API access          | ❌            | ❌              | ❌          | ✅             |

> ⚠️ **MUHIM:** Hozirgi kod bazasida premium/subscription modeli **mavjud emas**. Faqat `CustomUser.is_premium` boolean field va `premium_until` DateTimeField bor. To'liq subscription management Sprint 25 da rejalashtirilgan. Yuqoridagi limitlar **kelajak reja** — hozir barcha funksiyalar barcha foydalanuvchilar uchun ochiq.

### 2.3 Konversiya Funneli (Maqsad)

```
Free Users (100%)
    │
    ├── Month 1-3:  2% → Basic,  1% → Pro,   0.1% → Enterprise
    ├── Month 4-6:  5% → Basic,  3% → Pro,   0.5% → Enterprise
    ├── Month 7-12: 8% → Basic,  5% → Pro,   1.0% → Enterprise
    └── Month 13+: 10% → Basic,  7% → Pro,   2.0% → Enterprise
```

---

## 3. MOLIYAVIY PROYEKSIYALAR

### 3.1 MRR (Monthly Recurring Revenue) Hisoblari

> **Formula:** MRR = (Basic users × 29,000) + (Pro users × 59,000) + (Enterprise users × 149,000)

| Oy  | Basic  | Pro   | Enterprise | MRR (UZS)     | MRR (USD) | Kumulyativ (UZS) |
| --- | ------ | ----- | ---------- | ------------- | --------- | ---------------- |
| 1   | 3      | 2     | 0          | 205,000       | $16       | 205,000          |
| 3   | 30     | 15    | 3          | 2,202,000     | $174      | 4,609,000        |
| 6   | 130    | 70    | 25         | 11,625,000    | $919      | 38,484,000       |
| 12  | 560    | 280   | 120        | 50,640,000    | $4,003    | 248,244,000      |
| 18  | 1,700  | 900   | 400        | 162,000,000   | $12,806   | 1,128,244,000    |
| 24  | 4,800  | 2,500 | 1,200      | 465,500,000   | $36,798   | 4,308,244,000    |
| 36  | 10,500 | 5,500 | 3,000      | 1,076,000,000 | $85,059   | 15,000,000,000+  |

> **Eslatma:** Bu proyeksiyalar OPTIMISTIK senariy. "Conservativ" senariy uchun barcha raqamlarni 3x ga bo'ling. Dastlabki 6 oy daromad deyarli nol bo'lishi kutiladi.

### 3.2 Xarajatlar Tuzilmasi

| Xarajat turi       | Oy 1-3   | Oy 4-6   | Oy 7-12   | Oy 13-24  | Oy 25-36    | Izoh                          |
| ------------------ | -------- | -------- | --------- | --------- | ----------- | ----------------------------- |
| Server (VPS/Cloud) | $20/oy   | $50/oy   | $100/oy   | $300/oy   | $800/oy     | Hetzner → DigitalOcean → AWS  |
| AI API             | $5/oy    | $20/oy   | $80/oy    | $250/oy   | $600/oy     | Groq (free tier) → paid       |
| Domain + SSL       | $15/yil  | —        | $15/yil   | $15/yil   | $15/yil     | .uz yoki .com                 |
| Marketing          | $0/oy    | $0/oy    | $50/oy    | $200/oy   | $500/oy     | Telegram ads, SEO, influencer |
| TTS API            | $0/oy    | $5/oy    | $20/oy    | $50/oy    | $100/oy     | Google TTS / Azure            |
| Developer          | $0\*     | $0\*     | $0\*      | $0\*      | $0-2000\*   | \*qarang: pastda              |
| **Jami (oylik)**   | **~$25** | **~$75** | **~$265** | **~$815** | **~$2,015** |                               |

> **\*Developer xarajat eslatmasi:** Hozir loyiha solo developer tomonidan rivojlantiriladi (Firdavs). Oy haqqi $0, lekin imkoniyat xarajati (opportunity cost) ~$400-800/oy (O'zbekiston developer o'rtacha maoshi). 25+ oyda jamoa kengaytirish rejalashtirilgan ($1,000-2,000/oy).

### 3.3 Break-Even Tahlili

```
Break-even = Oylik xarajat / O'rtacha ARPU

O'rtacha ARPU (taxminiy): (29,000 × 0.6) + (59,000 × 0.3) + (149,000 × 0.1) = 50,000 UZS ≈ $3.95

Month 1-3:  $25 / $3.95 = 7 to'lovchi user → Break-even
Month 7-12: $265 / $3.95 = 68 to'lovchi user → Break-even
Month 13-24: $815 / $3.95 = 207 to'lovchi user → Break-even
Month 25-36: $2,015 / $3.95 = 511 to'lovchi user → Break-even
```

> **Xulosa:** Dastlabki 6 oyda break-even 7-20 to'lovchi user bilan erishilishi mumkin. Bu juda qulay chunki server xarajati past ($20-50/oy).

### 3.4 Foyda Proyeksiyasi

| Oy  | MRR (USD) | Xarajat (USD) | Sof foyda (USD) | Marja    |
| --- | --------- | ------------- | --------------- | -------- |
| 1   | $16       | $25           | -$9             | ❌ Zarar |
| 3   | $174      | $25           | +$149           | 86%      |
| 6   | $919      | $75           | +$844           | 92%      |
| 12  | $4,003    | $265          | +$3,738         | 93%      |
| 18  | $12,806   | $815          | +$11,991        | 94%      |
| 24  | $36,798   | $815          | +$35,983        | 98%      |
| 36  | $85,059   | $2,015        | +$83,044        | 98%      |

> **Ogohlantirish:** Yuqori marja SaaS industryada normal (70-90%), lekin bu raqamlar developer maoshi HISOBGA OLINMAGAN. Agar $800/oy developer maoshi qo'shilsa, dastlabki 12 oyda marja ~50-60% ga tushadi.

---

## 4. FEATURE COMPARISON (Xususiyat Solishtirish)

| Xususiyat                   | WordFix        | Duolingo      | Quizlet    | Anki         | Memrise    |
| --------------------------- | -------------- | ------------- | ---------- | ------------ | ---------- |
| SM-2 Spaced Repetition      | ✅ SM-2 + AI   | ❌\*          | ❌\*       | ✅ SM-2      | ❌\*       |
| AI So'z Boyitish            | ✅ 3 provider  | ❌            | ❌         | ❌           | ❌         |
| AI Chat (kontekstli)        | ✅             | ❌            | ❌         | ❌           | ❌         |
| Smart Import (matn tahlil)  | ✅ AI-First    | ❌            | ❌         | ❌           | ❌         |
| O'zbek tili support         | ✅ To'liq      | ⚠️ Cheklangan | ❌         | ⚠️ Community | ❌         |
| O'yin turlari               | 7 ta           | 5-6 ta        | 3-4 ta     | 0 ta         | 2-3 ta     |
| Badge tizimi                | 31 ta (9 kat.) | Bor           | Yo'q       | Yo'q         | Bor        |
| Confusing Pairs AI          | ✅             | ❌            | ❌         | ❌           | ❌         |
| Learning Profile (adaptive) | ✅             | ⚠️            | ❌         | ❌           | ❌         |
| CSV Import                  | ✅             | ❌            | ✅         | ✅           | ❌         |
| Daily Challenges            | ✅             | ✅            | ❌         | ❌           | ✅         |
| Analytics (haftalik/oylik)  | ✅             | ⚠️            | ❌         | ⚠️ Plugin    | ❌         |
| Narx (oylik)                | Free / $2.29   | Free/$7.99    | Free/$7.99 | Free         | Free/$8.49 |
| Mahalliy to'lov (UZS)       | ✅ Payme/Click | ❌            | ❌         | —            | ❌         |

> **\*** Duolingo o'z "Birdbrain" algoritmini ishlatadi (SM-2 emas). Quizlet "Learn mode" da oddiy SR bor (klassik Leitner emas). Memrise o'z SR algoritmini ishlatadi (SM-2 emas). Faqat Anki haqiqiy SM-2 implementatsiyaga ega.

---

## 5. MARKETING STRATEGIYASI

### 5.1 Bosqichlar

| Bosqich            | Muddat   | Kanal                         | Byudjet (oylik) | Maqsad              |
| ------------------ | -------- | ----------------------------- | --------------- | ------------------- |
| **MVP Launch**     | Oy 1-3   | Telegram, O'zbek IT community | $0 (organic)    | 100-500 beta users  |
| **Early Traction** | Oy 4-6   | SEO, App Store Optimization   | $0 (organic)    | 1,000-2,000 users   |
| **Growth**         | Oy 7-12  | Telegram ads, YouTube UZ      | $50/oy          | 5,000-10,000 users  |
| **Scale**          | Oy 13-24 | Instagram, Telegram, Referral | $200/oy         | 20,000-50,000 users |
| **Expansion**      | Oy 25-36 | Multi-channel, Influencer     | $500/oy         | 100,000+ users      |

### 5.2 Asosiy Kanallar

| Kanal           | Sabab                                        | Strategiya                            |
| --------------- | -------------------------------------------- | ------------------------------------- |
| Telegram        | O'zbekistonda #1 messenger (~20M users)      | WordFix kanal + guruh + mini-app      |
| Instagram       | O'zbek yoshlar orasida populyar              | Reels: "Bugungi so'z", tips           |
| YouTube (UZ)    | Uzun format kontent, SEO                     | Tutorial, review video                |
| Referral dastur | Word-of-mouth eng samarali kanal             | "Do'stingizga ulashing → 50 XP bonus" |
| Universitetlar  | To'g'ridan-to'g'ri maqsadli auditoriya       | Talabalar uchun bepul Pro (1 oy)      |
| SEO (Google UZ) | "Ingliz tili o'rganish" qidiruv hajmi yuqori | Blog, landing page optimization       |

### 5.3 Retention Strategiyasi

| Strategiya        | Mexanizm                                       | Hozirgi holat              |
| ----------------- | ---------------------------------------------- | -------------------------- |
| Daily Streak      | Streak yo'qolish qo'rquvi (loss aversion)      | ✅ Implemented             |
| Push Notification | Review reminder, streak warning                | ⚠️ In-app only (PWA kerak) |
| Daily Challenges  | Har kuni yangi 3 ta challenge + bonus XP       | ✅ Implemented             |
| Badge System      | 31 ta badge, progressive unlock                | ✅ Implemented             |
| Leaderboard       | Haftalik/oylik reyting                         | ❌ Sprint 27 da            |
| Weekly Report     | Haftalik progress xulosa (in-app notification) | ✅ Implemented (Celery)    |

---

## 6. TEXNIK IMKONIYATLAR XARITASI

### 6.1 Hozirgi Texnik Stack (Kod bazasidan)

| Komponent       | Texnologiya                      | Versiya    |
| --------------- | -------------------------------- | ---------- |
| Backend         | Django + DRF                     | 5.x + 3.15 |
| Frontend        | React + TypeScript               | 19 + 5.6   |
| Database        | PostgreSQL                       | 16-alpine  |
| Cache/Broker    | Redis                            | 7-alpine   |
| Task Queue      | Celery + Beat                    | 5.4        |
| Auth            | SimpleJWT + django-allauth       | 5.3        |
| AI (Primary)    | Groq (llama-3.3-70b-versatile)   | —          |
| AI (Fallback 1) | Google Gemini (gemini-2.0-flash) | —          |
| AI (Fallback 2) | OpenAI (gpt-4o-mini)             | —          |
| Build           | Vite                             | 6          |
| State           | Zustand + TanStack Query         | 5 + 5      |
| Styling         | Tailwind CSS                     | 3.4        |
| Docker          | Docker Compose (7 services)      | —          |

### 6.2 Scaling Yo'l Xaritasi

| Bosqich      | Users    | Infra                                       | Narx (oylik) |
| ------------ | -------- | ------------------------------------------- | ------------ |
| MVP          | 0-1K     | Single VPS (2-4GB RAM, Hetzner)             | $20          |
| Early Growth | 1K-10K   | Dedicated CPU + Managed PostgreSQL          | $50          |
| Growth       | 10K-50K  | 2 server + Load balancer + CDN              | $100-300     |
| Scale        | 50K-200K | Multi-server + Redis Cluster + Monitoring   | $300-800     |
| Enterprise   | 200K+    | Kubernetes / Cloud (AWS/GCP) + Auto-scaling | $1,000+      |

---

## 7. RISK ASSESSMENT

### 7.1 Texnik Risklar

| Risk                      | Ehtimollik | Ta'sir | Yechim                                                |
| ------------------------- | ---------- | ------ | ----------------------------------------------------- |
| AI API narx oshishi       | O'rta      | Yuqori | FallbackAIProvider (hardcoded) mavjud                 |
| Groq API cheklash/xizmat  | O'rta      | Yuqori | 3 provider fallback + Circuit Breaker                 |
| PostgreSQL scaling muammo | Past       | O'rta  | Read replicas, connection pooling (PgBouncer)         |
| Redis memory overflow     | Past       | O'rta  | Maxmemory policy + monitoring                         |
| Security breach           | Past       | Yuqori | JWT rotation, rate limiting, OWASP top 10 (Sprint 14) |

### 7.2 Biznes Risklar

| Risk                           | Ehtimollik | Ta'sir | Yechim                                         |
| ------------------------------ | ---------- | ------ | ---------------------------------------------- |
| Foydalanuvchi kam              | O'rta      | Yuqori | Free tier keng, organic marketing, referral    |
| Duolingo UZ kontent yaxshilash | Past       | O'rta  | AI + custom-content ustunlik saqlanadi         |
| To'lov integratsiya muammo     | Past       | Yuqori | Payme/Click SDK + fallback bank transfer       |
| Solo developer burn-out        | O'rta      | Yuqori | Sprint buffer, realistic estimates, automation |
| Kurs o'zgarishi (UZS/USD)      | O'rta      | Past   | Narxlar UZS da aniqlangan, API xarajat USD     |

### 7.3 Regulatory Risklar

| Risk                        | Ehtimollik | Ta'sir | Yechim                                                  |
| --------------------------- | ---------- | ------ | ------------------------------------------------------- |
| Ma'lumotlar himoyasi qonuni | O'rta      | O'rta  | GDPR-like privacy policy, data export, account deletion |
| AI kontenti nazorat         | Past       | Past   | Content filter + moderatsiya flag                       |

---

## 8. O'SISH STRATEGIYASI (Kelajak 36 oy)

### Phase 1: MVP → Product-Market Fit (Oy 1-6)

- ✅ Core funksionallik (87 use case)
- ✅ AI integration (3 provider fallback)
- ✅ Gamification (31 badge, 7 o'yin, XP, streak)
- 🔜 Security hardening (Sprint 14)
- 🔜 Contact/Feedback (Sprint 15)
- 🔜 Admin Panel (Sprint 16-17)
- 🔜 Stability sprint (Sprint 18.5)

### Phase 2: Growth (Oy 7-12)

- PWA + Offline mode
- i18n (Rus, Qozoq tili)
- Payment integration (Payme/Click)
- Feature gating (Free/Basic/Pro/Enterprise limitlar)
- Advanced Leaderboard + Social features

### Phase 3: Scale (Oy 13-24)

- Mobile app (React Native)
- Content marketplace
- B2B/Korporativ paketlar
- Advanced analytics + AI recommendations
- Multi-region deployment

### Phase 4: Expansion (Oy 25-36)

- Boshqa tillar (Rus-Ingliz, Qozoq-Ingliz)
- White-label B2B
- API marketplace
- Community kontent
- Enterprise features (SSO, audit log)

---

## 9. KPI VA METRIKLAR

### 9.1 Asosiy KPIlar

| KPI                    | Maqsad (Oy 6) | Maqsad (Oy 12) | Maqsad (Oy 24) | Hisoblash                |
| ---------------------- | ------------- | -------------- | -------------- | ------------------------ |
| MAU (Monthly Active)   | 1,000         | 5,000          | 50,000         | Oyda 1+ sessiya          |
| DAU/MAU ratio          | 20%+          | 25%+           | 30%+           | Kundalik faollik / oylik |
| Free → Paid konversiya | 3%            | 5%             | 8%             | To'lovchi / jami users   |
| Day 7 Retention        | 40%           | 50%            | 60%            | 7-kun qaytish            |
| Day 30 Retention       | 20%           | 30%            | 40%            | 30-kun qaytish           |
| ARPU (oylik)           | $2.00         | $3.50          | $4.00          | MRR / to'lovchi users    |
| Churn rate             | <10%          | <8%            | <5%            | Oylik bekor qilish       |
| NPS                    | 30+           | 40+            | 50+            | Net Promoter Score       |

### 9.2 Funnel Metriklar

```
Landing → Register:    30-40% (maqsad)
Register → Onboarding: 80-90%
Onboarding → 1st Word: 70-80%
1st Word → Day 7:      40-50%
Day 7 → Day 30:        50-60%
Day 30 → Premium:      3-8%
```

---

## O'ZGARISHLAR TARIXI

| Sana       | Kim      | Nima o'zgardi                                                                                                                             |
| ---------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-27 | AI Agent | Dastlabki versiya yaratildi                                                                                                               |
| 2026-02-27 | AI Audit | MRR qayta hisoblandi, server cost realga moslandi, raqobatchi SR tuzatildi, marketing byudjet qo'shildi, mahalliy raqobatchilar qo'shildi |
