"""
Smart import use cases: text analysis, word import, and CSV import.
"""

import csv
import io
import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class AnalyzeTextUseCase:
    """Analyze text and suggest unknown words for the user."""

    def __init__(self, word_repo, ai_provider, user_repo, prompt_template: str, language_map: dict):
        self.word_repo = word_repo
        self.ai_provider = ai_provider
        self.user_repo = user_repo
        self.prompt_template = prompt_template
        self.language_map = language_map

    def execute(self, user_id, text: str, max_words: int = 20) -> list[dict]:
        user_id = UUID(str(user_id))

        if not text or not text.strip():
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is required.")

        if len(text) > 5000:
            from apps.common.exceptions import ValidationError
            raise ValidationError("Text is too long. Maximum 5000 characters allowed.")

        # 1. Get user's existing words
        existing_words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=10000,
        )
        known_words = [w.original_word.lower() for w in existing_words]

        # 2. Get user language info
        lang_info = self.user_repo.get_user_language_info(user_id)
        native_lang = self.language_map.get(
            lang_info.get("native_language", "uz"), "Uzbek"
        )
        proficiency = lang_info.get("proficiency_level", "A2")

        # 3. Try AI analysis
        if self.ai_provider:
            try:
                prompt = self.prompt_template.format(
                    text=text[:5000],
                    proficiency_level=proficiency,
                    native_language=native_lang,
                    known_words=", ".join(known_words[:200]) if known_words else "none",
                    max_words=max_words,
                )
                result = self.ai_provider.generate_json(prompt, max_tokens=2000, temperature=0.3)

                if isinstance(result, list):
                    suggestions = result
                elif isinstance(result, dict) and "words" in result:
                    suggestions = result["words"]
                else:
                    suggestions = [result] if isinstance(result, dict) else []

                # Filter out known words
                filtered = []
                for s in suggestions[:max_words]:
                    word = s.get("word", "").lower().strip()
                    if word and word not in known_words and len(word) > 2:
                        s["word"] = word
                        filtered.append(s)

                return filtered[:max_words]

            except Exception as e:
                logger.warning(f"AI analysis failed, using fallback: {e}")

        # 4. Fallback: simple extraction
        return self._fallback_extract(text, known_words, max_words)

    def _fallback_extract(self, text: str, known_words: list, max_words: int) -> list:
        """Simple regex-based word extraction fallback."""
        import re
        from collections import Counter

        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_counts = Counter(words)

        # Common English words to skip
        stop_words = {
            "the", "and", "for", "are", "but", "not", "you", "all", "can",
            "had", "her", "was", "one", "our", "out", "has", "his", "how",
            "its", "may", "new", "now", "old", "see", "way", "who", "did",
            "get", "let", "say", "she", "too", "use", "will", "with",
            "that", "this", "have", "from", "they", "been", "said", "each",
            "which", "their", "there", "were", "what", "when", "make",
            "like", "just", "over", "such", "take", "year", "them", "some",
            "than", "then", "very", "about", "would", "these", "other",
            "into", "more", "also", "been", "could", "your", "after",
        }

        suggestions = []
        for word, count in word_counts.most_common(max_words * 3):
            if word in known_words or word in stop_words:
                continue
            if len(word) < 4:
                continue
            suggestions.append({
                "word": word,
                "translation": "",
                "part_of_speech": "",
                "context_sentence": "",
                "difficulty": "medium",
                "reason": f"Appears {count} time(s) in the text",
            })
            if len(suggestions) >= max_words:
                break

        return suggestions


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
