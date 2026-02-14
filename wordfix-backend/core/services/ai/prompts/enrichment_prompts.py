"""
Word enrichment prompts.
"""

NATIVE_LANGUAGE_MAP = {
    "uz": "Uzbek",
    "ru": "Russian",
    "tr": "Turkish",
    "ko": "Korean",
    "ar": "Arabic",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "ja": "Japanese",
    "zh": "Chinese",
    "hi": "Hindi",
    "pt": "Portuguese",
}


WORD_ENRICHMENT_PROMPT = """You are a language learning assistant. User speaks {native_language}, \
learning {learning_language}, level {proficiency_level}.

Enrich this word: "{word}"

Respond ONLY with valid JSON:
{{
  "translation": "in {native_language}",
  "pronunciation": "IPA like /ˈfiːtʃər/",
  "part_of_speech": "noun|verb|adjective|adverb|preposition|conjunction|pronoun|interjection|phrase|other",
  "definition": "clear English definition for {proficiency_level} level",
  "example_sentence": "natural sentence for {proficiency_level} level",
  "example_translation": "sentence translation in {native_language}",
  "synonyms": ["syn1","syn2","syn3"],
  "antonyms": ["ant1","ant2"],
  "collocations": ["col1","col2","col3"],
  "word_family": ["form1","form2"],
  "difficulty_level": "easy|medium|hard",
  "mnemonic": "creative memory trick in {native_language}, use sound/visual associations",
  "usage_notes": "usage tips, common mistakes, formal/informal register"
}}"""
