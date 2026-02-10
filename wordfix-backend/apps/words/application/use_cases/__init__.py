"""
Word application use cases package.

Re-exports all use cases so existing imports remain unchanged:
    from apps.words.application.use_cases import AddWordUseCase  # works
"""

from .word_crud import *  # noqa: F401, F403
from .enrichment import *  # noqa: F401, F403
from .review import *  # noqa: F401, F403
from .streak import *  # noqa: F401, F403
from .testing import *  # noqa: F401, F403
from .games import *  # noqa: F401, F403
from .smart_import import *  # noqa: F401, F403
from .chat import *  # noqa: F401, F403
from .analytics import *  # noqa: F401, F403
from .confusing_pairs import *  # noqa: F401, F403
from .daily_challenges import *  # noqa: F401, F403
