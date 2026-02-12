"""
Analytics use cases.
"""

import calendar
import logging
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from django.core.cache import cache

logger = logging.getLogger(__name__)


class GetAnalyticsOverviewUseCase:
    """Get comprehensive analytics overview for a user."""

    def __init__(self, word_repo, user_repo, streak_repo, activity_repo):
        self.word_repo = word_repo
        self.user_repo = user_repo
        self.streak_repo = streak_repo
        self.activity_repo = activity_repo

    def execute(self, user_id) -> dict:
        user_id = UUID(str(user_id))

        # Check cache (5 min TTL)
        cache_key = f"analytics_overview_{user_id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        # Word stats
        stats = self.word_repo.get_stats(user_id)
        total_words = stats.get("total", 0)
        mastered_words = stats.get("mastered", 0)
        mastered_pct = round((mastered_words / total_words * 100), 1) if total_words > 0 else 0

        # Review stats
        review_stats = self.word_repo.get_review_summary_stats(user_id)
        total_reviews = review_stats.get("total_reviews", 0)
        total_correct = review_stats.get("total_correct", 0)
        overall_accuracy = round((total_correct / total_reviews * 100), 1) if total_reviews > 0 else 0

        # Streak
        streak = self.streak_repo.get_or_create(user_id)

        # Progress
        try:
            from apps.users.infrastructure.repositories import DjangoProgressRepository
            progress_repo = DjangoProgressRepository()
            progress = progress_repo.get_or_create(user_id)
            total_xp = progress.total_xp
            current_level = progress.level
            tests_completed = progress.tests_completed
            games_played = progress.games_played
            total_study_time = progress.total_study_time_seconds
        except Exception:
            total_xp = 0
            current_level = 1
            tests_completed = 0
            games_played = 0
            total_study_time = 0

        # Format study time
        hours = total_study_time // 3600
        minutes = (total_study_time % 3600) // 60
        total_study_time_formatted = f"{hours}h {minutes}m"

        # Calculate avg daily stats
        try:
            user = self.user_repo.get_by_id(user_id)
            member_since = user.date_joined
            from datetime import datetime as dt
            member_since_days = max((datetime.now(timezone.utc) - member_since).days, 1) if member_since else 1
        except Exception:
            member_since_days = 1

        avg_daily_words = round(total_words / member_since_days, 1)
        avg_daily_time = round(total_study_time / member_since_days)

        result = {
            "total_words": total_words,
            "mastered_words": mastered_words,
            "mastered_percentage": mastered_pct,
            "total_reviews": total_reviews,
            "total_correct": total_correct,
            "overall_accuracy": overall_accuracy,
            "total_study_time_formatted": total_study_time_formatted,
            "total_xp": total_xp,
            "current_level": current_level,
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "tests_completed": tests_completed,
            "games_played": games_played,
            "avg_daily_words": avg_daily_words,
            "avg_daily_time": avg_daily_time,
            "member_since_days": member_since_days,
        }

        cache.set(cache_key, result, timeout=300)  # 5 min
        return result


class GetWeeklyStatsUseCase:
    """Get weekly stats (last 7 days)."""

    def __init__(self, activity_repo):
        self.activity_repo = activity_repo

    def execute(self, user_id) -> list[dict]:
        user_id = UUID(str(user_id))

        # Check cache (10 min TTL)
        cache_key = f"weekly_stats_{user_id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        today = date.today()
        start_date = today - timedelta(days=6)

        activities = self.activity_repo.get_by_date_range(user_id, start_date, today)
        activity_map = {a.date: a for a in activities}

        result = []
        for i in range(7):
            d = start_date + timedelta(days=i)
            activity = activity_map.get(d)
            result.append({
                "date": d.isoformat(),
                "words_reviewed": activity.words_reviewed if activity else 0,
                "words_added": activity.words_added if activity else 0,
                "correct": activity.correct_answers if activity else 0,
                "incorrect": activity.incorrect_answers if activity else 0,
                "xp_earned": activity.xp_earned if activity else 0,
                "time_seconds": activity.total_time_seconds if activity else 0,
                "goal_completed": activity.goal_completed if activity else False,
            })

        cache.set(cache_key, result, timeout=600)  # 10 min
        return result


class GetMonthlyStatsUseCase:
    """Get monthly stats (last 30 days)."""

    def __init__(self, activity_repo):
        self.activity_repo = activity_repo

    def execute(self, user_id) -> list[dict]:
        user_id = UUID(str(user_id))
        today = date.today()
        start_date = today - timedelta(days=29)

        activities = self.activity_repo.get_by_date_range(user_id, start_date, today)
        activity_map = {a.date: a for a in activities}

        result = []
        for i in range(30):
            d = start_date + timedelta(days=i)
            activity = activity_map.get(d)
            result.append({
                "date": d.isoformat(),
                "words_reviewed": activity.words_reviewed if activity else 0,
                "words_added": activity.words_added if activity else 0,
                "correct": activity.correct_answers if activity else 0,
                "incorrect": activity.incorrect_answers if activity else 0,
                "xp_earned": activity.xp_earned if activity else 0,
                "time_seconds": activity.total_time_seconds if activity else 0,
                "goal_completed": activity.goal_completed if activity else False,
            })

        return result


class GetDifficultWordsUseCase:
    """Get words with lowest accuracy rate."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id, limit: int = 10) -> list[dict]:
        user_id = UUID(str(user_id))
        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=10000,
        )

        # Filter words that have been reviewed at least once
        reviewed = [w for w in words if w.review_count > 0]
        # Sort by accuracy rate (ascending)
        reviewed.sort(key=lambda w: w.accuracy_rate)

        result = []
        for w in reviewed[:limit]:
            result.append({
                "id": str(w.id),
                "original_word": w.original_word,
                "translation": w.translation,
                "accuracy_rate": w.accuracy_rate,
                "review_count": w.review_count,
                "correct_count": w.correct_count,
                "incorrect_count": w.incorrect_count,
                "confidence_score": w.confidence_score,
            })

        return result


class GetWordProgressUseCase:
    """Get word progress distribution."""

    def __init__(self, word_repo):
        self.word_repo = word_repo

    def execute(self, user_id) -> dict:
        user_id = UUID(str(user_id))

        # Check cache (5 min TTL)
        cache_key = f"word_progress_{user_id}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        words, _ = self.word_repo.get_all_by_user(
            user_id=user_id, page=1, page_size=10000,
        )

        # By confidence
        by_confidence = {"0-25": 0, "25-50": 0, "50-75": 0, "75-100": 0}
        for w in words:
            if w.confidence_score < 25:
                by_confidence["0-25"] += 1
            elif w.confidence_score < 50:
                by_confidence["25-50"] += 1
            elif w.confidence_score < 75:
                by_confidence["50-75"] += 1
            else:
                by_confidence["75-100"] += 1

        # By difficulty
        by_difficulty = {"easy": 0, "medium": 0, "hard": 0}
        for w in words:
            if w.difficulty_level in by_difficulty:
                by_difficulty[w.difficulty_level] += 1

        # By category
        cat_map = {}
        for w in words:
            cat_name = w.category.name if w.category else "Uncategorized"
            if cat_name not in cat_map:
                cat_map[cat_name] = {"name": cat_name, "count": 0, "total_confidence": 0}
            cat_map[cat_name]["count"] += 1
            cat_map[cat_name]["total_confidence"] += w.confidence_score
        by_category = []
        for cat_info in cat_map.values():
            by_category.append({
                "name": cat_info["name"],
                "count": cat_info["count"],
                "avg_confidence": round(cat_info["total_confidence"] / cat_info["count"], 1) if cat_info["count"] > 0 else 0,
            })

        # Recently mastered
        mastered = [w for w in words if w.is_mastered]
        mastered.sort(key=lambda w: w.updated_at or w.created_at, reverse=True)
        recently_mastered = [
            {"id": str(w.id), "original_word": w.original_word, "translation": w.translation}
            for w in mastered[:5]
        ]

        # Needs attention
        reviewed = [w for w in words if w.review_count > 0 and not w.is_mastered]
        reviewed.sort(key=lambda w: w.confidence_score)
        needs_attention = [
            {"id": str(w.id), "original_word": w.original_word, "translation": w.translation,
             "confidence_score": w.confidence_score}
            for w in reviewed[:5]
        ]

        result = {
            "by_confidence": by_confidence,
            "by_difficulty": by_difficulty,
            "by_category": by_category,
            "recently_mastered": recently_mastered,
            "needs_attention": needs_attention,
        }

        cache.set(cache_key, result, timeout=300)  # 5 min
        return result


class GetStudyCalendarUseCase:
    """Get study calendar data (heatmap)."""

    def __init__(self, activity_repo):
        self.activity_repo = activity_repo

    def execute(self, user_id, year: int, month: int) -> list[dict]:
        user_id = UUID(str(user_id))

        _, days_in_month = calendar.monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, days_in_month)

        activities = self.activity_repo.get_by_date_range(user_id, start_date, end_date)
        activity_map = {a.date: a for a in activities}

        result = []
        for day in range(1, days_in_month + 1):
            d = date(year, month, day)
            activity = activity_map.get(d)
            result.append({
                "date": d.isoformat(),
                "active": activity is not None and activity.words_reviewed > 0,
                "words_reviewed": activity.words_reviewed if activity else 0,
                "goal_completed": activity.goal_completed if activity else False,
            })

        return result
