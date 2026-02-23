"""
Language detector module for smart import.

Detects whether a word/line is Uzbek, English, noise, title/header, etc.
"""

import re

# ═══════════════════════════════════════════════════════════════════
# UZBEK LANGUAGE DATA
# ═══════════════════════════════════════════════════════════════════

# O'zbekcha maxsus harflar (apostrof bilan yoziladigan)
UZBEK_SPECIFIC_CHARS = {"o'", "g'", "O'", "G'", "oʻ", "gʻ", "Oʻ", "Gʻ"}

# O'zbekcha suffiks lar
UZBEK_SUFFIXES = [
    "moq", "lik", "chi", "lar", "ning", "dan", "dagi",
    "ga", "ni", "qil", "lan", "lash", "ish", "uchi", "uvchi",
    "siz", "li", "cha", "kor", "xona", "zor",
    "gan", "kan", "gen", "kin", "gin", "qan",
    "yotgan", "ayotgan", "ilgan", "lgan",
    "dir", "gich", "vchi", "shi", "tir",
]

# O'zbekcha keng tarqalgan so'zlar (250+)
UZBEK_COMMON = {
    # Fe'llar
    "qilmoq", "bo'lmoq", "olmoq", "bermoq", "kelmoq", "ketmoq",
    "yozmoq", "o'qimoq", "bilmoq", "ko'rmoq", "aytmoq", "ishlamoq",
    "tushunmoq", "yaratmoq", "nishonlamoq", "sarflamoq", "tanlamoq",
    "to'plamoq", "yig'moq", "kutmoq", "qolmoq", "urmoq", "tutmoq",
    "baqirmoq", "jilmaymoq", "chalmoq", "jiringlamoq",

    # Otlar
    "maqsad", "xotira", "mashg'ulot", "savdo", "diagramma",
    "sinfdosh", "dars", "tushlik", "shamol", "varrak", "bulut",
    "jadval", "musobaqa", "loyiha", "qorin", "xalta", "narx",
    "konus", "ekran", "dori", "kayfiyat",

    # Sifatlar
    "mashhur", "qimmat", "arzon", "kuchli", "xavfsiz",
    "muvaffaqiyatli", "kechikkan", "hayajonlangan", "xavotirlangan",
    "voyaga", "yetgan", "kichkina", "qo'rqqan", "uyg'oq",

    # Ravishlar va bog'lovchilar
    "keyinroq", "aslida", "qayerdadir", "taxminan", "yakunda",
    "intiqlik", "sababli", "tufayli",

    # Ko'p ishlatiladigan
    "urg'ochi", "oziq", "ovqat", "mahsulot", "mahsulotlari",
    "farzand", "barmoq", "qo'lqop", "markasi",
    "tomoq", "yo'tal", "og'rig'i", "bosh",

    # Qo'shimcha
    "tayyorlangan", "takrorladingiz", "tanishtirmob",
    "dalda", "qo'llab", "quvvatlamoq",
    "sharafiga", "nomlangan", "pochtadan", "jo'natmoq",
    "o'ramoq", "g'amxo'rlik", "tuzalgan",
    "nishonlamoq", "sarflamob", "olib",

    # Grammatik so'zlar
    "tugallash", "boshlash", "bajarildi", "topshirish", "o'rganish",
    "joylashgan", "keltirilgan", "olingan", "yuborilgan", "qo'shilgan",
    "mavjud", "kerakli", "zaruriy", "muhim", "asosiy", "birinchi",
    "ikkinchi", "uchinchi", "katta", "kichik", "yangi", "eski",
    "yaxshi", "yomon", "boshqa", "har", "hammasi", "qanday",
    "nima", "qayerda", "qachon", "nega", "kim", "qancha",
    "uchun", "bilan", "orqali", "haqida", "sifatida", "bo'yicha",
    "keyin", "oldin", "hozir", "endi", "hali", "shu", "bu",
    "erkak", "bola", "qiz", "kishi", "odam",
    "narsa", "ish", "joy", "vaqt", "kun", "yil", "oy",
    "daraja", "miqdor", "holat", "sabab", "natija",
    "tanlang", "kiriting", "belgilang", "tekshiring", "saqlang",
    "ochiladi", "yopiladi", "ko'rsatiladi", "amalga", "oshiriladi",
    "tugadi", "boshlandi", "tayyor", "to'g'ri", "noto'g'ri",
    "mos", "emas", "yo'q", "ha", "balki", "albatta",
    "faqat", "hamma", "barch", "hech",
    "shart", "kerak", "lozim", "mumkin", "imkon",
    "quyidagi", "yuqoridagi", "qo'shimcha",

    # Tarjima so'zlari (often appear next to English words)
    "juda", "dam", "olmoq", "bosh", "og'rig'i",
    "qarsak", "ochko", "ball", "tutib",
    "haq", "oziq-ovqat", "qiz",
}

# ═══════════════════════════════════════════════════════════════════
# ENGLISH NOISE WORDS
# ═══════════════════════════════════════════════════════════════════

ENGLISH_NOISE = {
    "notebooklm", "gner", "bonmo", "tlae", "goge", "reroers",
    "gerdscc", "dwoented", "pelton", "wilk", "saodwich",
    "personel", "antions", "streetr", "lonson", "ste",
    "immu", "kangaro0",
}

# ═══════════════════════════════════════════════════════════════════
# TITLE / HEADER PATTERNS
# ═══════════════════════════════════════════════════════════════════

TITLE_PATTERNS = [
    r"^essential\s+english",
    r"^how\s+to\s+use",
    r"^the\s+method",
    r"^unit\s+\d+",
    r"^chapter\s+\d+",
    r"^section\s+\d+",
    r"^lesson\s+\d+",
    r"^part\s+\d+",
    r"^topic\s+\d+",
    r"^review\s+challenge",
    r"^keep\s+practicing",
    r"^great\s+job",
    r"^\d+\s+key\s+words",
    r"^source\s+material",
    r"^designed\s+for",
    r"^reading\s+starter",
    r"learners$",
    r"vocabulary$",
]


# ═══════════════════════════════════════════════════════════════════
# DETECTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════


def is_uzbek_word(word: str) -> bool:
    """Detect if a word is Uzbek based on common words, suffixes, and patterns."""
    w = word.lower().strip()
    if not w:
        return False

    # 1. Direct match in common Uzbek words
    if w in UZBEK_COMMON:
        return True

    # 2. Multi-word phrases — check each word
    if " " in w:
        parts = w.split()
        uzbek_parts = sum(1 for p in parts if p in UZBEK_COMMON)
        if uzbek_parts >= len(parts) * 0.5:
            return True

    # 3. Check Uzbek-specific character patterns (o', g')
    if "o'" in w or "g'" in w or "oʻ" in w or "gʻ" in w:
        return True

    # 4. Check Uzbek suffixes
    for suffix in UZBEK_SUFFIXES:
        if w.endswith(suffix) and len(w) > len(suffix) + 2:
            return True

    return False


def is_english_word(word: str) -> bool:
    """Check if word is a valid English word candidate (min 3 chars)."""
    w = word.strip().lower()

    # 1. Empty or too short (min 3 chars for meaningful vocabulary)
    if len(w) < 3:
        return False

    # 2. In noise list
    if w in ENGLISH_NOISE:
        return False

    # 3. Must be only ASCII letters + space + apostrophe + hyphen
    word_stripped = word.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z' \-]*[a-zA-Z]$", word_stripped):
        return False

    # 4. Must have at least 1 vowel
    if not re.search(r'[aeiouAEIOU]', word_stripped):
        return False

    # 5. Must not be Uzbek
    if is_uzbek_word(word):
        return False

    # 6. No digits
    if re.search(r'\d', word):
        return False

    return True


def has_uzbek_characters(text: str) -> bool:
    """Check if text contains Uzbek-specific character patterns."""
    t = text.lower()
    return "o'" in t or "g'" in t or "oʻ" in t or "gʻ" in t or "'" in t


def is_document_title(text: str) -> bool:
    """Detect if text is a document title or instructional header."""
    t = text.strip().lower()

    # Long phrases (6+ words) are likely titles
    if len(t.split()) > 6:
        return True

    # Check title patterns
    return any(re.search(p, t) for p in TITLE_PATTERNS)


def classify_line(line: str) -> str:
    """
    Classify a line of text into a category.

    Returns one of:
    - "english_word": English word
    - "uzbek_translation": Uzbek translation
    - "numbered_entry": "1. Female" format
    - "dash_pair": "Word – Translation"
    - "parenthesized": "(Translation)"
    - "section_header": "Unit 9: ..."
    - "title": Title/instruction
    - "noise": OCR noise, number, URL, etc.
    - "unknown": Unclassified
    """
    stripped = line.strip()
    if not stripped:
        return "noise"

    # Section header
    if re.match(r'^(Unit|Chapter|Section|Lesson|Part|Topic)\s+\d', stripped, re.IGNORECASE):
        return "section_header"

    # Title / instruction
    if is_document_title(stripped):
        return "title"

    # Numbered entry: "1. Female" or "1) Female"
    match = re.match(r'^\d+[\.\)]\s+(.+)$', stripped)
    if match:
        return "numbered_entry"

    # Dash pair: "Word – Translation"
    if re.search(r'\s*[–—\-]\s*', stripped) and re.search(r'[a-zA-Z]', stripped):
        parts = re.split(r'\s*[–—\-]\s*', stripped, maxsplit=1)
        if len(parts) == 2 and parts[0].strip() and parts[1].strip():
            return "dash_pair"

    # Parenthesized: "(Translation)"
    if re.match(r'^\(.+\)$', stripped):
        return "parenthesized"

    # Uzbek translation
    if is_uzbek_word(stripped) or has_uzbek_characters(stripped):
        return "uzbek_translation"

    # English word
    if is_english_word(stripped):
        return "english_word"

    # Pure noise: numbers, special chars
    if re.match(r'^[\d\s.,;:!?\-–—]+$', stripped):
        return "noise"

    # Very short non-English
    if len(stripped) <= 2:
        return "noise"

    return "unknown"
