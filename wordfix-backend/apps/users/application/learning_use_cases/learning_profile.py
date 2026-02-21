"""
Learning Profile use cases – profile analysis, difficulty adjustment.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

logger = logging.getLogger(__name__)


class GetLearningProfileUseCase:
    """Return a user's learning profile, creating one if absent."""

    def __init__(self, profile_repo):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID) -> dict:
        profile = self.profile_repo.get_or_create(user_id)

        # Build analysis_data-based skills or use flat fields
        analysis = getattr(profile, "analysis_data", None) or {}
        skills_data = analysis.get("skills", {})
        skills_scores = skills_data.get("all", {}) if isinstance(skills_data, dict) else {}

        return {
            "id": str(profile.id),
            "user_id": str(profile.user_id),
            "preferred_style": profile.preferred_style,
            "style_confidence": profile.style_confidence,
            "difficulty_level": profile.current_difficulty_level,
            "best_time": {
                "start_hour": profile.best_hour_start or 9,
                "end_hour": profile.best_hour_end or 12,
                "best_days": profile.best_days or [],
            },
            "session_stats": {
                "avg_duration": 15,
                "optimal_words": 20,
                "retention_rate": 0.0,
            },
            "skills": {
                "strongest": profile.strongest_skills or [],
                "weakest": profile.weakest_skills or [],
                "scores": skills_scores,
            },
            "last_analyzed": (
                profile.last_analyzed_at.isoformat() if profile.last_analyzed_at else None
            ),
        }


class AnalyzeLearningProfileUseCase:
    """Analyze user data to determine style and optimal schedule."""

    def __init__(
        self,
        profile_repo,
        performance_repo,
        profile_service,
        word_repo=None,
        review_repo=None,
        game_repo=None,
        test_repo=None,
    ):
        self.profile_repo = profile_repo
        self.performance_repo = performance_repo
        self.profile_service = profile_service
        self.word_repo = word_repo
        self.review_repo = review_repo
        self.game_repo = game_repo
        self.test_repo = test_repo

    def execute(self, user_id: UUID) -> dict:
        profile = self.profile_repo.get_or_create(user_id)

        # 1. Gather stats (protected)
        try:
            stats = self._gather_stats(user_id)
        except Exception:
            logger.warning("Stats gathering failed for user %s, using defaults", user_id)
            stats = {
                "review_accuracy": 0.0,
                "test_accuracy": 0.0,
                "game_scores": {},
                "listening_accuracy": 0.0,
                "session_counts": {},
            }

        # 2. Analyze learning style (protected)
        try:
            style_result = self.profile_service.analyze_learning_style(stats)
        except Exception:
            logger.warning("Learning style analysis failed, using defaults")
            style_result = {"style": "visual", "confidence": 0.0}

        # 3. Optimal time analysis (protected)
        try:
            performances = self.performance_repo.get_recent(user_id, days=30)
            perf_dicts = [
                {
                    "hour": p.hour_of_day,
                    "day": p.day_of_week,
                    "effectiveness": p.effectiveness_score,
                }
                for p in performances
            ]
            time_result = self.profile_service.calculate_optimal_time(perf_dicts)
        except Exception:
            logger.warning("Optimal time calculation failed, using defaults")
            time_result = {
                "best_hours": [9, 10, 11],
                "best_days": [0, 1, 2, 3, 4],
                "confidence": 0.0,
            }

        # 4. Skills assessment (protected)
        try:
            skills = self._assess_skills(stats)
        except Exception:
            logger.warning("Skills assessment failed, using defaults")
            skills = {
                "all": {"vocabulary": 0, "grammar": 0, "listening": 0, "speed": 0, "context": 0},
                "strongest": [],
                "weakest": ["vocabulary", "grammar"],
            }

        # 5. Update profile
        try:
            profile.preferred_style = style_result["style"]
            profile.style_confidence = style_result["confidence"]
            profile.best_hour_start = time_result["best_hours"][0] if time_result.get("best_hours") else 9
            profile.best_hour_end = (
                time_result["best_hours"][-1] if time_result.get("best_hours") else 12
            )
            profile.best_days = time_result.get("best_days", [])
            profile.strongest_skills = skills.get("strongest", [])
            profile.weakest_skills = skills.get("weakest", [])
            profile.last_analyzed_at = datetime.now(timezone.utc)
            profile.analysis_data = {
                "style": style_result,
                "time": time_result,
                "skills": skills,
            }
            self.profile_repo.save(profile)
        except Exception:
            logger.warning("Failed to save profile for user %s", user_id)

        recommendations = []
        if skills.get("weakest"):
            recommendations.append(f"Focus on: {', '.join(skills['weakest'])}")
        if time_result.get("best_hours"):
            hours_str = ", ".join(str(h) for h in time_result["best_hours"])
            recommendations.append(f"Best study hours: {hours_str}")

        return {
            "learning_style": {
                "style": style_result.get("style", "visual"),
                "confidence": style_result.get("confidence", 0.0),
                "breakdown": style_result.get("breakdown", {
                    "visual": 0.25, "auditory": 0.25,
                    "reading": 0.25, "kinesthetic": 0.25,
                }),
            },
            "optimal_time": time_result,
            "skills": {
                "strongest": skills.get("strongest", []),
                "weakest": skills.get("weakest", []),
                "scores": skills.get("all", {}),
            },
            "recommendations": recommendations,
        }

    def _gather_stats(self, user_id: UUID) -> dict:
        """Collect aggregate stats from various repos."""
        stats = {
            "review_accuracy": 0.0,
            "test_accuracy": 0.0,
            "game_scores": {},
            "listening_accuracy": 0.0,
            "session_counts": {},
        }

        performances = self.performance_repo.get_recent(user_id, days=30)
        if not performances:
            return stats

        review_scores = []
        test_scores = []
        game_map: dict[str, list[float]] = {}

        for p in performances:
            if p.session_type == "review":
                review_scores.append(p.accuracy)
            elif p.session_type == "test":
                test_scores.append(p.accuracy)
            elif p.session_type == "game":
                game_map.setdefault("game", []).append(p.accuracy)

        stats["review_accuracy"] = (
            sum(review_scores) / len(review_scores) if review_scores else 0.0
        )
        stats["test_accuracy"] = (
            sum(test_scores) / len(test_scores) if test_scores else 0.0
        )
        for k, v in game_map.items():
            stats["game_scores"][k] = sum(v) / len(v) if v else 0.0
        stats["session_counts"] = {
            "review": len(review_scores),
            "test": len(test_scores),
            "game": sum(len(v) for v in game_map.values()),
        }
        return stats

    def _assess_skills(self, stats: dict) -> dict:
        """Identify strong and weak areas from stats."""
        skills: dict[str, float] = {
            "vocabulary": stats.get("review_accuracy", 0),
            "grammar": stats.get("test_accuracy", 0),
            "listening": stats.get("listening_accuracy", 0),
            "speed": stats.get("game_scores", {}).get("speed_round", 0),
            "context": stats.get("game_scores", {}).get("word_context", 0),
        }

        sorted_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)
        strongest = [s[0] for s in sorted_skills[:2] if s[1] > 0]
        weakest = [s[0] for s in sorted_skills[-2:] if s[1] < 0.8]

        return {
            "all": skills,
            "strongest": strongest,
            "weakest": weakest,
        }


class GetAdaptiveDifficultyUseCase:
    """Get or adjust adaptive difficulty for a user."""

    def __init__(self, profile_repo, profile_service):
        self.profile_repo = profile_repo
        self.profile_service = profile_service

    def execute(self, user_id: UUID, recent_accuracy: float | None = None) -> dict:
        profile = self.profile_repo.get_or_create(user_id)
        old_level = profile.current_difficulty_level
        adjusted = False
        direction = "none"

        if recent_accuracy is not None:
            new_level = self.profile_service.calculate_difficulty_adjustment(
                profile.current_difficulty_level,
                recent_accuracy,
                profile.difficulty_adjustment_rate,
            )
            if new_level != old_level:
                profile.current_difficulty_level = new_level
                self.profile_repo.save(profile)
                adjusted = True
                direction = "up" if new_level > old_level else "down"

        return {
            "difficulty_level": profile.current_difficulty_level,
            "adjusted": adjusted,
            "direction": direction,
        }
