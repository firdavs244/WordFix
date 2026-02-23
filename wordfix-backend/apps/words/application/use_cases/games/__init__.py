"""
Game use cases: Speed Round, Word Match, Word Context, Story Builder,
Listening Challenge, Synonym & Antonym, Irregular Verbs.

This package re-exports all game use cases for backward compatibility.
"""

from .speed_round import StartSpeedRoundUseCase, SubmitSpeedRoundUseCase  # noqa: F401
from .word_match import StartWordMatchUseCase, SubmitWordMatchUseCase  # noqa: F401
from .word_context import StartWordContextUseCase, SubmitWordContextUseCase  # noqa: F401
from .story_builder import (  # noqa: F401
    StartStoryBuilderUseCase,
    SubmitStoryRoundUseCase,
    CompleteStoryBuilderUseCase,
)
from .listening import (  # noqa: F401
    StartListeningChallengeUseCase,
    SubmitListeningAnswerUseCase,
    CompleteListeningChallengeUseCase,
)
from .synonym_antonym import (  # noqa: F401
    StartSynonymAntonymUseCase,
    SubmitSynonymAntonymUseCase,
    CompleteSynonymAntonymUseCase,
)
from .irregular_verbs import (  # noqa: F401
    StartIrregularVerbsUseCase,
    SubmitIrregularVerbUseCase,
    CompleteIrregularVerbsUseCase,
)
from .game_stats import GetGameHistoryUseCase, GetGameStatsUseCase  # noqa: F401

__all__ = [
    "StartSpeedRoundUseCase",
    "SubmitSpeedRoundUseCase",
    "StartWordMatchUseCase",
    "SubmitWordMatchUseCase",
    "StartWordContextUseCase",
    "SubmitWordContextUseCase",
    "StartStoryBuilderUseCase",
    "SubmitStoryRoundUseCase",
    "CompleteStoryBuilderUseCase",
    "StartListeningChallengeUseCase",
    "SubmitListeningAnswerUseCase",
    "CompleteListeningChallengeUseCase",
    "StartSynonymAntonymUseCase",
    "SubmitSynonymAntonymUseCase",
    "CompleteSynonymAntonymUseCase",
    "StartIrregularVerbsUseCase",
    "SubmitIrregularVerbUseCase",
    "CompleteIrregularVerbsUseCase",
    "GetGameHistoryUseCase",
    "GetGameStatsUseCase",
]
