"""
Game session repository implementation using Django ORM.
"""

from uuid import UUID

from apps.common.exceptions import EntityNotFoundError
from apps.words.domain.entities import GameSessionEntity, StoryRoundEntity, ListeningRoundEntity
from apps.words.domain.repositories import AbstractGameSessionRepository
from apps.words.infrastructure.models import GameSession
from apps.words.infrastructure.models.game_models import StoryRound, ListeningRound


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
        from django.db.models import Avg, Max, Sum

        qs = GameSession.objects.filter(user_id=user_id, is_completed=True)
        total_games = qs.count()
        total_xp = qs.aggregate(total=Sum("xp_earned"))["total"] or 0

        # Per-game stats
        stats_by_type = {}
        for game_type in ["speed_round", "word_match", "word_context",
                          "story_builder", "listening_challenge"]:
            type_qs = qs.filter(game_type=game_type)
            count = type_qs.count()
            best_score = type_qs.aggregate(best=Max("score"))["best"] or 0
            avg_score = round(type_qs.aggregate(avg=Avg("score"))["avg"] or 0, 1)
            type_xp = type_qs.aggregate(total=Sum("xp_earned"))["total"] or 0
            stats_by_type[game_type] = {
                "games_played": count,
                "best_score": best_score,
                "avg_score": avg_score,
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

    # ── Story Round helpers ──────────────────────────────────────────

    @staticmethod
    def _story_round_to_entity(sr: StoryRound) -> StoryRoundEntity:
        return StoryRoundEntity(
            id=sr.id,
            session_id=sr.session_id,
            round_number=sr.round_number,
            ai_text=sr.ai_text,
            user_text=sr.user_text,
            target_words=sr.target_words,
            words_used=sr.words_used,
            grammar_corrections=sr.grammar_corrections,
            is_correct_usage=sr.is_correct_usage,
            score=sr.score,
            is_active=sr.is_active,
            created_at=sr.created_at,
            updated_at=sr.updated_at,
        )

    def create_story_round(self, session_id: UUID, **kwargs) -> StoryRoundEntity:
        sr = StoryRound.objects.create(session_id=session_id, **kwargs)
        return self._story_round_to_entity(sr)

    def get_story_rounds(self, session_id: UUID) -> list[StoryRoundEntity]:
        rounds = StoryRound.objects.filter(session_id=session_id).order_by("round_number")
        return [self._story_round_to_entity(r) for r in rounds]

    def get_story_round(self, session_id: UUID, round_number: int) -> StoryRoundEntity:
        try:
            sr = StoryRound.objects.get(session_id=session_id, round_number=round_number)
            return self._story_round_to_entity(sr)
        except StoryRound.DoesNotExist:
            raise EntityNotFoundError(f"Story round {round_number} not found.")

    def get_latest_story_round(self, session_id: UUID) -> StoryRoundEntity | None:
        sr = StoryRound.objects.filter(session_id=session_id).order_by("-round_number").first()
        if sr is None:
            return None
        return self._story_round_to_entity(sr)

    def update_story_round(self, round_id: UUID, **kwargs) -> StoryRoundEntity:
        try:
            sr = StoryRound.objects.get(id=round_id)
        except StoryRound.DoesNotExist:
            raise EntityNotFoundError("Story round not found.")
        for field, value in kwargs.items():
            setattr(sr, field, value)
        sr.save()
        return self._story_round_to_entity(sr)

    # ── Listening Round helpers ──────────────────────────────────────

    @staticmethod
    def _listening_round_to_entity(lr: ListeningRound) -> ListeningRoundEntity:
        return ListeningRoundEntity(
            id=lr.id,
            session_id=lr.session_id,
            word_id=lr.word_id,
            round_number=lr.round_number,
            correct_answer=lr.correct_answer,
            user_answers=lr.user_answers,
            attempts_used=lr.attempts_used,
            max_attempts=lr.max_attempts,
            is_correct=lr.is_correct,
            hints_shown=lr.hints_shown,
            score=lr.score,
            is_active=lr.is_active,
            created_at=lr.created_at,
            updated_at=lr.updated_at,
        )

    def create_listening_round(self, session_id: UUID, **kwargs) -> ListeningRoundEntity:
        lr = ListeningRound.objects.create(session_id=session_id, **kwargs)
        return self._listening_round_to_entity(lr)

    def get_listening_rounds(self, session_id: UUID) -> list[ListeningRoundEntity]:
        rounds = ListeningRound.objects.filter(
            session_id=session_id,
        ).select_related("word").order_by("round_number")
        return [self._listening_round_to_entity(r) for r in rounds]

    def get_listening_round(self, session_id: UUID, round_number: int) -> ListeningRoundEntity:
        try:
            lr = ListeningRound.objects.select_related("word").get(
                session_id=session_id, round_number=round_number,
            )
            return self._listening_round_to_entity(lr)
        except ListeningRound.DoesNotExist:
            raise EntityNotFoundError(f"Listening round {round_number} not found.")

    def update_listening_round(self, round_id: UUID, **kwargs) -> ListeningRoundEntity:
        try:
            lr = ListeningRound.objects.get(id=round_id)
        except ListeningRound.DoesNotExist:
            raise EntityNotFoundError("Listening round not found.")
        for field, value in kwargs.items():
            setattr(lr, field, value)
        lr.save()
        return self._listening_round_to_entity(lr)
