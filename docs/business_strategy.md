# WordFix — Business Strategy

> Bu fayl loyihaning biznes strategiyasini, bozor tahlilini va monetizatsiya rejasini tavsiflaydi.
> Barcha raqamlar haqiqiy bozor ma'lumotlari va kod bazasidan olingan.
> Oxirgi yangilangan: 2026-02-28

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

### CHANGELOG (2026-02-28 Monetizatsiya Rewrite)

- **Tier nomlar o'zgardi:** Basic → Starter, Enterprise → Premium (individual), yangi Enterprise = B2B
- **Narxlar:** Free/0 → Starter/29K → Pro/59K → Premium/99K UZS (Enterprise alohida B2B: $49-99/oy)
- **Yillik rejalar qo'shildi:** Starter 249K, Pro 499K, Premium 849K UZS (~29-30% chegirma)
- **AI Model Selection tizimi qo'shildi:** Basic(Groq)/Standard(Gemini)/Professional(GPT-4o) — user tanlaydi
- **Falsafa o'zgardi:** "BARCHA funksiyalar barchaga ochiq — faqat MIQDOR farq qiladi"
- Free tier saxiyroq: 30 so'z/kun (150 max), 15 AI chat, 30 o'yin, 30 AI enrichment, 5 test, 50 CSV
- ❌ Hech qanday funksiya yopilmaydi (AI Chat, Smart Import, CSV — barchaga ochiq)
- ❌ PDF Import — hech qanday tier'da yo'q
- Arxivlangan so'zlar jami sig'imga kiradi
- MRR formula yangilandi: (Starter × 29K) + (Pro × 59K) + (Premium × 99K)
- AI API xarajat taqsimoti tier bo'yicha qo'shildi
- ARPU qayta hisoblandi: $3.83 (eski $3.95)
- Konversiya trigeri aniqlandi: "150 ta so'z limiti tugadi"

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

### 2.0 Asosiy Falsafa

> **"FREE tier — SAXIY bo'lsin. Foydalanuvchi bepul rejada WordFix'dan haqiqiy foyda ko'rsin. BARCHA funksiyalar barchaga ochiq — faqat MIQDOR farq qiladi."**

- ❌ Hech qanday funksiya butunlay yopilmaydi (AI Chat, Smart Import, CSV — barchaga ochiq)
- ✅ Barcha 7 ta o'yin — barchaga ochiq
- ✅ Barcha analytics, gamification, review — to'liq ochiq
- ✅ Farq faqat: kunlik limit, so'z sig'imi, AI model tanlovi
- 🎯 Konversiya trigeri: **"150 ta so'z limiti tugadi"** — bu eng kuchli upsell moment

### 2.1 AI Model Tanlov Tizimi (YANGI)

> Foydalanuvchi o'zi tanlaydi qaysi AI modeldan foydalanish. Bu subscription tier bilan bog'liq.

| AI Tier             | Model                | Tezlik      | Sifat      | Narx (1K tokenga) | Subscription kerak |
| ------------------- | -------------------- | ----------- | ---------- | ----------------- | ------------------ |
| 🟢 **Basic**        | Groq (llama-3.3-70b) | ⚡ Juda tez | ⭐⭐⭐     | ~$0 (free tier)   | Free               |
| 🟡 **Standard**     | Gemini 2.0 Flash     | 🚀 Tez      | ⭐⭐⭐⭐   | ~$0.10            | Starter+           |
| 🔴 **Professional** | GPT-4o-mini / GPT-4o | 🐢 O'rtacha | ⭐⭐⭐⭐⭐ | ~$0.50            | Pro+               |

**AI Model + Subscription aloqasi:**

| Subscription | Basic (Groq) | Standard (Gemini) | Professional (GPT-4o) |
| ------------ | ------------ | ----------------- | --------------------- |
| **Free**     | ✅ (30/kun)  | ❌                | ❌                    |
| **Starter**  | ✅ Cheksiz   | ✅ (60/kun)       | ❌                    |
| **Pro**      | ✅ Cheksiz   | ✅ Cheksiz        | ✅ (50/kun)           |
| **Premium**  | ✅ Cheksiz   | ✅ Cheksiz        | ✅ Cheksiz            |

> **Texnik:** Mavjud fallback zanjiri (Groq → Gemini → OpenAI → Hardcoded) saqlanadi. Foydalanuvchi tanlagan model **birinchi** uriniladi, keyin fallback ishlaydi.

### 2.2 Narx Rejalari (Yagona — barcha hujjatlarda bir xil)

| Reja           | Oylik narx          | USD ekvivalent | Yillik narx | Yillik USD | Chegirma | Maqsadli auditoriya                       |
| -------------- | ------------------- | -------------- | ----------- | ---------- | -------- | ----------------------------------------- |
| **Free**       | 0 UZS               | $0             | —           | —          | —        | Barcha — funnel boshi                     |
| **Starter**    | 29,000 UZS          | ~$2.29         | 249,000 UZS | ~$19.68    | ~29%     | Talabalar, o'z-o'zini rivojlantiruvchilar |
| **Pro**        | 59,000 UZS          | ~$4.66         | 499,000 UZS | ~$39.45    | ~30%     | Faol o'rganuvchilar                       |
| **Premium**    | 99,000 UZS          | ~$7.83         | 849,000 UZS | ~$67.11    | ~29%     | Jiddiy professional o'rganuvchilar        |
| **Enterprise** | $49-99/oy (per org) | —              | Kelishiladi | —          | —        | B2B: ta'lim muassasalari, korporativ      |

> **Kurs:** 1 USD ≈ 12,650 UZS (2025-Q4 o'rtacha)
>
> **Enterprise** alohida B2B tier: 50 ta user per org, admin panel, bulk licensing, priority support. Individual subscription bilan aralashtirilMASIN.

### 2.3 Reja Xususiyatlari — Batafsil Solishtirish

> **Prinsip:** Barcha funksiyalar barchaga ochiq. Faqat **miqdor** farq qiladi.

#### 📦 So'z Saqlash

| Xususiyat         | Free                 | Starter (29K)        | Pro (59K)            | Premium (99K)        |
| ----------------- | -------------------- | -------------------- | -------------------- | -------------------- |
| Kunlik qo'shish   | 30 ta/kun            | 120 ta/kun           | 500 ta/kun           | 1,000 ta/kun         |
| Jami so'z sig'imi | 150 ta               | 400 ta               | 1,200 ta             | 2,000 ta             |
| Archive           | ✅ (sig'imga kiradi) | ✅ (sig'imga kiradi) | ✅ (sig'imga kiradi) | ✅ (sig'imga kiradi) |

> ⚠️ Arxivlangan so'zlar ham jami sig'imga kiritiladi. Masalan: Free user 100 ta aktiv + 50 ta arxiv = 150 ta limit to'lgan.

#### 🎮 O'yinlar

| Xususiyat           | Free        | Starter     | Pro         | Premium     |
| ------------------- | ----------- | ----------- | ----------- | ----------- |
| O'yin turlari       | Barcha 7 ta | Barcha 7 ta | Barcha 7 ta | Barcha 7 ta |
| Kunlik o'yin limiti | 30 ta/kun   | 100 ta/kun  | Cheksiz     | Cheksiz     |

#### 🤖 AI Xususiyatlar

| Xususiyat           | Free           | Starter                | Pro                                   | Premium                 |
| ------------------- | -------------- | ---------------------- | ------------------------------------- | ----------------------- |
| AI Enrichment       | 30 ta/kun      | 120 ta/kun             | 500 ta/kun                            | Cheksiz                 |
| AI Chat             | 15 xabar/kun   | 60 xabar/kun           | Cheksiz                               | Cheksiz                 |
| AI Test generatsiya | 5 ta/kun       | 20 ta/kun              | Cheksiz                               | Cheksiz                 |
| AI Model            | 🟢 Basic faqat | 🟢 Basic + 🟡 Standard | 🟢🟡🔴 Barchasi (50/kun Professional) | 🟢🟡🔴 Barchasi Cheksiz |

#### 📥 Import

| Xususiyat           | Free        | Starter      | Pro          | Premium      |
| ------------------- | ----------- | ------------ | ------------ | ------------ |
| Smart Import (matn) | 30 ta/kun   | 100 ta/kun   | 200 ta/kun   | Cheksiz      |
| CSV Import          | 50 ta/batch | 150 ta/batch | 300 ta/batch | 500 ta/batch |

> ❌ **PDF Import** — hech qanday tier'da yo'q. Roadmap'da ham yo'q.

#### 🔥 Streak & Offline

| Xususiyat         | Free  | Starter    | Pro        | Premium |
| ----------------- | ----- | ---------- | ---------- | ------- |
| Streak Protection | ❌    | 1 marta/oy | 3 marta/oy | Cheksiz |
| Offline so'zlar   | 50 ta | 200 ta     | 500 ta     | Cheksiz |

#### 📊 Har kunda ochiq (BARCHA tierlarda bir xil)

| Xususiyat                  | Holat                  |
| -------------------------- | ---------------------- |
| Spaced Repetition (SM-2)   | ✅ To'liq — limit yo'q |
| Analytics (haftalik/oylik) | ✅ To'liq — limit yo'q |
| Badges + XP + Level        | ✅ To'liq — limit yo'q |
| Confusing Pairs            | ✅ To'liq — limit yo'q |
| Learning Profile           | ✅ To'liq — limit yo'q |
| Daily Challenges           | ✅ To'liq — limit yo'q |
| Notifications              | ✅ To'liq — limit yo'q |

#### 📢 Reklama

| Xususiyat | Free                | Starter+ (barcha pullik)  |
| --------- | ------------------- | ------------------------- |
| Reklama   | ✅ Minimal (banner) | ❌ Reklama yo'q (Ad-free) |

#### 🏢 Enterprise (alohida B2B tier)

| Xususiyat               | Enterprise ($49-99/oy per org) |
| ----------------------- | ------------------------------ |
| Foydalanuvchilar        | 50 ta per org                  |
| Barcha Premium features | ✅                             |
| Admin Panel (org)       | ✅ Team management             |
| Bulk Licensing          | ✅                             |
| Priority Support        | ✅ (24h email, dedicated)      |
| Custom Analytics        | ✅ Organization-level report   |
| SSO (SAML/OAuth)        | ✅ (Sprint 35)                 |
| API Access              | ✅                             |

> ⚠️ **MUHIM:** Hozirgi kod bazasida premium/subscription modeli **mavjud emas**. Faqat `CustomUser.is_premium` boolean field va `premium_until` DateTimeField bor. To'liq subscription management Sprint 25 da rejalashtirilgan. Yuqoridagi limitlar **kelajak reja** — hozir barcha funksiyalar barcha foydalanuvchilar uchun ochiq.

### 2.4 Konversiya Funneli (Maqsad)

```
Free Users (100%)
    │
    ├── Month 1-3:  3% → Starter,  1% → Pro,   0.2% → Premium
    ├── Month 4-6:  5% → Starter,  3% → Pro,   0.5% → Premium
    ├── Month 7-12: 8% → Starter,  5% → Pro,   1.0% → Premium
    └── Month 13+: 10% → Starter,  7% → Pro,   2.0% → Premium
```

> **Asosiy konversiya trigeri:** "150 ta so'z limiti tugadi" — bu moment foydalanuvchi uchun eng og'riqli va Starter'ga o'tish motivatsiyasi eng yuqori.

---

## 3. MOLIYAVIY PROYEKSIYALAR

### 3.1 MRR (Monthly Recurring Revenue) Hisoblari

> **Formula:** MRR = (Starter users × 29,000) + (Pro users × 59,000) + (Premium users × 99,000) UZS
>
> **Enterprise** B2B alohida hisoblanadi (individual MRR ga kiritilmaydi)

| Oy  | Starter | Pro   | Premium | MRR (UZS)   | MRR (USD) | Kumulyativ (UZS) |
| --- | ------- | ----- | ------- | ----------- | --------- | ---------------- |
| 1   | 5       | 2     | 0       | 263,000     | $21       | 263,000          |
| 3   | 35      | 15    | 5       | 2,395,000   | $189      | 5,053,000        |
| 6   | 150     | 70    | 30      | 11,450,000  | $905      | 38,753,000       |
| 12  | 600     | 300   | 100     | 44,900,000  | $3,549    | 215,653,000      |
| 18  | 1,800   | 950   | 350     | 142,350,000 | $11,249   | 978,753,000      |
| 24  | 5,000   | 2,600 | 1,000   | 398,400,000 | $31,494   | 3,678,753,000    |
| 36  | 11,000  | 6,000 | 2,500   | 920,500,000 | $72,767   | 12,500,000,000+  |

> **Eslatma:** Bu proyeksiyalar OPTIMISTIK senariy. "Conservativ" senariy uchun barcha raqamlarni 3x ga bo'ling. Dastlabki 6 oy daromad deyarli nol bo'lishi kutiladi.
>
> **Enterprise B2B qo'shimcha:** Oy 12+ da 5-10 ta org × $49-99/oy = $245-$990/oy qo'shimcha daromad.

### 3.2 Xarajatlar Tuzilmasi

| Xarajat turi       | Oy 1-3   | Oy 4-6   | Oy 7-12   | Oy 13-24  | Oy 25-36    | Izoh                          |
| ------------------ | -------- | -------- | --------- | --------- | ----------- | ----------------------------- |
| Server (VPS/Cloud) | $20/oy   | $50/oy   | $100/oy   | $300/oy   | $800/oy     | Hetzner → DigitalOcean → AWS  |
| AI API (jami)      | $5/oy    | $25/oy   | $100/oy   | $300/oy   | $700/oy     | Quyida tier bo'yicha taqsimot |
| Domain + SSL       | $15/yil  | —        | $15/yil   | $15/yil   | $15/yil     | .uz yoki .com                 |
| Marketing          | $0/oy    | $0/oy    | $50/oy    | $200/oy   | $500/oy     | Telegram ads, SEO, influencer |
| TTS API            | $0/oy    | $5/oy    | $20/oy    | $50/oy    | $100/oy     | Google TTS / Azure            |
| Developer          | $0\*     | $0\*     | $0\*      | $0\*      | $0-2000\*   | \*qarang: pastda              |
| **Jami (oylik)**   | **~$25** | **~$80** | **~$285** | **~$865** | **~$2,115** |                               |

> **\*Developer xarajat eslatmasi:** Hozir loyiha solo developer tomonidan rivojlantiriladi (Firdavs). Oy haqqi $0, lekin imkoniyat xarajati (opportunity cost) ~$400-800/oy (O'zbekiston developer o'rtacha maoshi). 25+ oyda jamoa kengaytirish rejalashtirilgan ($1,000-2,000/oy).

#### AI API Xarajat Taqsimoti (tier bo'yicha)

| AI Tier         | Model            | Narx/1K token   | Free user xarajat | Starter xarajat | Pro xarajat | Premium xarajat |
| --------------- | ---------------- | --------------- | ----------------- | --------------- | ----------- | --------------- |
| 🟢 Basic        | Groq llama-3.3   | ~$0 (free tier) | $0                | $0              | $0          | $0              |
| 🟡 Standard     | Gemini 2.0 Flash | ~$0.10/1K token | —                 | ~$0.005/user    | ~$0.02/user | ~$0.05/user     |
| 🔴 Professional | GPT-4o-mini/4o   | ~$0.50/1K token | —                 | —               | ~$0.03/user | ~$0.10/user     |

> **Strategiya:** Free userlar faqat Groq (tekin) ishlatadi → AI xarajat $0. Asosiy xarajat Pro/Premium userlarning Professional model tanlashida.

### 3.3 Break-Even Tahlili

```
Break-even = Oylik xarajat / O'rtacha ARPU

O'rtacha ARPU (taxminiy): (29,000 × 0.55) + (59,000 × 0.30) + (99,000 × 0.15) = 48,500 UZS ≈ $3.83

Month 1-3:  $25 / $3.83 = 7 to'lovchi user → Break-even
Month 7-12: $285 / $3.83 = 75 to'lovchi user → Break-even
Month 13-24: $865 / $3.83 = 226 to'lovchi user → Break-even
Month 25-36: $2,115 / $3.83 = 553 to'lovchi user → Break-even
```

> **Xulosa:** Dastlabki 6 oyda break-even 7-20 to'lovchi user bilan erishilishi mumkin. Bu juda qulay chunki server xarajati past ($20-50/oy).

### 3.4 Foyda Proyeksiyasi

| Oy  | MRR (USD) | Xarajat (USD) | Sof foyda (USD) | Marja    |
| --- | --------- | ------------- | --------------- | -------- |
| 1   | $21       | $25           | -$4             | ❌ Zarar |
| 3   | $189      | $25           | +$164           | 87%      |
| 6   | $905      | $80           | +$825           | 91%      |
| 12  | $3,549    | $285          | +$3,264         | 92%      |
| 18  | $11,249   | $865          | +$10,384        | 92%      |
| 24  | $31,494   | $865          | +$30,629        | 97%      |
| 36  | $72,767   | $2,115        | +$70,652        | 97%      |

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
- Feature gating (Free/Starter/Pro/Premium limitlar)
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
| ARPU (oylik)           | $2.50         | $3.83          | $4.50          | MRR / to'lovchi users    |
| Churn rate             | <10%          | <8%            | <5%            | Oylik bekor qilish       |
| NPS                    | 30+           | 40+            | 50+            | Net Promoter Score       |

### 9.2 Funnel Metriklar

```
Landing → Register:    30-40% (maqsad)
Register → Onboarding: 80-90%
Onboarding → 1st Word: 70-80%
1st Word → Day 7:      40-50%
Day 7 → Day 30:        50-60%
Day 30 → Premium:      5-8%
```

---

## O'ZGARISHLAR TARIXI

| Sana       | Kim      | Nima o'zgardi                                                                                                                             |
| ---------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-27 | AI Agent | Dastlabki versiya yaratildi                                                                                                               |
| 2026-02-27 | AI Audit | MRR qayta hisoblandi, server cost realga moslandi, raqobatchi SR tuzatildi, marketing byudjet qo'shildi, mahalliy raqobatchilar qo'shildi |
| 2026-02-28 | AI Agent | Monetizatsiya to'liq rewrite: tier nomlar (Starter/Pro/Premium), AI Model Selection, saxiy free tier, yillik rejalar, narx 99K Premium    |
