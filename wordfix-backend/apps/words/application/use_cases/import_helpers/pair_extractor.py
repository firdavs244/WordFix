"""
Pair extractor module for smart import.

Extracts English word + Uzbek translation pairs from cleaned text
using multiple extraction strategies.
"""

import re
import logging
from typing import Optional

from .language_detector import is_english_word, is_uzbek_word, is_document_title, has_uzbek_characters

logger = logging.getLogger(__name__)


def extract_word_pairs(cleaned_text: str) -> list[dict]:
    """
    Extract English word + Uzbek translation pairs from cleaned text.

    Applies 6 extraction strategies in order of reliability:
    1. Numbered pairs (most reliable)
    2. Dash-separated pairs
    3. Inline parentheses
    4. Parenthesized translations (next line)
    5. Adjacent English→Uzbek line pairs
    6. Skip phrasal expressions with "..."

    Returns list of dicts with keys: word, translation, confidence
    """
    if not cleaned_text or not cleaned_text.strip():
        return []

    lines = cleaned_text.split("\n")
    lines = [l.strip() for l in lines]

    pairs = []
    used_indices = set()

    # ── Strategy 1: Numbered pairs ──────────────────────────────────
    # "1. Female\nUrg'ochi"
    for i, line in enumerate(lines):
        if i in used_indices:
            continue
        match = re.match(r'^(\d+)[\.\)]\s+(.+)$', line)
        if match:
            word_candidate = match.group(2).strip()
            # Skip if it's a section header
            if re.match(r'^(Unit|Chapter|Section|Lesson)\s+', word_candidate, re.IGNORECASE):
                continue
            if is_english_word(word_candidate) and not is_document_title(word_candidate):
                translation = ""
                if i + 1 < len(lines) and lines[i + 1]:
                    next_line = lines[i + 1].strip()
                    translation = _extract_translation(next_line)
                    if translation is not None:
                        used_indices.add(i + 1)
                    else:
                        translation = ""
                pairs.append({
                    "word": word_candidate,
                    "translation": translation,
                    "confidence": 0.95,
                })
                used_indices.add(i)

    # ── Strategy 2: Dash-separated pairs ────────────────────────────
    # "Clap – Qarsak chalmoq"
    for i, line in enumerate(lines):
        if i in used_indices:
            continue
        match = re.match(r'^(.+?)\s*[–—]\s*(.+)$', line)
        if not match:
            # Also try regular hyphen with spaces around it
            match = re.match(r'^(.+?)\s+\-\s+(.+)$', line)
        if match:
            word_candidate = match.group(1).strip()
            translation_candidate = match.group(2).strip()
            # Remove leading number: "1. Clap" → "Clap"
            word_candidate = re.sub(r'^\d+[\.\)]\s*', '', word_candidate).strip()
            if is_english_word(word_candidate) and not is_document_title(word_candidate):
                pairs.append({
                    "word": word_candidate,
                    "translation": translation_candidate,
                    "confidence": 0.90,
                })
                used_indices.add(i)

    # ── Strategy 3: Inline parentheses ──────────────────────────────
    # "Look after (G'amxo'rlik qilmoq)"
    for i, line in enumerate(lines):
        if i in used_indices:
            continue
        match = re.match(r'^(.+?)\s*\((.+?)\)\s*$', line)
        if match:
            word_candidate = match.group(1).strip()
            translation_candidate = match.group(2).strip()
            # Remove leading number
            word_candidate = re.sub(r'^\d+[\.\)]\s*', '', word_candidate).strip()
            if is_english_word(word_candidate) and not is_document_title(word_candidate):
                if is_uzbek_word(translation_candidate) or has_uzbek_characters(translation_candidate):
                    pairs.append({
                        "word": word_candidate,
                        "translation": translation_candidate,
                        "confidence": 0.88,
                    })
                    used_indices.add(i)

    # ── Strategy 4: Parenthesized translations on next line ─────────
    # "Headache\n(Bosh og'rig'i)"
    for i, line in enumerate(lines):
        if i in used_indices:
            continue
        if not line:
            continue
        word_candidate = line.strip()
        if is_english_word(word_candidate) and not is_document_title(word_candidate):
            if i + 1 < len(lines) and (i + 1) not in used_indices:
                next_line = lines[i + 1].strip()
                paren_match = re.match(r'^\((.+)\)$', next_line)
                if paren_match:
                    translation = paren_match.group(1).strip()
                    pairs.append({
                        "word": word_candidate,
                        "translation": translation,
                        "confidence": 0.92,
                    })
                    used_indices.add(i)
                    used_indices.add(i + 1)

    # ── Strategy 5: Adjacent English → Uzbek line pairs ─────────────
    # "Cone\nKonus"
    for i, line in enumerate(lines):
        if i in used_indices:
            continue
        if not line:
            continue
        word_candidate = line.strip()
        # Skip section headers
        if re.match(r'^(Unit|Chapter|Section|Lesson|Part|Topic)\s+\d', word_candidate, re.IGNORECASE):
            continue
        if is_english_word(word_candidate) and not is_document_title(word_candidate):
            if i + 1 < len(lines) and (i + 1) not in used_indices:
                next_line = lines[i + 1].strip()
                if next_line:
                    translation = _extract_translation(next_line)
                    if translation is not None:
                        pairs.append({
                            "word": word_candidate,
                            "translation": translation,
                            "confidence": 0.80,
                        })
                        used_indices.add(i)
                        used_indices.add(i + 1)

    # ── Deduplication & Filtering ───────────────────────────────────
    pairs = _deduplicate_pairs(pairs)
    pairs = _filter_pairs(pairs)

    # Sort by confidence (highest first)
    pairs.sort(key=lambda p: p.get("confidence", 0), reverse=True)

    return pairs


def _extract_translation(line: str) -> Optional[str]:
    """Extract translation from a line. Returns None if not a translation."""
    line = line.strip()
    if not line:
        return None

    # Parenthesized: (Bosh og'rig'i)
    match = re.match(r'^\((.+)\)$', line)
    if match:
        return match.group(1).strip()

    # Starts with '...' — Uzbek phrasal expression
    if line.startswith('...'):
        return line

    # O'zbekcha so'z or phrase
    if is_uzbek_word(line) or has_uzbek_characters(line):
        return line

    # If it's a pure English word — NOT a translation
    if is_english_word(line):
        return None

    # Mixed or unknown — could be translation if it has Uzbek characteristics
    # Check for any non-ASCII-letter which might indicate Uzbek
    if len(line) > 1 and not re.match(r'^[a-zA-Z\s]+$', line):
        return line

    return None


def _deduplicate_pairs(pairs: list[dict]) -> list[dict]:
    """Remove duplicate word entries (keep highest confidence)."""
    seen = {}
    for pair in pairs:
        key = pair["word"].lower().strip()
        if key not in seen or pair.get("confidence", 0) > seen[key].get("confidence", 0):
            seen[key] = pair
    return list(seen.values())


def _filter_pairs(pairs: list[dict]) -> list[dict]:
    """Filter out invalid pairs."""
    filtered = []
    for pair in pairs:
        word = pair["word"].strip()

        # Skip if not a valid English word
        if not is_english_word(word):
            continue

        # Skip document titles
        if is_document_title(word):
            continue

        # Skip very short words with no translation
        if len(word) <= 1 and not pair.get("translation"):
            continue

        filtered.append(pair)

    return filtered
