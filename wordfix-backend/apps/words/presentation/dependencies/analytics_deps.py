"""
Analytics use-case factories.
"""

from apps.words.application.use_cases import (
    GetAnalyticsOverviewUseCase,
    GetDifficultWordsUseCase,
    GetMonthlyStatsUseCase,
    GetStudyCalendarUseCase,
    GetWeeklyStatsUseCase,
    GetWordProgressUseCase,
)
from .common_deps import (
    get_activity_repository,
    get_streak_repository,
    get_user_repository,
    get_word_repository,
)


def get_analytics_overview_use_case() -> GetAnalyticsOverviewUseCase:
    return GetAnalyticsOverviewUseCase(
        word_repo=get_word_repository(),
        user_repo=get_user_repository(),
        streak_repo=get_streak_repository(),
        activity_repo=get_activity_repository(),
    )


def get_weekly_stats_use_case() -> GetWeeklyStatsUseCase:
    return GetWeeklyStatsUseCase(activity_repo=get_activity_repository())


def get_monthly_stats_use_case() -> GetMonthlyStatsUseCase:
    return GetMonthlyStatsUseCase(activity_repo=get_activity_repository())


def get_difficult_words_use_case() -> GetDifficultWordsUseCase:
    return GetDifficultWordsUseCase(word_repo=get_word_repository())


def get_word_progress_use_case() -> GetWordProgressUseCase:
    return GetWordProgressUseCase(word_repo=get_word_repository())


def get_study_calendar_use_case() -> GetStudyCalendarUseCase:
    return GetStudyCalendarUseCase(activity_repo=get_activity_repository())
