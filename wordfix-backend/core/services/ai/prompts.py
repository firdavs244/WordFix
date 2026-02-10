"""
AI service prompts for word enrichment and test generation.
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


# =============================================================================
# TEST GENERATION PROMPTS
# =============================================================================

MULTIPLE_CHOICE_PROMPT = """You are a language test generator. Create multiple-choice questions.
User speaks {native_language}, learning English, level {proficiency_level}.

Generate exactly {count} questions using ONLY these words: {words_list}

Mix question types:
- word → translation (give English word, pick correct {native_language} translation)
- translation → word (give {native_language} translation, pick correct English word)
- definition → word (give English definition, pick correct English word)

Each question must have exactly 4 options. Distractors should be plausible (similar difficulty, same part of speech when possible).

Respond ONLY with a valid JSON array:
[
  {{
    "word": "the target word",
    "question_type": "word_to_translation|translation_to_word|multiple_choice",
    "question": "the question text",
    "correct_answer": "correct option",
    "options": ["option1", "option2", "option3", "option4"],
    "explanation": "brief explanation why this is correct"
  }}
]"""


FILL_BLANK_PROMPT = """You are a language test generator. Create fill-in-the-blank questions.
User speaks {native_language}, learning English, level {proficiency_level}.

Generate exactly {count} sentences using ONLY these words: {words_list}

Each sentence should:
- Be natural and appropriate for {proficiency_level} level
- Have exactly one blank (___) where the target word belongs
- Include a helpful hint

Respond ONLY with a valid JSON array:
[
  {{
    "word": "the target word",
    "question_type": "fill_blank",
    "sentence_with_blank": "The ___ of this product is amazing.",
    "correct_answer": "quality",
    "hint": "starts with 'q', means how good something is",
    "explanation": "brief explanation"
  }}
]"""


CONTEXT_GUESS_PROMPT = """You are a language test generator. Create context-guess questions.
User speaks {native_language}, learning English, level {proficiency_level}.

Generate exactly {count} short paragraphs (3-5 sentences each) using ONLY these words: {words_list}

Each paragraph should:
- Use the target word naturally in context
- Replace the target word with ___ in the paragraph
- Be appropriate for {proficiency_level} level
- Have 4 answer options (1 correct + 3 plausible distractors)

Respond ONLY with a valid JSON array:
[
  {{
    "word": "the target word",
    "question_type": "context_guess",
    "context_paragraph": "paragraph with ___ replacing the target word",
    "question": "What word best fits the blank?",
    "correct_answer": "correct word",
    "options": ["option1", "option2", "option3", "option4"],
    "explanation": "brief explanation based on context clues"
  }}
]"""


WORD_CONTEXT_GAME_PROMPT = """You are a language learning assistant. Create short context passages.
User speaks {native_language}, learning English, level {proficiency_level}.

For each of these words, write a short passage (2-3 sentences) that uses the word naturally.
Replace the target word with ___ in the passage.
Words: {words_list}

Respond ONLY with a valid JSON array:
[
  {{
    "word": "target word",
    "context": "passage with ___ replacing the target word",
    "correct_answer": "the target word",
    "options": ["option1", "option2", "option3", "option4"],
    "explanation": "context clues that point to the answer"
  }}
]"""


# =============================================================================
# SMART IMPORT PROMPTS
# =============================================================================

SMART_IMPORT_PROMPT = """You are a vocabulary analysis assistant. Analyze the given English text and \
identify words that a {proficiency_level} level student (who speaks {native_language}) probably does NOT know.

Text to analyze:
\"\"\"
{text}
\"\"\"

The student already knows these words (EXCLUDE them): {known_words}

Instructions:
1. Find up to {max_words} words the student likely does NOT know
2. Focus on useful, practical vocabulary
3. Prioritize more important/common words first
4. Exclude proper nouns, numbers, and very basic words (a, the, is, etc.)

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


# =============================================================================
# AI CHAT PROMPTS
# =============================================================================

CHAT_SYSTEM_PROMPT = """You are a friendly English tutor chatting with a {proficiency_level} level \
student who speaks {native_language}. Your goals:
1. Have a natural conversation about {topic}
2. Naturally use these target words in your messages: {words_list}
3. Keep your language appropriate for {proficiency_level} level
4. After the student responds, briefly note any grammar mistakes
5. Encourage the student to use the target words

Format your response as JSON:
{{
  "message": "your conversational response",
  "corrections": [{{"original": "I go yesterday", "corrected": "I went yesterday", "explanation": "Past tense needed"}}],
  "words_used_by_student": ["feature", "determine"],
  "encouragement": "Great use of 'feature'! Try using 'avalanche' in your next message."
}}"""


# =============================================================================
# SMART DISTRACTOR PROMPT
# =============================================================================

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


# =============================================================================
# CONFUSING PAIR DRILL PROMPT
# =============================================================================

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
