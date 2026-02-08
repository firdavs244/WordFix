"""
Word repository implementations using Django ORM.
"""

from datetime import date
from uuid import UUID

from django.db.models import Count, Q, Avg
from django.utils import timezone

from apps.common.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from apps.words.domain.entities import (
    DailyActivityEntity,
    DailyStreakEntity,
    GameSessionEntity,
    ReviewLogEntity,
    ReviewSessionEntity,
    TestQuestionEntity,
    TestSessionEntity,
    WordCategoryEntity,
    WordEntity,
)
from apps.words.domain.repositories import (
    AbstractDailyActivityRepository,
    AbstractDailyStreakRepository,
    AbstractGameSessionRepository,
    AbstractReviewLogRepository,
    AbstractReviewSessionRepository,
    AbstractTestQuestionRepository,
    AbstractTestSessionRepository,
    AbstractWordCategoryRepository,
    AbstractWordRepository,
)
from apps.words.infrastructure.models import (
    DailyActivity,
    DailyStreak,
    GameSession,
    ReviewLog,
    ReviewSession,
    TestQuestion,
    TestSession,
    Word,
    WordCategory,
)


class DjangoWordRepository(AbstractWordRepository):
    """Concrete implementation of AbstractWordRepository."""

    def _to_entity(self, word: Word) -> WordEntity:
        """Convert Word model to WordEntity."""
        category_entity = None
        if word.category:
            category_entity = WordCategoryEntity(
                id=word.category.id,
                user_id=word.category.user_id,
                name=word.category.name,
                color=word.category.color,
                icon=word.category.icon,
                words_count=word.category.words_count,
            )

        return WordEntity(
            id=word.id,
            user_id=word.user_id,
            original_word=word.original_word,
            translation=word.translation,
            pronunciation=word.pronunciation,
            part_of_speech=word.part_of_speech,
            definition=word.definition,
            example_sentence=word.example_sentence,
            example_translation=word.example_translation,
            synonyms=word.synonyms,
            antonyms=word.antonyms,
            collocations=word.collocations,
            word_family=word.word_family,
            image_url=word.image_url,
            audio_url=word.audio_url,
            notes=word.notes,
            mnemonic=word.mnemonic,
            usage_notes=word.usage_notes,
            category_id=word.category_id,
            category=category_entity,
            tags=word.tags,
            difficulty_level=word.difficulty_level,
            is_enriched=word.is_enriched,
            enrichment_status=word.enrichment_status,
            enrichment_error=word.enrichment_error,
            enriched_at=word.enriched_at,
            confidence_score=word.confidence_score,
            next_review_at=word.next_review_at,
            review_count=word.review_count,
            correct_count=word.correct_count,
            incorrect_count=word.incorrect_count,
            last_reviewed_at=word.last_reviewed_at,
            is_mastered=word.is_mastered,
            easiness_factor=word.easiness_factor,
            repetition_number=word.repetition_number,
            interval_days=word.interval_days,
            is_active=word.is_active,
            created_at=word.created_at,
            updated_at=word.updated_at,
        )

    def get_by_id(self, word_id: UUID, user_id: UUID) -> WordEntity:
        try:
            word = Word.objects.select_related("category").get(id=word_id, user_id=user_id)
            return self._to_entity(word)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")

    def get_all_by_user(
        self, user_id: UUID, filters: dict | None = None,
        ordering: str = "-created_at", page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(user_id=user_id).select_related("category")

        if filters:
            if filters.get("category_id"):
                qs = qs.filter(category_id=filters["category_id"])
            if filters.get("difficulty_level"):
                qs = qs.filter(difficulty_level=filters["difficulty_level"])
            if "is_mastered" in filters:
                qs = qs.filter(is_mastered=filters["is_mastered"])
            if "is_enriched" in filters:
                qs = qs.filter(is_enriched=filters["is_enriched"])
            if filters.get("part_of_speech"):
                qs = qs.filter(part_of_speech=filters["part_of_speech"])
            if filters.get("search"):
                query = filters["search"]
                qs = qs.filter(
                    Q(original_word__icontains=query) | Q(translation__icontains=query)
                )

        # Ordering
        allowed_ordering = {
            "created_at", "-created_at",
            "original_word", "-original_word",
            "confidence_score", "-confidence_score",
        }
        if ordering not in allowed_ordering:
            ordering = "-created_at"

        total = qs.count()
        qs = qs.order_by(ordering)

        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        words = [self._to_entity(w) for w in qs[start:end]]

        return words, total

    def create(self, user_id: UUID, **kwargs) -> WordEntity:
        original_word = kwargs.get("original_word", "").strip().lower()
        if Word.objects.filter(user_id=user_id, original_word__iexact=original_word).exists():
            raise EntityAlreadyExistsError(
                f"Word '{original_word}' already exists in your word bank."
            )
        kwargs["original_word"] = original_word
        word = Word.objects.create(user_id=user_id, **kwargs)
        word = Word.objects.select_related("category").get(id=word.id)
        return self._to_entity(word)

    def update(self, word_id: UUID, user_id: UUID, **kwargs) -> WordEntity:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")

        for field, value in kwargs.items():
            setattr(word, field, value)
        word.save()
        word = Word.objects.select_related("category").get(id=word.id)
        return self._to_entity(word)

    def delete(self, word_id: UUID, user_id: UUID) -> None:
        try:
            word = Word.objects.get(id=word_id, user_id=user_id)
        except Word.DoesNotExist:
            raise EntityNotFoundError("Word not found.")
        word.delete()

    def exists(self, original_word: str, user_id: UUID) -> bool:
        return Word.objects.filter(
            user_id=user_id, original_word__iexact=original_word.strip()
        ).exists()

    def get_count_by_user(self, user_id: UUID) -> int:
        return Word.objects.filter(user_id=user_id).count()

    def search(
        self, user_id: UUID, query: str, page: int = 1, page_size: int = 20,
    ) -> tuple[list[WordEntity], int]:
        qs = Word.objects.filter(
            user_id=user_id,
        ).filter(
            Q(original_word__icontains=query) | Q(translation__icontains=query)
        ).select_related("category")

        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        words = [self._to_entity(w) for w in qs[start:end]]
        return words, total

    def get_by_category(self, user_id: UUID, category_id: UUID) -> list[WordEntity]:
        qs = Word.objects.filter(
            user_id=user_id, category_id=category_id
        ).select_related("category")
        return [self._to_entity(w) for w in qs]

    def get_words_for_review(self, user_id: UUID) -> list[WordEntity]:
        now = timezone.now()
        qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
        ).filter(
            Q(next_review_at__isnull=True) | Q(next_review_at__lte=now)
        ).select_related("category").order_by("confidence_score")[:20]
        return [self._to_entity(w) for w in qs]

    def get_review_words(
        self, user_id: UUID, limit: int = 20, session_type: str = "review",
    ) -> list[WordEntity]:
        """Get words due for review based on session type."""
        now = timezone.now()

        if session_type == "quick":
            limit = 5

        if session_type == "focus":
            qs = Word.objects.filter(
                user_id=user_id,
                is_mastered=False,
                confidence_score__lt=30,
            ).select_related("category").order_by("confidence_score")[:limit]
            return [self._to_entity(w) for w in qs]

        # Due words + some new words
        due_qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
            next_review_at__lte=now,
        ).select_related("category").order_by("next_review_at")

        new_qs = Word.objects.filter(
            user_id=user_id,
            is_mastered=False,
            next_review_at__isnull=True,
        ).select_related("category").order_by("created_at")[:5]

        due_list = list(due_qs[:limit])
        remaining = limit - len(due_list)
        if remaining > 0:
            due_list.extend(list(new_qs[:remaining]))

        return [self._to_entity(w) for w in due_list]

    def get_review_summary_stats(self, user_id: UUID) -> dict:
        """Get review summary statistics for a user."""
        from datetime import timedelta

        now = timezone.now()

        total = Word.objects.filter(user_id=user_id).count()
        mastered = Word.objects.filter(user_id=user_id, is_mastered=True).count()
        due_today = Word.objects.filter(
            user_id=user_id, is_mastered=False, next_review_at__lte=now
        ).count()
        overdue = Word.objects.filter(
            user_id=user_id, is_mastered=False,
            next_review_at__lt=now - timedelta(days=1)
        ).count()
        new_words = Word.objects.filter(
            user_id=user_id, next_review_at__isnull=True
        ).count()
        learning = total - mastered - new_words

        next_word = Word.objects.filter(
            user_id=user_id, is_mastered=False, next_review_at__gt=now
        ).order_by("next_review_at").first()
        next_review_time = next_word.next_review_at.isoformat() if next_word else None

        return {
            "total_words": total,
            "due_today": due_today + new_words,
            "overdue": overdue,
            "mastered": mastered,
            "learning": learning,
            "new": new_words,
            "next_review_time": next_review_time,
        }

    def bulk_create(self, user_id: UUID, words_data: list[dict]) -> dict:
        created = 0
        skipped = 0
        errors = []

        for item in words_data:
            original_word = item.get("original_word", "").strip().lower()
            if not original_word:
                errors.append({"word": original_word, "error": "Word is required."})
                continue

            if Word.objects.filter(user_id=user_id, original_word__iexact=original_word).exists():
                skipped += 1
                continue

            try:
                Word.objects.create(
                    user_id=user_id,
                    original_word=original_word,
                    translation=item.get("translation", ""),
                    difficulty_level=item.get("difficulty_level", "medium"),
                    notes=item.get("notes", ""),
                    tags=item.get("tags", []),
                )
                created += 1
            except Exception as e:
                errors.append({"word": original_word, "error": str(e)})

        return {"created": created, "skipped": skipped, "errors": errors}

    def get_stats(self, user_id: UUID) -> dict:
        qs = Word.objects.filter(user_id=user_id)
        total = qs.count()
        if total == 0:
            return {
                "total": 0,
                "mastered": 0,
                "learning": 0,
                "new": 0,
                "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
                "by_category": [],
                "average_confidence": 0,
            }

        mastered = qs.filter(is_mastered=True).count()
        learning = qs.filter(is_mastered=False, review_count__gt=0).count()
        new_words = qs.filter(review_count=0).count()

        by_difficulty = {}
        for level in ("easy", "medium", "hard"):
            by_difficulty[level] = qs.filter(difficulty_level=level).count()

        by_category = list(
            qs.values("category__name", "category__color", "category__icon")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        by_category_formatted = [
            {
                "name": c["category__name"] or "Uncategorized",
                "color": c["category__color"] or "#6C5CE7",
                "icon": c["category__icon"] or "book",
                "count": c["count"],
            }
            for c in by_category
        ]

        avg_confidence = qs.aggregate(avg=Avg("confidence_score"))["avg"] or 0

        return {
            "total": total,
            "mastered": mastered,
            "learning": learning,
            "new": new_words,
            "by_difficulty": by_difficulty,
            "by_category": by_category_formatted,
            "average_confidence": round(avg_confidence, 1),
        }


class DjangoWordCategoryRepository(AbstractWordCategoryRepository):
    """Concrete implementation of AbstractWordCategoryRepository."""

    def _to_entity(self, cat: WordCategory) -> WordCategoryEntity:
        return WordCategoryEntity(
            id=cat.id,
            user_id=cat.user_id,
            name=cat.name,
            color=cat.color,
            icon=cat.icon,
            words_count=cat.words_count,
            is_active=cat.is_active,
            created_at=cat.created_at,
            updated_at=cat.updated_at,
        )

    def get_all_by_user(self, user_id: UUID) -> list[WordCategoryEntity]:
        qs = WordCategory.objects.filter(user_id=user_id)
        return [self._to_entity(c) for c in qs]

    def create(self, user_id: UUID, **kwargs) -> WordCategoryEntity:
        name = kwargs.get("name", "").strip()
        if WordCategory.objects.filter(user_id=user_id, name__iexact=name).exists():
            raise EntityAlreadyExistsError(f"Category '{name}' already exists.")
        cat = WordCategory.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(cat)

    def delete(self, category_id: UUID, user_id: UUID) -> None:
        try:
            cat = WordCategory.objects.get(id=category_id, user_id=user_id)
        except WordCategory.DoesNotExist:
            raise EntityNotFoundError("Category not found.")
        cat.delete()

    def exists(self, name: str, user_id: UUID) -> bool:
        return WordCategory.objects.filter(
            user_id=user_id, name__iexact=name.strip()
        ).exists()

    def update_words_count(self, category_id: UUID) -> None:
        try:
            cat = WordCategory.objects.get(id=category_id)
        except WordCategory.DoesNotExist:
            raise EntityNotFoundError("Category not found.")
        cat.words_count = Word.objects.filter(category_id=category_id).count()
        cat.save(update_fields=["words_count", "updated_at"])


class DjangoReviewSessionRepository(AbstractReviewSessionRepository):
    """Concrete implementation for ReviewSession."""

    def _to_entity(self, session: ReviewSession) -> ReviewSessionEntity:
        return ReviewSessionEntity(
            id=session.id,
            user_id=session.user_id,
            started_at=session.started_at,
            completed_at=session.completed_at,
            total_words=session.total_words,
            correct_count=session.correct_count,
            incorrect_count=session.incorrect_count,
            average_quality=session.average_quality,
            duration_seconds=session.duration_seconds,
            session_type=session.session_type,
            is_completed=session.is_completed,
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def create(self, user_id: UUID, **kwargs) -> ReviewSessionEntity:
        session = ReviewSession.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(session)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> ReviewSessionEntity:
        try:
            session = ReviewSession.objects.get(id=session_id, user_id=user_id)
            return self._to_entity(session)
        except ReviewSession.DoesNotExist:
            raise EntityNotFoundError("Review session not found.")

    def update(self, session_id: UUID, **kwargs) -> ReviewSessionEntity:
        try:
            session = ReviewSession.objects.get(id=session_id)
        except ReviewSession.DoesNotExist:
            raise EntityNotFoundError("Review session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._to_entity(session)

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[ReviewSessionEntity], int]:
        qs = ReviewSession.objects.filter(user_id=user_id).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        sessions = [self._to_entity(s) for s in qs[start:end]]
        return sessions, total


class DjangoReviewLogRepository(AbstractReviewLogRepository):
    """Concrete implementation for ReviewLog."""

    def _to_entity(self, log: ReviewLog) -> ReviewLogEntity:
        return ReviewLogEntity(
            id=log.id,
            session_id=log.session_id,
            user_id=log.user_id,
            word_id=log.word_id,
            quality=log.quality,
            response_time_ms=log.response_time_ms,
            is_correct=log.is_correct,
            reviewed_at=log.reviewed_at,
            previous_confidence=log.previous_confidence,
            new_confidence=log.new_confidence,
            previous_interval=log.previous_interval,
            new_interval=log.new_interval,
            is_active=log.is_active,
            created_at=log.created_at,
            updated_at=log.updated_at,
        )

    def create(self, **kwargs) -> ReviewLogEntity:
        log = ReviewLog.objects.create(**kwargs)
        return self._to_entity(log)

    def get_by_session(self, session_id: UUID) -> list[ReviewLogEntity]:
        qs = ReviewLog.objects.filter(session_id=session_id).order_by("reviewed_at")
        return [self._to_entity(log) for log in qs]

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[ReviewLogEntity], int]:
        qs = ReviewLog.objects.filter(user_id=user_id).order_by("-reviewed_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        logs = [self._to_entity(log) for log in qs[start:end]]
        return logs, total


class DjangoStreakRepository(AbstractDailyStreakRepository):
    """Concrete implementation for DailyStreak."""

    def _to_entity(self, streak: DailyStreak) -> DailyStreakEntity:
        return DailyStreakEntity(
            id=streak.id,
            user_id=streak.user_id,
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            last_activity_date=streak.last_activity_date,
            streak_frozen_until=streak.streak_frozen_until,
            total_review_days=streak.total_review_days,
            is_active=streak.is_active,
            created_at=streak.created_at,
            updated_at=streak.updated_at,
        )

    def get_or_create(self, user_id: UUID) -> DailyStreakEntity:
        streak, _ = DailyStreak.objects.get_or_create(user_id=user_id)
        return self._to_entity(streak)

    def update(self, streak_id: UUID, **kwargs) -> DailyStreakEntity:
        try:
            streak = DailyStreak.objects.get(id=streak_id)
        except DailyStreak.DoesNotExist:
            raise EntityNotFoundError("Streak not found.")
        for field, value in kwargs.items():
            setattr(streak, field, value)
        streak.save()
        return self._to_entity(streak)


class DjangoDailyActivityRepository(AbstractDailyActivityRepository):
    """Concrete implementation for DailyActivity."""

    def _to_entity(self, activity: DailyActivity) -> DailyActivityEntity:
        return DailyActivityEntity(
            id=activity.id,
            user_id=activity.user_id,
            date=activity.date,
            words_reviewed=activity.words_reviewed,
            words_added=activity.words_added,
            words_mastered=activity.words_mastered,
            correct_answers=activity.correct_answers,
            incorrect_answers=activity.incorrect_answers,
            total_time_seconds=activity.total_time_seconds,
            goal_completed=activity.goal_completed,
            xp_earned=activity.xp_earned,
            is_active=activity.is_active,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
        )

    def get_or_create_today(self, user_id: UUID) -> DailyActivityEntity:
        today = date.today()
        activity, _ = DailyActivity.objects.get_or_create(
            user_id=user_id,
            date=today,
        )
        return self._to_entity(activity)

    def update(self, activity_id: UUID, **kwargs) -> DailyActivityEntity:
        try:
            activity = DailyActivity.objects.get(id=activity_id)
        except DailyActivity.DoesNotExist:
            raise EntityNotFoundError("Activity not found.")
        for field, value in kwargs.items():
            setattr(activity, field, value)
        activity.save()
        return self._to_entity(activity)

    def get_by_date_range(
        self, user_id: UUID, start_date, end_date
    ) -> list[DailyActivityEntity]:
        qs = DailyActivity.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date,
        ).order_by("date")
        return [self._to_entity(a) for a in qs]


class DjangoTestSessionRepository(AbstractTestSessionRepository):
    """Concrete implementation for TestSession."""

    def _to_entity(self, session: TestSession) -> TestSessionEntity:
        return TestSessionEntity(
            id=session.id,
            user_id=session.user_id,
            test_type=session.test_type,
            difficulty=session.difficulty,
            total_questions=session.total_questions,
            correct_answers=session.correct_answers,
            incorrect_answers=session.incorrect_answers,
            score_percentage=session.score_percentage,
            started_at=session.started_at,
            completed_at=session.completed_at,
            duration_seconds=session.duration_seconds,
            is_completed=session.is_completed,
            is_active=session.is_active,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def create(self, user_id: UUID, **kwargs) -> TestSessionEntity:
        session = TestSession.objects.create(user_id=user_id, **kwargs)
        return self._to_entity(session)

    def get_by_id(self, session_id: UUID, user_id: UUID) -> TestSessionEntity:
        try:
            session = TestSession.objects.get(id=session_id, user_id=user_id)
            return self._to_entity(session)
        except TestSession.DoesNotExist:
            raise EntityNotFoundError("Test session not found.")

    def update(self, session_id: UUID, **kwargs) -> TestSessionEntity:
        try:
            session = TestSession.objects.get(id=session_id)
        except TestSession.DoesNotExist:
            raise EntityNotFoundError("Test session not found.")
        for field, value in kwargs.items():
            setattr(session, field, value)
        session.save()
        return self._to_entity(session)

    def get_by_user(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> tuple[list[TestSessionEntity], int]:
        qs = TestSession.objects.filter(user_id=user_id).order_by("-started_at")
        total = qs.count()
        start = (page - 1) * page_size
        end = start + page_size
        sessions = [self._to_entity(s) for s in qs[start:end]]
        return sessions, total


class DjangoTestQuestionRepository(AbstractTestQuestionRepository):
    """Concrete implementation for TestQuestion."""

    def _to_entity(self, q: TestQuestion) -> TestQuestionEntity:
        return TestQuestionEntity(
            id=q.id,
            session_id=q.session_id,
            word_id=q.word_id,
            question_type=q.question_type,
            question_text=q.question_text,
            correct_answer=q.correct_answer,
            options=q.options,
            user_answer=q.user_answer,
            is_correct=q.is_correct,
            response_time_ms=q.response_time_ms,
            explanation=q.explanation,
            order=q.order,
            is_active=q.is_active,
            created_at=q.created_at,
            updated_at=q.updated_at,
        )

    def create(self, **kwargs) -> TestQuestionEntity:
        q = TestQuestion.objects.create(**kwargs)
        return self._to_entity(q)

    def bulk_create(self, questions_data: list[dict]) -> list[TestQuestionEntity]:
        questions = [TestQuestion(**data) for data in questions_data]
        created = TestQuestion.objects.bulk_create(questions)
        return [self._to_entity(q) for q in created]

    def get_by_id(self, question_id: UUID) -> TestQuestionEntity:
        try:
            q = TestQuestion.objects.get(id=question_id)
            return self._to_entity(q)
        except TestQuestion.DoesNotExist:
            raise EntityNotFoundError("Test question not found.")

    def get_by_session(self, session_id: UUID) -> list[TestQuestionEntity]:
        qs = TestQuestion.objects.filter(session_id=session_id).order_by("order")
        return [self._to_entity(q) for q in qs]

    def update(self, question_id: UUID, **kwargs) -> TestQuestionEntity:
        try:
            q = TestQuestion.objects.get(id=question_id)
        except TestQuestion.DoesNotExist:
            raise EntityNotFoundError("Test question not found.")
        for field, value in kwargs.items():
            setattr(q, field, value)
        q.save()
        return self._to_entity(q)


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
