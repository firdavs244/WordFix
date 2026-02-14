"""
Story Builder game prompts and fallback templates.
"""

STORY_START_PROMPT = """You are a creative storyteller for a {proficiency_level} level English learner \
who speaks {native_language}.

Create the beginning of a short, engaging story (2-3 sentences).
Genre: {genre}
You MUST naturally use this word in the story: "{target_word}"

Keep language appropriate for {proficiency_level} level.
The story should be interesting enough that the reader wants to continue it.

Respond ONLY with valid JSON:
{{
  "story_text": "Your 2-3 sentence story beginning...",
  "genre": "{genre}",
  "setting": "brief setting description"
}}
"""


STORY_CONTINUE_PROMPT = """You are a creative storyteller helping a {proficiency_level} level English learner.

Story so far:
{story_so_far}

The student wrote this continuation:
"{user_text}"

Tasks:
1. Check if they correctly used the target word(s): {target_words}
2. Check grammar
3. Continue the story with 2-3 new sentences
4. Naturally include this new target word: "{next_target_word}"

Respond ONLY with valid JSON:
{{
  "words_used_correctly": ["word1"],
  "words_not_used": ["word2"],
  "grammar_corrections": [
    {{"original": "wrong text", "corrected": "correct text", "explanation": "why"}}
  ],
  "is_grammar_good": true,
  "feedback": "Brief encouraging feedback in {native_language}",
  "continuation": "Your 2-3 sentence story continuation...",
  "score": 15
}}

Score rules (0-20 per round):
- Used target word correctly: +8
- Good grammar: +7
- Creative/interesting writing: +5
- Didn't use target word: 0 for word part
"""


STORY_GENRES = [
    "adventure", "mystery", "comedy", "sci-fi",
    "daily_life", "travel", "fantasy", "horror_light",
]


STORY_FALLBACK_TEMPLATES = {
    "adventure": [
        "The sun was setting behind the mountains when {name} found an old map in the attic. It showed a path to a hidden {target_word} that nobody had seen before.",
        "Deep in the jungle, a group of explorers discovered an ancient temple. The walls were covered with strange symbols about {target_word}.",
    ],
    "mystery": [
        "Detective Parker looked at the evidence on the table. Something about this case was different — it all connected to {target_word}.",
        "The old house on Hill Street had been empty for years. But last night, someone saw a light in the window and heard a voice talking about {target_word}.",
    ],
    "comedy": [
        "My neighbor's cat decided to become a chef yesterday. Its first recipe involved {target_word} and a lot of confusion.",
        "When the alarm went off, Tom realized he had accidentally set it for PM instead of AM. His day of {target_word} was just beginning.",
    ],
    "sci-fi": [
        "In the year 3025, humans discovered that {target_word} was the key to traveling between galaxies.",
        "The robot looked at its creator with curiosity. 'Tell me about {target_word},' it said for the first time.",
    ],
    "daily_life": [
        "It was a normal Monday morning until Sarah's coffee machine started making unusual sounds related to {target_word}.",
        "Walking to school, Jamie noticed something interesting about {target_word} that changed the whole day.",
    ],
    "travel": [
        "The train to Barcelona was late, so Maria decided to explore the small town. She found a café where everyone was talking about {target_word}.",
        "After landing in Tokyo, the first thing Alex noticed was how everything connected to {target_word}.",
    ],
    "fantasy": [
        "In the magical kingdom of Eldoria, a young wizard discovered a spell book about {target_word}.",
        "The dragon was not like other dragons. Instead of breathing fire, it could create {target_word} from thin air.",
    ],
    "horror_light": [
        "The old library was quiet, too quiet. Then a book about {target_word} fell from the shelf by itself.",
        "Every night at midnight, the painting on the wall changed. Tonight it showed something about {target_word}.",
    ],
}
