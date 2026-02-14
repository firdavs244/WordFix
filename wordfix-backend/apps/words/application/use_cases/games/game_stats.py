"""Game history and stats use cases."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class GetGameHistoryUseCase:
    """Get game session history."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id, page=1, page_size=20):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_by_user(
            user_id=user_id, page=page, page_size=page_size
        )


class GetGameStatsUseCase:
    """Get game stats for a user."""

    def __init__(self, game_session_repo):
        self.game_session_repo = game_session_repo

    def execute(self, user_id):
        user_id = UUID(str(user_id))
        return self.game_session_repo.get_stats(user_id=user_id)
