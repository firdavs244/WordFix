"""
Game session repository implementation using Django ORM.
"""

from uuid import UUID

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import GameSessionEntity
from apps.words.domain.repositories import AbstractGameSessionRepository
from apps.words.infrastructure.models import GameSession


class DjangoGameSessionRepository(AbstractGameSessionRepository):
    """Concrete implementation for GameSession."""

    def _to_entity(self, session: GameSession) -> GameSessionEntity:
        return GameSessionEntity(
            id=session.id,
            user_id=session.user_id,
            game_type=session.game_type,
            score=session.score,
            max_score=session.max_score,
            correct_answers=session.correct_answers,
            incorrect_answers=session.incorrect_answers,
            duration_seconds=session.duration_seconds,
            started_at=session.started_at,
            completed_at=session.completed_at,
            is_completed=session.is_completed,
            level=session.level,
            xp_earned=session.xp_earned,
            current_combo=session.current_combo,
            max_combo=session.max_combo,
            combo_xp_bonus=session.combo_xp_bonus,
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def create(self, user_id: UUID, **kwargs) -> GameSessionEntity:
        session = GameSession.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(session)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> GameSessionEntity:
        try:
            session = GameSession.objects.get(id=session_id, user_id=user_id)
            return self._to_entity(session)
        except GameSession.DoesNotExist:
            raise EntityNotFoundError("Game session not found.")

    def update(self, session_id: UUID, **kwargs) -> GameSessionEntity:
        try:
            session = GameSession.objects.get(id=session_id)
        except GameSession.DoesNotExist:
            raise EntityNotFoundError("Game session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._to_entity(session)

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[GameSessionEntity], int]:
        qs = GameSession.objects.filter(user_id=user_id).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        sessions = [self._to_entity(s) for s in qs[start:end]]
        return sessions, total

    def get_stats(self, user_id: UUID) -> dict:
        from django.db.models import Max, Sum

        qs = GameSession.objects.filter(user_id=user_id, is_completed=True)
        total_games = qs.count()
        total_xp = qs.aggregate(total=Sum("xp_earned"))["total"] or 0

        # Per-game stats
        stats_by_type = {}
        for game_type in ["speed_round", "word_match", "word_context"]:
            type_qs = qs.filter(game_type=game_type)
            count = type_qs.count()
            best_score = type_qs.aggregate(best=Max("score"))["best"] or 0
            type_xp = type_qs.aggregate(total=Sum("xp_earned"))["total"] or 0
            stats_by_type[game_type] = {
                "games_played": count,
                "best_score": best_score,
                "total_xp": type_xp,
            }

        # Favorite game
        favorite = None
        max_count = 0
        for gt, st in stats_by_type.items():
            if st["games_played"] > max_count:
                max_count = st["games_played"]
                favorite = gt

        return {
            "total_games": total_games,
            "total_xp": total_xp,
            "favorite_game": favorite,
            "by_type": stats_by_type,
        }
