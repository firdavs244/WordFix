"""
AI service prompts package.

Re-exports all prompt constants for backward compatibility.
Import from here: ``from core.services.ai.prompts import WORD_ENRICHMENT_PROMPT``
"""

from .enrichment_prompts import (  # noqa: F401
    NATIVE_LANGUAGE_MAP,
    WORD_ENRICHMENT_PROMPT,
)
from .test_prompts import (  # noqa: F401
    CONTEXT_GUESS_PROMPT,
    FILL_BLANK_PROMPT,
    MULTIPLE_CHOICE_PROMPT,
    WORD_CONTEXT_GAME_PROMPT,
)
from .game_prompts import (  # noqa: F401
    STORY_CONTINUE_PROMPT,
    STORY_FALLBACK_TEMPLATES,
    STORY_GENRES,
    STORY_START_PROMPT,
    SYNONYM_ANTONYM_PROMPT,
)
from .chat_prompts import CHAT_SYSTEM_PROMPT  # noqa: F401
from .import_prompts import (  # noqa: F401
    CONFUSING_PAIR_DRILL_PROMPT,
    SMART_DISTRACTOR_PROMPT,
    SMART_IMPORT_PROMPT,
)

__all__ = [
    "NATIVE_LANGUAGE_MAP",
    "WORD_ENRICHMENT_PROMPT",
    "MULTIPLE_CHOICE_PROMPT",
    "FILL_BLANK_PROMPT",
    "CONTEXT_GUESS_PROMPT",
    "WORD_CONTEXT_GAME_PROMPT",
    "SMART_IMPORT_PROMPT",
    "CHAT_SYSTEM_PROMPT",
    "SMART_DISTRACTOR_PROMPT",
    "CONFUSING_PAIR_DRILL_PROMPT",
    "STORY_START_PROMPT",
    "STORY_CONTINUE_PROMPT",
    "STORY_GENRES",
    "STORY_FALLBACK_TEMPLATES",
    "SYNONYM_ANTONYM_PROMPT",
]
