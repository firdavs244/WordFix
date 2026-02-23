"""
Smart import, distractor, and confusing pair drill prompts.
"""

SMART_IMPORT_PROMPT = """You are a vocabulary extraction expert. Analyze the following English text \
and extract ALL meaningful vocabulary words.

TEXT:
\"\"\"
{text}
\"\"\"

The learner's current level: {proficiency_level}
The learner's native language: {native_language}
Words the student already knows (EXCLUDE them): {known_words}

EXTRACTION RULES:
1. Extract ALL unique content words (nouns, verbs, adjectives, adverbs)
2. SKIP: articles (a, the), prepositions (in, on, at), pronouns (I, he, she),
   common verbs (is, are, was, have, do, go, get, make, take),
   conjunctions (and, but, or), numbers
3. SKIP: proper nouns (names, places) unless they are commonly used words
4. For EACH word, provide:
   - The word in base/dictionary form (e.g., "running" -> "run")
   - Part of speech
   - CEFR difficulty level (A1, A2, B1, B2, C1, C2)
   - Translation to {native_language} (2-3 main translations)
   - A brief definition in English
5. Sort by difficulty: C2 first, then C1, B2, B1, A2, A1
6. Extract up to {max_words} words - get ALL meaningful words

Respond ONLY with a valid JSON array:
[
  {{
    "word": "serendipity",
    "part_of_speech": "noun",
    "difficulty": "C1",
    "translation": "kutilmagan topilma",
    "definition": "the occurrence of finding pleasant things by chance",
    "context_sentence": "the sentence from the text where this word appears",
    "reason": "Advanced vocabulary useful for academic reading"
  }}
]"""


SMART_DISTRACTOR_PROMPT = """
Word: "{word}" (translation: "{translation}", part of speech: {part_of_speech})
User level: {user_level}
EXCLUDE these synonyms: {synonyms}

Generate exactly {count} WRONG translation options in {native_language}.

Rules:
- Options must NOT be synonyms or similar meanings of "{word}"
- Options must be same part of speech ({part_of_speech})
- Options should be similar difficulty level
- Options should be plausible (same topic/category but different meaning)
- Options must be single words or short phrases

Good examples:
- Word "run" (yugurmoq) → "o'tirmoq", "uxlamoq", "yurish"
  NOT "chopmoq", "yugurish", "shoshmoq" (these are synonyms)
- Word "happy" (baxtli) → "xafa", "charchagan", "g'azablangan"
  NOT "xursand", "mamnun", "quvnoq" (these are synonyms)

Respond ONLY with valid JSON:
{{"distractors": ["option1", "option2", "option3"]}}
"""


CONFUSING_PAIR_DRILL_PROMPT = """
User speaks {native_language}, learning English at {proficiency_level} level.

They keep confusing these two words:
Word 1: "{word_1}" ({translation_1})
Word 2: "{word_2}" ({translation_2})
They confused them {confusion_count} times.

Create a mini-lesson to help them distinguish:

Respond ONLY with valid JSON:
{{
  "explanation": "Clear explanation of the difference in {native_language}",
  "word_1_examples": [
    {{"sentence": "English sentence using {word_1}", "translation": "in {native_language}"}},
    {{"sentence": "Another sentence", "translation": "translation"}}
  ],
  "word_2_examples": [
    {{"sentence": "English sentence using {word_2}", "translation": "in {native_language}"}},
    {{"sentence": "Another sentence", "translation": "translation"}}
  ],
  "mnemonic": "Creative memory trick in {native_language} to remember the difference",
  "test_questions": [
    {{
      "sentence": "Sentence with blank: The ___ of the medicine was immediate.",
      "correct_answer": "the correct word",
      "wrong_answer": "the wrong word",
      "explanation": "Why this answer is correct"
    }},
    {{
      "sentence": "Another sentence with blank",
      "correct_answer": "correct",
      "wrong_answer": "wrong",
      "explanation": "explanation"
    }},
    {{
      "sentence": "Third sentence",
      "correct_answer": "correct",
      "wrong_answer": "wrong",
      "explanation": "explanation"
    }},
    {{
      "sentence": "Fourth sentence",
      "correct_answer": "correct",
      "wrong_answer": "wrong",
      "explanation": "explanation"
    }},
    {{
      "sentence": "Fifth sentence",
      "correct_answer": "correct",
      "wrong_answer": "wrong",
      "explanation": "explanation"
    }}
  ]
}}
"""
