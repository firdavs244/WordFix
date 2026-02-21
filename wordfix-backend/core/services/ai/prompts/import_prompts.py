"""
Smart import, distractor, and confusing pair drill prompts.
"""

SMART_IMPORT_PROMPT = """You are a vocabulary analysis assistant. Analyze the given English text and \
identify words that a {proficiency_level} level student (who speaks {native_language}) probably does NOT know.

Text to analyze:
\"\"\"
{text}
\"\"\"

The student already knows these words (EXCLUDE them): {known_words}

Instructions:
1. Find up to {max_words} words the student likely does NOT know
2. Prioritize: rare/advanced words first, then medium, then common last
3. Sort by difficulty: hardest first
4. Skip very common words (the, is, are, have, do, go, get, make, take, etc.)
5. Include: academic, professional, and idiomatic words
6. Exclude proper nouns, numbers, and basic function words
7. Focus on useful, practical vocabulary worth memorizing

Respond ONLY with a valid JSON array:
[
  {{
    "word": "the vocabulary word (lowercase)",
    "translation": "translation in {native_language}",
    "part_of_speech": "noun|verb|adjective|adverb|preposition|conjunction|pronoun|interjection|phrase|other",
    "context_sentence": "the sentence from the text where this word appears",
    "difficulty": "easy|medium|hard",
    "reason": "brief explanation why this word is worth learning for a {proficiency_level} student"
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
