"""
Smart Import — AI-First Architecture

Sprint 12.4: To'liq AI-first yondashuv.

Tamoyil: AI HAMMA ishni qiladi. Python faqat AI ga so'rov yuboradi
va natijani formatlaydi.

Pipeline:
1. Matnni minimal tozalash (URL, email olib tashlash)
2. AI Call #1: Matndan ingliz so'zlarini ajratish + tarjima + metadata
3. AI Call #2: Natijalarni validatsiya qilish (tarjima to'g'riligini tekshirish)
4. Natijani frontend ga qaytarish

Agar AI unavailable bo'lsa — oxirgi fallback (import_helpers) ishlatiladi.
"""

import csv
import io
import json
import logging
import re
from uuid import UUID

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# BACKWARD COMPATIBILITY — keep old names available for existing tests
# ═══════════════════════════════════════════════════════════════════
from .import_helpers.text_cleaner import clean_imported_text  # noqa: F401
from .import_helpers.pair_extractor import extract_word_pairs  # noqa: F401
from .import_helpers.language_detector import is_english_word, is_uzbek_word  # noqa: F401
from .import_helpers.translation_db import (  # noqa: F401
    COMMON_TRANSLATIONS,
    CEFR_ORDER,
    get_translation,
    estimate_cefr,
)

STOP_WORDS = {
    "the", "and", "for", "are", "but", "not", "you", "all", "can",
    "had", "her", "was", "one", "our", "out", "has", "his", "how",
    "its", "may", "new", "now", "old", "see", "way", "who", "did",
    "get", "let", "say", "she", "too", "use", "will", "with",
    "that", "this", "have", "from", "they", "been", "said", "each",
    "which", "their", "there", "were", "what", "when", "make",
    "like", "just", "over", "such", "take", "year", "them", "some",
    "than", "then", "very", "about", "would", "these", "other",
    "into", "more", "also", "could", "your", "after",
    "first", "made", "before", "many", "being", "where", "most",
    "much", "only", "through", "back", "long", "come", "good",
    "know", "still", "down", "should", "because", "right",
    "think", "does", "another", "well", "even", "here", "must",
    "same", "those", "every", "between", "own", "under", "last",
    "never", "great", "little", "while", "time", "people", "part",
    "help", "line", "turn", "move", "thing", "look", "place",
    "work", "play", "run", "want", "need", "went", "read",
    "hand", "high", "again", "next", "give", "name",
    "keep", "head", "start", "might", "show", "began", "life",
    "seem", "call", "world", "going", "point", "live", "left",
    "found", "both", "number", "day", "water", "word", "write",
    "open", "side", "told", "home", "small", "large", "end",
    "along", "house", "away", "ask", "men", "got",
    "off", "put", "three", "kind", "set", "few", "really",
    "something", "man", "came", "anything", "without", "always",
    "until", "used", "done", "enough", "though", "quite",
    "across", "once", "almost", "often", "since", "ever",
    "any", "shall", "able", "don", "having", "doing",
}


def detect_structured_format(text: str) -> bool:
    """Detect if text is in structured format (word – translation). Backward compat."""
    lines = text.strip().split('\n')
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return False
    numbered_lines = [l for l in non_empty if re.match(r'^\d+[\.\)]\s+[A-Za-z]', l.strip())]
    dash_lines = [l for l in non_empty if re.search(r'[A-Za-z]+\s*[–—\-:=]\s*\S+', l.strip())]
    if len(numbered_lines) >= 5 or len(dash_lines) >= 5:
        return True
    separator_count = 0
    for line in non_empty:
        if re.search(r'[–\-:=]', line) and re.search(r'[a-zA-Z]', line):
            separator_count += 1
    return separator_count / max(len(non_empty), 1) > 0.3


def parse_structured_text(text: str) -> list[dict]:
    """Parse structured text (word – translation pairs) into word list. Backward compat."""
    results = []
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^(Unit|Chapter|Section|Lesson|Part|Topic)\s+\d', line, re.IGNORECASE):
            continue
        if not re.search(r'[–—\-:=]', line):
            continue
        match = re.match(
            r'(?:\d+[\.\)]\s*)?([A-Za-z][A-Za-z\s\'\-]*(?:\([^)]*\))?[A-Za-z\s\'\-]*?)\s*[–—\-:=]\s*(.+)',
            line
        )
        if match:
            word_raw = match.group(1).strip()
            translation = match.group(2).strip()
            paren_match = re.search(r'\(([^)]+)\)', word_raw)
            paren_note = ""
            if paren_match:
                paren_note = paren_match.group(1).strip()
                word_clean = re.sub(r'\s*\([^)]*\)', '', word_raw).strip()
            else:
                word_clean = word_raw.strip()
            first_token = word_clean.split()[0] if word_clean.split() else ""
            if first_token and is_english_word(first_token):
                entry = {
                    'word': word_clean,
                    'translation': translation,
                }
                if paren_note:
                    entry['notes'] = paren_note
                results.append(entry)
    return results


class AnalyzeTextUseCase:
    """
    AI-First text analysis — har qanday formatdagi matndan ingliz so'zlarini ajratish.

    Sprint 12.4: To'liq qayta yozildi.

    Qo'llab-quvvatlanadigan formatlar (AI tufayli CHEKLANMAGAN):
    - "word - translation" lug'at formati
    - "1. word / translation" raqamli format
    - PDF dan ko'chirilgan matn (noise, metadata bilan)
    - Oddiy ingliz matni (paragraph)
    - Aralash matn (ingliz + o'zbek)
    - Darslik sahifalari
    - Har qanday boshqa format
    """

    def __init__(self, word_repo, ai_provider=None, **kwargs):
        """
        Initialize AnalyzeTextUseCase.

        Args:
            word_repo: Word repository for user library checks.
            ai_provider: AI provider for text analysis.
            **kwargs: Backward-compatible params (user_repo, prompt_template, language_map).
        """
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        # Kept for backward compat — no longer used in AI-first pipeline
        self.user_repo = kwargs.get('user_repo')
        self.prompt_template = kwargs.get('prompt_template', '')
        self.language_map = kwargs.get('language_map', {})

    def execute(self, user_id, text: str, max_words: int = 100) -> dict:
        user_id_val = UUID(str(user_id))

        if not text or not text.strip():
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is required.")

        if len(text) > 5000:
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is too long. Maximum 5000 characters allowed.")

        # Minimal tozalash — faqat URL va email
        cleaned = self._minimal_clean(text)

        if not cleaned or len(cleaned.strip()) < 3:
            return self._empty_result()

        # AI bilan tahlil
        if self.ai_provider and self._provider_is_available():
            try:
                suggestions = self._full_ai_pipeline(cleaned, max_words)
                parse_mode = "ai"
            except Exception as e:
                logger.error(f"AI import pipeline failed: {e}", exc_info=True)
                suggestions = self._last_resort_fallback(cleaned, max_words)
                parse_mode = "fallback"
        else:
            logger.warning("AI provider not available for import")
            suggestions = self._last_resort_fallback(cleaned, max_words)
            parse_mode = "fallback"

        # User library check
        existing_words = self._get_user_words(user_id_val)
        for s in suggestions:
            s["in_user_library"] = s["word"].lower().strip() in existing_words

        already_in = sum(1 for s in suggestions if s["in_user_library"])

        return {
            "suggestions": suggestions,
            "parse_mode": parse_mode,
            "total_found": len(suggestions),
            "already_in_library": already_in,
            "new_words": len(suggestions) - already_in,
            "text_difficulty": self._calc_difficulty(suggestions),
            "ai_used": parse_mode == "ai",
        }

    # ═════════════════════════════════════════════════════════════════
    # MINIMAL CLEANING
    # ═════════════════════════════════════════════════════════════════

    def _minimal_clean(self, text: str) -> str:
        """Faqat texnik noise olib tashlash. Matn mazmuniga tegmaydi."""
        if not text:
            return ""
        # URL va email
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'www\.\S+', '', text)
        text = re.sub(r'\S+@\S+\.\S+', '', text)
        # Unicode BOM va maxsus belgilar
        text = text.replace('\ufeff', '').replace('\u200b', '')
        # Ortiqcha bo'sh qatorlar
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        return text.strip()

    # ═════════════════════════════════════════════════════════════════
    # AI PIPELINE (2 bosqich)
    # ═════════════════════════════════════════════════════════════════

    def _full_ai_pipeline(self, text: str, max_words: int) -> list[dict]:
        """
        2 bosqichli AI pipeline:

        BOSQICH 1: Matndan so'zlarni ajratish + tarjima
        BOSQICH 2: Tarjimalarni validatsiya va tuzatish
        """

        # ═══ BOSQICH 1: AJRATISH ═══
        raw_words = self._ai_extract(text, max_words)

        if not raw_words:
            logger.warning("AI extraction returned empty, trying with simplified prompt")
            raw_words = self._ai_extract_simple(text, max_words)

        if not raw_words:
            raise ValueError("AI could not extract any words")

        # ═══ BOSQICH 2: VALIDATSIYA ═══
        validated = self._ai_validate(raw_words)

        return validated

    def _ai_extract(self, text: str, max_words: int) -> list[dict]:
        """AI Call #1 — matndan ingliz so'zlarini ajratish."""

        # Matn juda uzun bo'lsa — qisqartirish
        if len(text) > 6000:
            text = text[:6000]

        prompt = self._build_extraction_prompt(text, max_words)

        try:
            result = self.ai_provider.generate_json(prompt)
        except Exception:
            # JSON parse fail bo'lsa — text sifatida olish va o'zimiz parse qilish
            raw = self.ai_provider.generate_text(prompt)
            result = self._extract_json_from_text(raw)

        if not isinstance(result, list):
            if isinstance(result, dict) and "words" in result:
                result = result["words"]
            else:
                raise ValueError(f"AI returned unexpected format: {type(result)}")

        # Dublikatlarni olib tashlash
        seen = set()
        unique = []
        for item in result:
            if not isinstance(item, dict) or "word" not in item:
                continue
            w = item["word"].lower().strip()
            if w and w not in seen and len(w) >= 2:
                seen.add(w)
                unique.append(item)

        return unique[:max_words]

    def _build_extraction_prompt(self, text: str, max_words: int) -> str:
        return f"""You are an expert English vocabulary extractor for language learners.

I will give you a text. Your job is to extract ENGLISH vocabulary words from it.

IMPORTANT RULES:

1. WHAT TO EXTRACT:
   - English words and phrases useful for language learning
   - Phrasal verbs as single items: "look after", "give up", "pick up"
   - Idioms as single items: "sore throat", "home run", "in fact"
   - Common collocations: "make a decision", "take a break"

2. WHAT TO SKIP (DO NOT include these):
   - Words that are NOT English (Uzbek, Russian, or any other language)
   - Document metadata: page numbers, dates, times, prices
   - Brand names, platform names, author names
   - Section headers like "Unit 5", "Chapter 3" (but extract words FROM those sections)
   - OCR garbage/corrupted text (random letter sequences that aren't real words)
   - Very common English function words used as structural text: "the", "a", "is", "are", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with" (UNLESS they are part of a phrasal verb or idiom)
   - Instructions like "How to use", "Click here", "Keep practicing"

3. TRANSLATION HANDLING — THIS IS CRITICAL:
   - If the user's text ALREADY contains translations (e.g., "grip — ushlab olish" or "Female / Urg'ochi"), USE the user's translation — do NOT replace it
   - BUT if the user's translation is OBVIOUSLY WRONG (e.g., "grip — koptok" where "koptok" means "ball" but "grip" means "ushlab olish"), then CORRECT the translation and set "translation_corrected" to true
   - If NO translation is provided in the text, provide an Uzbek translation yourself
   - Translations must be in UZBEK language

4. FOR EACH WORD provide:
   - "word": the English word/phrase (lowercase)
   - "translation": Uzbek translation
   - "translation_source": "user" if taken from user's text, "ai" if you provided it, "corrected" if you fixed user's wrong translation
   - "original_user_translation": only if translation_source is "corrected" — what the user originally wrote
   - "pronunciation": IPA format like /ˈæp.əl/
   - "definition": short English definition (max 15 words)
   - "example": simple example sentence using this word (max 15 words, A2-B1 level)
   - "part_of_speech": one of: noun, verb, adjective, adverb, preposition, pronoun, phrase, phrasal_verb, idiom
   - "cefr": one of: A1, A2, B1, B2, C1, C2

5. SORTING: Sort by CEFR level — A1 first, C2 last. Within same level, alphabetical.

6. MAXIMUM: Return at most {max_words} words.

Respond with a JSON array only. No markdown code blocks, no explanation, no extra text.

TEXT TO ANALYZE:
\"\"\"
{text}
\"\"\"

JSON ARRAY:"""

    def _ai_extract_simple(self, text: str, max_words: int) -> list[dict]:
        """Soddalashtirilgan prompt — agar birinchisi fail bo'lsa."""

        prompt = f"""Extract English vocabulary words from this text.
For each word give: word, uzbek translation, pronunciation (IPA), CEFR level (A1-C2).
Skip non-English words, headers, metadata, garbage text.
Return JSON array: [{{"word":"...","translation":"...","pronunciation":"...","cefr":"..."}}]
Max {max_words} words.

Text:
{text[:3000]}

JSON:"""

        try:
            result = self.ai_provider.generate_json(prompt)
            if isinstance(result, list):
                return result
        except Exception:
            raw = self.ai_provider.generate_text(prompt)
            return self._extract_json_from_text(raw)

        return []

    # ═════════════════════════════════════════════════════════════════
    # AI VALIDATION (BOSQICH 2)
    # ═════════════════════════════════════════════════════════════════

    def _ai_validate(self, words: list[dict]) -> list[dict]:
        """
        AI Call #2 — tarjimalar to'g'riligini tekshirish.

        Nima uchun kerak:
        - AI #1 xato tarjima bergan bo'lishi mumkin
        - Foydalanuvchi matnida xato tarjima bo'lishi mumkin
        - Ba'zi so'zlar aslida ingliz emas (AI #1 xato ajratgan)
        """

        if not words or len(words) == 0:
            return []

        # 30 tadan ko'p bo'lsa — batch qilib yuboramiz
        if len(words) <= 30:
            return self._validate_batch(words)
        else:
            result = []
            for i in range(0, len(words), 30):
                batch = words[i:i + 30]
                validated = self._validate_batch(batch)
                result.extend(validated)
            return result

    def _validate_batch(self, words: list[dict]) -> list[dict]:
        """Bir batch so'zlarni validatsiya qilish."""

        word_list = "\n".join(
            f"- {w.get('word', '?')}: {w.get('translation', '?')}"
            for w in words
        )

        prompt = f"""You are an English-Uzbek translation validator.

Check each word-translation pair below. For each one:
1. Is the "word" actually an English word? (not Uzbek, not gibberish, not a name)
2. Is the Uzbek translation correct?
3. If translation is wrong, what is the correct one?

Word list:
{word_list}

For each word respond:
- "word": the English word
- "is_valid_english": true/false (is this actually an English vocabulary word?)
- "translation_correct": true/false
- "correct_translation": the correct Uzbek translation (whether original was right or wrong)
- "cefr": A1/A2/B1/B2/C1/C2

Return JSON array only. No explanation.
JSON:"""

        try:
            validation = self.ai_provider.generate_json(prompt)
        except Exception:
            try:
                raw = self.ai_provider.generate_text(prompt)
                validation = self._extract_json_from_text(raw)
            except Exception as e:
                logger.warning(f"Validation AI call failed: {e}")
                # Validatsiya fail — original larni qaytarish
                return self._format_suggestions(words)

        if not isinstance(validation, list):
            return self._format_suggestions(words)

        # Validation natijasini original words bilan birlashtirish
        val_map = {}
        for v in validation:
            if isinstance(v, dict) and "word" in v:
                val_map[v["word"].lower().strip()] = v

        result = []
        for w in words:
            word_key = w.get("word", "").lower().strip()
            val = val_map.get(word_key, {})

            # Agar valid English emas — skip
            if val.get("is_valid_english") is False:
                logger.debug(f"Skipping non-English word: {word_key}")
                continue

            # Tarjima tuzatish
            if val.get("correct_translation"):
                final_translation = val["correct_translation"]
            else:
                final_translation = w.get("translation", "")

            # CEFR — validation dan yoki original dan
            cefr = val.get("cefr") or w.get("cefr", "A2")

            result.append({
                "word": w.get("word", "").strip(),
                "translation": final_translation,
                "pronunciation": w.get("pronunciation", ""),
                "definition": w.get("definition", ""),
                "example_sentence": w.get("example", ""),
                "part_of_speech": w.get("part_of_speech", ""),
                "difficulty": cefr,
                "translation_source": w.get("translation_source", "ai"),
                "original_user_translation": w.get("original_user_translation", ""),
            })

        return result

    # ═════════════════════════════════════════════════════════════════
    # JSON EXTRACTION HELPER
    # ═════════════════════════════════════════════════════════════════

    def _extract_json_from_text(self, text: str) -> list:
        """AI response dan JSON array ajratish."""
        if not text:
            return []

        # Markdown code block ichidagi JSON
        md_match = re.search(r'```(?:json)?\s*(\[[\s\S]*?\])\s*```', text)
        if md_match:
            try:
                return json.loads(md_match.group(1))
            except json.JSONDecodeError:
                pass

        # To'g'ridan-to'g'ri JSON array
        arr_match = re.search(r'(\[[\s\S]*\])', text)
        if arr_match:
            try:
                return json.loads(arr_match.group(1))
            except json.JSONDecodeError:
                pass

        # JSON object ichida "words" key
        obj_match = re.search(r'(\{[\s\S]*\})', text)
        if obj_match:
            try:
                obj = json.loads(obj_match.group(1))
                if isinstance(obj, dict):
                    for key in ["words", "vocabulary", "results", "data"]:
                        if key in obj and isinstance(obj[key], list):
                            return obj[key]
            except json.JSONDecodeError:
                pass

        return []

    # ═════════════════════════════════════════════════════════════════
    # YORDAMCHI METODLAR
    # ═════════════════════════════════════════════════════════════════

    def _format_suggestions(self, words: list[dict]) -> list[dict]:
        """Raw AI natijasini frontend format ga keltirish."""
        return [
            {
                "word": w.get("word", "").strip(),
                "translation": w.get("translation", ""),
                "pronunciation": w.get("pronunciation", ""),
                "definition": w.get("definition", ""),
                "example_sentence": w.get("example", ""),
                "part_of_speech": w.get("part_of_speech", ""),
                "difficulty": w.get("cefr", "A2"),
                "translation_source": w.get("translation_source", "ai"),
                "original_user_translation": w.get("original_user_translation", ""),
            }
            for w in words
            if w.get("word", "").strip()
        ]

    def _provider_is_available(self) -> bool:
        """Check if AI provider is available (with safe fallback)."""
        try:
            return self.ai_provider.is_available()
        except Exception:
            return False

    def _get_user_words(self, user_id) -> set[str]:
        """Foydalanuvchining mavjud so'zlari."""
        try:
            existing_words, _ = self.word_repo.get_all_by_user(
                user_id=user_id, page=1, page_size=10000,
            )
            return {w.original_word.lower() for w in existing_words}
        except Exception:
            try:
                words = self.word_repo.get_user_word_list(user_id)
                return {w.lower().strip() for w in words}
            except Exception:
                try:
                    words = self.word_repo.get_words(user_id)
                    return {
                        w.original_word.lower().strip()
                        for w in words
                        if hasattr(w, 'original_word')
                    }
                except Exception:
                    return set()

    def _calc_difficulty(self, suggestions: list[dict]) -> str:
        """Matn qiyinligini hisoblash."""
        if not suggestions:
            return "A1"
        levels = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
        total = 0
        count = 0
        for s in suggestions:
            diff = s.get("difficulty", "A2")
            if diff in levels:
                total += levels[diff]
                count += 1
        if count == 0:
            return "A1"
        avg = total / count
        for level, val in sorted(levels.items(), key=lambda x: x[1]):
            if avg <= val + 0.5:
                return level
        return "C2"

    def _empty_result(self) -> dict:
        return {
            "suggestions": [],
            "parse_mode": "empty",
            "total_found": 0,
            "already_in_library": 0,
            "new_words": 0,
            "text_difficulty": "A1",
            "ai_used": False,
        }

    def _last_resort_fallback(self, text: str, max_words: int) -> list[dict]:
        """
        AI butunlay ishlamasa — import_helpers dan foydalanish.
        Bu OXIRGI chora. Ideal holatda hech qachon chaqirilmasligi kerak.
        """
        try:
            cleaned = clean_imported_text(text)
            pairs = extract_word_pairs(cleaned)

            suggestions = []
            seen = set()
            for pair in pairs:
                word = pair.get("word", "").strip()
                if not word or word.lower() in seen:
                    continue
                seen.add(word.lower())

                translation = pair.get("translation", "")
                if not translation:
                    translation = get_translation(word) or ""

                suggestions.append({
                    "word": word,
                    "translation": translation,
                    "pronunciation": "",
                    "definition": "",
                    "example_sentence": "",
                    "part_of_speech": "",
                    "difficulty": estimate_cefr(word),
                    "translation_source": "fallback",
                    "original_user_translation": "",
                })

            return suggestions[:max_words]
        except Exception as e:
            logger.error(f"Last resort fallback also failed: {e}")
            return []


class ImportWordsUseCase:
    """Bulk import selected words into user's word bank."""

    def __init__(self, word_repo, enrich_task=None, enrichment_enabled: bool = True):
        self.word_repo = word_repo
        self.enrich_task = enrich_task
        self.enrichment_enabled = enrichment_enabled

    def execute(self, user_id, selected_words: list[dict]) -> dict:
        user_id = UUID(str(user_id))
        added = 0
        skipped = 0

        for word_data in selected_words:
            original_word = word_data.get("original_word", "").strip().lower()
            if not original_word:
                skipped += 1
                continue

            if self.word_repo.exists(original_word, user_id):
                skipped += 1
                continue

            try:
                word = self.word_repo.create(
                    user_id=user_id,
                    original_word=original_word,
                    translation=word_data.get("translation", ""),
                    difficulty_level=word_data.get("difficulty_level", "medium"),
                )
                added += 1

                # Queue enrichment
                if self.enrichment_enabled and self.enrich_task:
                    try:
                        self.enrich_task(str(word.id), str(user_id))
                    except Exception as e:
                        logger.warning(f"Failed to queue enrichment for {original_word}: {e}")

            except Exception as e:
                logger.warning(f"Failed to import word '{original_word}': {e}")
                skipped += 1

        return {"added": added, "skipped": skipped}


class ValidateCSVUseCase:
    """Validate and preview a CSV file before import."""

    MAX_ROWS = 500
    REQUIRED_HEADER = "word"
    KNOWN_HEADERS = {"word", "translation", "difficulty", "category", "notes"}

    def execute(self, file_content: str) -> dict:
        """
        Parse CSV, detect headers, return preview + errors.
        """
        errors = []
        reader = csv.DictReader(io.StringIO(file_content))

        if not reader.fieldnames:
            return {
                "headers": [],
                "preview": [],
                "total_rows": 0,
                "valid_rows": 0,
                "errors": ["No headers found in CSV file."],
                "has_translation": False,
                "has_difficulty": False,
                "has_category": False,
            }

        # Normalize header names
        headers = [h.strip().lower() for h in reader.fieldnames]

        if self.REQUIRED_HEADER not in headers:
            return {
                "headers": headers,
                "preview": [],
                "total_rows": 0,
                "valid_rows": 0,
                "errors": ["CSV must have a 'word' column."],
                "has_translation": False,
                "has_difficulty": False,
                "has_category": False,
            }

        has_translation = "translation" in headers
        has_difficulty = "difficulty" in headers
        has_category = "category" in headers

        rows = []
        preview = []
        valid_count = 0

        for i, row in enumerate(reader, start=2):  # start=2 since row 1 is header
            if i - 1 > self.MAX_ROWS:
                errors.append(f"File has more than {self.MAX_ROWS} rows. Only first {self.MAX_ROWS} will be imported.")
                break

            # Normalize keys
            normalized = {}
            for k, v in row.items():
                normalized[k.strip().lower()] = (v or "").strip()

            word = normalized.get("word", "").strip()
            if not word:
                errors.append(f"Row {i}: empty word.")
                continue
            if len(word) > 100:
                errors.append(f"Row {i}: word too long (max 100 chars).")
                continue

            valid_count += 1
            rows.append(normalized)

            if len(preview) < 10:
                preview.append(normalized)

        return {
            "headers": headers,
            "preview": preview,
            "total_rows": len(rows) + len([e for e in errors if "Row" in e]),
            "valid_rows": valid_count,
            "errors": errors,
            "has_translation": has_translation,
            "has_difficulty": has_difficulty,
            "has_category": has_category,
        }


class CSVImportUseCase:
    """Import words from CSV file into user's word bank."""

    MAX_ROWS = 500
    VALID_DIFFICULTIES = {"easy", "medium", "hard"}

    def __init__(self, word_repo, enrich_task=None, enrichment_enabled: bool = True):
        self.word_repo = word_repo
        self.enrich_task = enrich_task
        self.enrichment_enabled = enrichment_enabled

    def execute(self, user_id, file_content: str) -> dict:
        """
        Parse CSV and import words.
        """
        user_id = UUID(str(user_id))
        errors = []
        imported = 0
        skipped_duplicate = 0
        skipped_invalid = 0
        categories_created = []

        reader = csv.DictReader(io.StringIO(file_content))
        if not reader.fieldnames:
            return {
                "total_in_file": 0,
                "imported": 0,
                "skipped_duplicate": 0,
                "skipped_invalid": 0,
                "errors": ["No headers found in CSV file."],
                "categories_created": [],
            }

        headers = [h.strip().lower() for h in reader.fieldnames]
        has_translation = "translation" in headers
        has_difficulty = "difficulty" in headers
        has_category = "category" in headers

        rows = list(reader)
        total_in_file = len(rows)

        if total_in_file > self.MAX_ROWS:
            return {
                "total_in_file": total_in_file,
                "imported": 0,
                "skipped_duplicate": 0,
                "skipped_invalid": 0,
                "errors": [f"Too many rows ({total_in_file}). Maximum is {self.MAX_ROWS}."],
                "categories_created": [],
            }

        for i, row in enumerate(rows, start=2):
            # Normalize keys
            normalized = {}
            for k, v in row.items():
                normalized[k.strip().lower()] = (v or "").strip()

            word = normalized.get("word", "").strip().lower()
            if not word:
                errors.append(f"Row {i}: empty word.")
                skipped_invalid += 1
                continue
            if len(word) > 100:
                errors.append(f"Row {i}: word too long.")
                skipped_invalid += 1
                continue

            # Check duplicate
            if self.word_repo.exists(word, user_id):
                skipped_duplicate += 1
                continue

            # Prepare word data
            translation = normalized.get("translation", "") if has_translation else ""
            difficulty = normalized.get("difficulty", "medium").lower() if has_difficulty else "medium"
            if difficulty not in self.VALID_DIFFICULTIES:
                difficulty = "medium"
            notes = normalized.get("notes", "")

            # Category handling
            category_id = None
            if has_category and normalized.get("category"):
                cat_name = normalized["category"].strip()
                if cat_name:
                    try:
                        from apps.words.infrastructure.models import WordCategory
                        cat, created = WordCategory.objects.get_or_create(
                            user_id=user_id,
                            name=cat_name,
                            defaults={"color": "#6C5CE7", "icon": "folder"},
                        )
                        category_id = cat.id
                        if created and cat_name not in categories_created:
                            categories_created.append(cat_name)
                    except Exception:
                        pass

            try:
                create_kwargs = {
                    "original_word": word,
                    "translation": translation,
                    "difficulty_level": difficulty,
                    "notes": notes,
                }
                if category_id:
                    create_kwargs["category_id"] = category_id

                new_word = self.word_repo.create(user_id=user_id, **create_kwargs)
                imported += 1

                # Queue enrichment
                if self.enrichment_enabled and self.enrich_task:
                    try:
                        self.enrich_task(str(new_word.id), str(user_id))
                    except Exception as e:
                        logger.warning(f"Failed to queue enrichment for {word}: {e}")

            except Exception as e:
                logger.warning(f"Failed to import word '{word}': {e}")
                skipped_duplicate += 1

        return {
            "total_in_file": total_in_file,
            "imported": imported,
            "skipped_duplicate": skipped_duplicate,
            "skipped_invalid": skipped_invalid,
            "errors": errors,
            "categories_created": categories_created,
        }
