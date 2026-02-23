"""
Smart import use cases: text analysis, word import, and CSV import.

Sprint 12.2: Fully rewritten AnalyzeTextUseCase with import_helpers pipeline.
"""

import csv
import io
import logging
import re
from collections import Counter
from uuid import UUID

from .import_helpers.text_cleaner import clean_imported_text
from .import_helpers.pair_extractor import extract_word_pairs
from .import_helpers.language_detector import is_english_word, is_uzbek_word
from .import_helpers.translation_db import (
    COMMON_TRANSLATIONS,
    CEFR_ORDER,
    get_translation,
    estimate_cefr,
)

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# BACKWARD COMPATIBILITY — keep old names available for existing tests
# ═══════════════════════════════════════════════════════════════════

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
    """Detect if text is in structured format (word – translation)."""
    lines = text.strip().split('\n')
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return False

    # Pattern 1: "number. word" lines
    numbered_lines = [l for l in non_empty if re.match(r'^\d+[\.\)]\s+[A-Za-z]', l.strip())]

    # Pattern 2: "word – translation" or "word - translation" lines
    dash_lines = [l for l in non_empty if re.search(r'[A-Za-z]+\s*[–—\-:=]\s*\S+', l.strip())]

    # If 5+ structured lines → structured
    if len(numbered_lines) >= 5 or len(dash_lines) >= 5:
        return True

    # Original heuristic: separator ratio
    separator_count = 0
    for line in non_empty:
        if re.search(r'[–\-:=]', line) and re.search(r'[a-zA-Z]', line):
            separator_count += 1
    return separator_count / max(len(non_empty), 1) > 0.3


def parse_structured_text(text: str) -> list[dict]:
    """Parse structured text (word – translation pairs) into word list.

    Handles multi-unit texts like:
        Unit 6: Our Favorite Hobbies
        1. Clap – qarsak chalmoq
        2. Choose (chose) – tanlamoq
        Unit 7: ...
    """
    results = []
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip headers: Unit X, Chapter X, Section X, Lesson X, Part X, Topic X
        if re.match(r'^(Unit|Chapter|Section|Lesson|Part|Topic)\s+\d', line, re.IGNORECASE):
            continue
        # Skip lines that are pure titles (no separator and no number prefix)
        if not re.search(r'[–—\-:=]', line):
            continue
        # Pattern: optional number + English word(s) + separator + translation
        match = re.match(
            r'(?:\d+[\.\)]\s*)?([A-Za-z][A-Za-z\s\'\-]*(?:\([^)]*\))?[A-Za-z\s\'\-]*?)\s*[–—\-:=]\s*(.+)',
            line
        )
        if match:
            word_raw = match.group(1).strip()
            translation = match.group(2).strip()

            # Extract parenthetical forms: "Choose (chose)" -> word="Choose", keep note
            paren_match = re.search(r'\(([^)]+)\)', word_raw)
            paren_note = ""
            if paren_match:
                paren_note = paren_match.group(1).strip()
                word_clean = re.sub(r'\s*\([^)]*\)', '', word_raw).strip()
            else:
                word_clean = word_raw.strip()

            # Make sure the first real token is English
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


# AI PROMPT for structured format enrichment
STRUCTURED_ENRICHMENT_PROMPT = """For each English word below, provide additional learning information.
The learner speaks {native_language} at {proficiency_level} level.

Words: {word_list}

For EACH word respond with:
1. part_of_speech (noun/verb/adjective/adverb/phrase/other)
2. difficulty (CEFR level: A1, A2, B1, B2, C1, C2)
3. definition (brief English definition, appropriate for the learner's level)
4. example (one natural example sentence)
5. pronunciation (IPA format)

Sort output by difficulty: A1 first → C2 last

RESPOND ONLY with valid JSON:
{{
  "words": [
    {{
      "word": "clap",
      "part_of_speech": "verb",
      "difficulty": "A1",
      "definition": "to hit your hands together to make a sound",
      "example": "The audience clapped after the performance.",
      "pronunciation": "/klæp/"
    }}
  ]
}}"""


# AI PROMPT for smart import pair enrichment
SMART_IMPORT_ENRICHMENT_PROMPT = """You are an English vocabulary expert. I have these English words with Uzbek translations:

{word_pairs}

For each word, provide:
1. pronunciation (IPA format, e.g. /ˈfɪʃ/)
2. definition (short, in English, max 15 words)
3. example_sentence (simple, A2-B1 level, max 12 words)
4. part_of_speech (noun/verb/adjective/adverb/phrase/idiom)
5. cefr (A1/A2/B1/B2/C1/C2)
6. If translation is missing or "?", provide Uzbek translation

Respond in JSON array format:
[{{"word": "...", "pronunciation": "...", "definition": "...", "example": "...", "part_of_speech": "...", "cefr": "...", "translation": "..."}}]

IMPORTANT: Return ONLY the JSON array, no other text."""


class AnalyzeTextUseCase:
    """Analyze text and suggest unknown words for the user.

    Sprint 12.2: New pipeline-based approach:
    1. Text cleaning (remove noise, metadata, instructions)
    2. Pair extraction (structured parsing with multiple strategies)
    3. AI enrichment (if AI available)
    4. Fallback enrichment (if AI unavailable)
    5. User library check
    6. Response formatting

    Also supports legacy modes for backward compatibility:
    - STRUCTURED: word – translation pairs (dash-separated)
    - PLAIN ENGLISH: Extract vocabulary from English text via AI
    - MIXED: Mixed language text, extract only English words
    """

    def __init__(self, word_repo, ai_provider=None, user_repo=None,
                 prompt_template: str = "", language_map: dict = None):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map or {}

    def execute(self, user_id, text: str, max_words: int = 100) -> dict:
        user_id = UUID(str(user_id))

        if not text or not text.strip():
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is required.")

        if len(text) > 5000:
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is too long. Maximum 5000 characters allowed.")

        # ── STEP 1: Get user's existing words ───────────────────────
        existing_words = self._get_user_words(user_id)

        # ── STEP 2: Try new smart pipeline first ────────────────────
        # Clean the text
        cleaned = clean_imported_text(text)

        # Extract word-translation pairs
        pairs = extract_word_pairs(cleaned)

        if pairs:
            # Smart pipeline found pairs — use new flow
            return self._handle_smart_pipeline(
                pairs, existing_words, user_id, max_words
            )

        # ── STEP 3: Fallback — try legacy dash-separated format ─────
        if detect_structured_format(text):
            native_lang, proficiency = self._get_user_lang_info(user_id)
            return self._handle_structured(
                text, existing_words, native_lang, proficiency, max_words
            )

        # ── STEP 4: Fallback — try plain English AI extraction ──────
        native_lang, proficiency = self._get_user_lang_info(user_id)
        if self._is_likely_english_text(text):
            return self._handle_plain_english(
                text, existing_words, native_lang, proficiency, max_words
            )

        # ── STEP 5: Fallback — mixed text extraction ────────────────
        return self._handle_mixed(
            text, existing_words, native_lang, proficiency, max_words
        )

    # ═════════════════════════════════════════════════════════════════
    # NEW SMART PIPELINE (Sprint 12.2)
    # ═════════════════════════════════════════════════════════════════

    def _handle_smart_pipeline(self, pairs, known_words_set, user_id, max_words):
        """New smart import pipeline using import_helpers modules."""

        # Try AI enrichment
        parse_mode = "structured"
        ai_used = False

        if self.ai_provider:
            try:
                pairs = self._enrich_with_ai(pairs)
                parse_mode = "ai"
                ai_used = True
            except Exception as e:
                logger.warning(f"AI enrichment failed, using fallback: {e}")
                pairs = self._enrich_with_fallback(pairs)
        else:
            pairs = self._enrich_with_fallback(pairs)

        # Build suggestions
        suggestions = []
        already_in_library = 0

        for pair in pairs[:max_words]:
            word = pair["word"]
            word_lower = word.lower().strip()
            in_library = word_lower in known_words_set

            if in_library:
                already_in_library += 1

            suggestions.append({
                "word": word,
                "translation": pair.get("translation", ""),
                "pronunciation": pair.get("pronunciation", ""),
                "definition": pair.get("definition", ""),
                "context_sentence": pair.get("example", ""),
                "example_sentence": pair.get("example", ""),
                "part_of_speech": pair.get("part_of_speech", ""),
                "difficulty": pair.get("cefr", estimate_cefr(word)),
                "reason": "Smart import",
                "in_user_library": in_library,
            })

        # Sort by CEFR difficulty (A1 first)
        suggestions.sort(
            key=lambda x: CEFR_ORDER.get(x.get("difficulty", "B1"), 3),
            reverse=True
        )

        return {
            "suggestions": suggestions,
            "parse_mode": parse_mode,
            "total_found": len(suggestions),
            "already_in_library": already_in_library,
            "new_words": len(suggestions) - already_in_library,
            "text_difficulty": self._estimate_text_difficulty(suggestions),
            "ai_used": ai_used,
        }

    def _enrich_with_ai(self, pairs: list[dict]) -> list[dict]:
        """Enrich word pairs using AI — pronunciation, definition, example."""

        word_pairs_text = "\n".join(
            f'- {p["word"]}: {p.get("translation", "?")}'
            for p in pairs
        )

        prompt = SMART_IMPORT_ENRICHMENT_PROMPT.format(
            word_pairs=word_pairs_text
        )

        result = self.ai_provider.generate_json(prompt, max_tokens=3000, temperature=0.3)

        if isinstance(result, list):
            ai_map = {
                item["word"].lower(): item
                for item in result
                if isinstance(item, dict) and "word" in item
            }
            for pair in pairs:
                ai_data = ai_map.get(pair["word"].lower(), {})
                pair["pronunciation"] = ai_data.get("pronunciation", "")
                pair["definition"] = ai_data.get("definition", "")
                pair["example"] = ai_data.get("example", ai_data.get("example_sentence", ""))
                pair["part_of_speech"] = ai_data.get("part_of_speech", "")
                pair["cefr"] = ai_data.get("cefr", estimate_cefr(pair["word"]))
                if not pair.get("translation") or pair["translation"] == "?":
                    pair["translation"] = ai_data.get("translation", "")

        return pairs

    def _enrich_with_fallback(self, pairs: list[dict]) -> list[dict]:
        """Enrich without AI — use translation_db and heuristics."""

        for pair in pairs:
            word = pair["word"]

            # Translation from DB
            if not pair.get("translation"):
                pair["translation"] = get_translation(word) or ""

            # CEFR estimation
            pair["cefr"] = estimate_cefr(word)

            # Empty fields for AI-only data
            pair.setdefault("pronunciation", "")
            pair.setdefault("definition", "")
            pair.setdefault("example", "")
            pair.setdefault("part_of_speech", "")

        return pairs

    # ═════════════════════════════════════════════════════════════════
    # LEGACY HANDLERS (kept for backward compatibility)
    # ═════════════════════════════════════════════════════════════════

    def _handle_structured(self, text, known_words_set, native_lang, proficiency, max_words):
        """REGIME 1: Structured format (word – translation)."""
        parsed = parse_structured_text(text)
        if not parsed:
            return self._handle_plain_english(text, known_words_set, native_lang, proficiency, max_words)

        words_data = []
        already_in_library = 0
        for item in parsed:
            word = item['word'].strip()
            word_lower = word.lower()
            in_library = word_lower in known_words_set
            if in_library:
                already_in_library += 1
            words_data.append({
                'word': word,
                'translation': item['translation'],
                'in_user_library': in_library,
            })

        # Try AI enrichment for additional metadata
        enriched_map = {}
        if self.ai_provider and words_data:
            try:
                word_list = ", ".join([w['word'] for w in words_data[:max_words]])
                prompt = STRUCTURED_ENRICHMENT_PROMPT.format(
                    native_language=native_lang,
                    proficiency_level=proficiency,
                    word_list=word_list,
                )
                result = self.ai_provider.generate_json(prompt, max_tokens=3000, temperature=0.3)
                ai_words = result.get("words", []) if isinstance(result, dict) else result if isinstance(result, list) else []
                for aw in ai_words:
                    enriched_map[aw.get("word", "").lower()] = aw
            except Exception as e:
                logger.warning(f"AI enrichment for structured import failed: {e}")

        suggestions = []
        for wd in words_data[:max_words]:
            word_lower = wd['word'].lower()
            ai_data = enriched_map.get(word_lower, {})
            suggestions.append({
                "word": wd['word'],
                "translation": wd['translation'],
                "part_of_speech": ai_data.get("part_of_speech", ""),
                "difficulty": ai_data.get("difficulty", estimate_cefr(wd['word'])),
                "definition": ai_data.get("definition", ""),
                "context_sentence": ai_data.get("example", ""),
                "pronunciation": ai_data.get("pronunciation", ""),
                "reason": "From structured text",
                "in_user_library": wd['in_user_library'],
            })

        suggestions.sort(key=lambda x: CEFR_ORDER.get(x.get("difficulty", "B1"), 3), reverse=True)

        return {
            "suggestions": suggestions,
            "parse_mode": "structured",
            "total_found": len(suggestions),
            "already_in_library": already_in_library,
            "text_difficulty": self._estimate_text_difficulty(suggestions),
        }

    def _handle_plain_english(self, text, known_words_set, native_lang, proficiency, max_words):
        """REGIME 2: Plain English text — AI extraction."""
        known_words = list(known_words_set)[:200]

        if self.ai_provider:
            try:
                prompt = self.prompt_template.format(
                    text=text[:5000],
                    proficiency_level=proficiency,
                    native_language=native_lang,
                    known_words=", ".join(known_words) if known_words else "none",
                    max_words=max_words,
                )
                result = self.ai_provider.generate_json(prompt, max_tokens=2000, temperature=0.3)

                if isinstance(result, list):
                    ai_suggestions = result
                elif isinstance(result, dict) and "words" in result:
                    ai_suggestions = result["words"]
                else:
                    ai_suggestions = [result] if isinstance(result, dict) else []

                suggestions = []
                already_in_library = 0
                for s in ai_suggestions[:max_words]:
                    word = s.get("word", "").lower().strip()
                    if not word or len(word) < 3:
                        continue
                    in_library = word in known_words_set
                    if in_library:
                        already_in_library += 1
                    s["word"] = word
                    s["in_user_library"] = in_library
                    if "translations" in s and isinstance(s["translations"], list):
                        s["translation"] = ", ".join(s["translations"])
                    if not s.get("translation"):
                        s["translation"] = COMMON_TRANSLATIONS.get(word, "")
                    suggestions.append(s)

                return {
                    "suggestions": suggestions,
                    "parse_mode": "ai_extracted",
                    "total_found": len(suggestions),
                    "already_in_library": already_in_library,
                    "text_difficulty": self._estimate_text_difficulty(suggestions),
                }

            except Exception as e:
                logger.warning(f"AI analysis failed, using fallback: {e}")

        return self._fallback_extract(text, known_words_set, max_words)

    def _handle_mixed(self, text, known_words_set, native_lang, proficiency, max_words):
        """REGIME 3: Mixed language text — extract only English words."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        unique_english = []
        seen = set()
        skipped_non_english = 0
        for w in words:
            wl = w.lower()
            if wl in seen:
                continue
            seen.add(wl)
            if wl in STOP_WORDS:
                continue
            if not is_english_word(w):
                skipped_non_english += 1
                continue
            unique_english.append(wl)

        suggestions = []
        already_in_library = 0
        for word in unique_english[:max_words]:
            in_library = word in known_words_set
            if in_library:
                already_in_library += 1
            suggestions.append({
                "word": word,
                "translation": COMMON_TRANSLATIONS.get(word, ""),
                "part_of_speech": "",
                "difficulty": estimate_cefr(word),
                "definition": "",
                "context_sentence": "",
                "pronunciation": "",
                "reason": "Extracted from mixed text",
                "in_user_library": in_library,
            })

        suggestions.sort(key=lambda x: CEFR_ORDER.get(x.get("difficulty", "B1"), 3), reverse=True)

        return {
            "suggestions": suggestions,
            "parse_mode": "mixed",
            "total_found": len(suggestions),
            "already_in_library": already_in_library,
            "skipped_non_english": skipped_non_english,
            "text_difficulty": self._estimate_text_difficulty(suggestions),
        }

    def _fallback_extract(self, text, known_words_set, max_words):
        """Fallback: regex-based word extraction with heuristic difficulty."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_counts = Counter(words)

        candidates = []
        skipped_non_english = 0
        for word, count in word_counts.items():
            if word in known_words_set or word in STOP_WORDS:
                continue
            if len(word) < 4:
                continue
            if not is_english_word(word):
                skipped_non_english += 1
                continue
            candidates.append((word, count, len(word)))

        candidates.sort(key=lambda x: (CEFR_ORDER.get(estimate_cefr(x[0]), 5), -x[2]))

        suggestions = []
        already_in_library = 0
        for word, count, length in candidates[:max_words]:
            cefr = estimate_cefr(word)
            translation = COMMON_TRANSLATIONS.get(word, "")
            suggestions.append({
                "word": word,
                "translation": translation,
                "part_of_speech": "",
                "context_sentence": "",
                "difficulty": cefr,
                "definition": "",
                "pronunciation": "",
                "reason": f"Appears {count} time(s) in the text",
                "in_user_library": False,
            })

        return {
            "suggestions": suggestions,
            "parse_mode": "fallback",
            "total_found": len(suggestions),
            "already_in_library": already_in_library,
            "skipped_non_english": skipped_non_english,
            "text_difficulty": self._estimate_text_difficulty(suggestions),
        }

    # ═════════════════════════════════════════════════════════════════
    # INTERNAL HELPERS
    # ═════════════════════════════════════════════════════════════════

    def _get_user_words(self, user_id) -> set[str]:
        """Get set of lowercase words the user already has."""
        try:
            existing_words, _ = self.word_repo.get_all_by_user(
                user_id=user_id, page=1, page_size=10000,
            )
            return {w.original_word.lower() for w in existing_words}
        except Exception as e:
            logger.warning(f"Failed to get user words: {e}")
            return set()

    def _get_user_lang_info(self, user_id) -> tuple[str, str]:
        """Get user's native language name and proficiency level."""
        try:
            if self.user_repo:
                lang_info = self.user_repo.get_user_language_info(user_id)
                native_lang = self.language_map.get(
                    lang_info.get("native_language", "uz"), "Uzbek"
                )
                proficiency = lang_info.get("proficiency_level", "A2")
                return native_lang, proficiency
        except Exception as e:
            logger.warning(f"Failed to get user lang info: {e}")
        return "Uzbek", "A2"

    @staticmethod
    def _is_likely_english_text(text: str) -> bool:
        """Check if text is predominantly English."""
        words = text.split()
        if not words:
            return False
        english_count = sum(1 for w in words if is_english_word(w))
        return english_count / len(words) > 0.5

    @staticmethod
    def _estimate_text_difficulty(suggestions):
        """Estimate overall text difficulty from word difficulties."""
        if not suggestions:
            return "A1"
        levels = [s.get("difficulty", "B1") for s in suggestions if not s.get("in_user_library")]
        if not levels:
            return "A1"
        counter = Counter(levels)
        return counter.most_common(1)[0][0]


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
