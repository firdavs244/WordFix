"""
Learning Profile Domain Service.

Pure business logic for analyzing learning styles, optimal study times,
and difficulty adjustment. No Django/ORM imports.
"""


class LearningProfileService:
    """Service for analysing and adjusting a user's learning profile."""

    # Weight maps for each learning style
    _STYLE_WEIGHTS = {
        "visual": {"word_match": 0.3, "word_context": 0.3, "review": 0.2, "test": 0.2},
        "auditory": {"listening_challenge": 0.4, "story_builder": 0.2, "review": 0.2, "test": 0.2},
        "reading": {"review": 0.3, "test": 0.3, "word_context": 0.2, "story_builder": 0.2},
        "kinesthetic": {"speed_round": 0.3, "word_match": 0.3, "game": 0.2, "test": 0.2},
    }

    def analyze_learning_style(self, user_stats: dict) -> dict:
        """
        Determine the user's preferred learning style from their activity data.

        Args:
            user_stats: dict with keys such as review_accuracy, test_accuracy,
                        game_scores (dict of game_type → score), listening_accuracy,
                        session_counts (dict of activity_type → count).

        Returns:
            dict with 'style', 'confidence', 'breakdown'.
        """
        review_acc = user_stats.get("review_accuracy", 0)
        test_acc = user_stats.get("test_accuracy", 0)
        game_scores = user_stats.get("game_scores", {})
        listening_acc = user_stats.get("listening_accuracy", 0)

        style_scores: dict[str, float] = {}
        for style, weights in self._STYLE_WEIGHTS.items():
            score = 0.0
            for activity, weight in weights.items():
                if activity == "review":
                    score += review_acc * weight
                elif activity == "test":
                    score += test_acc * weight
                elif activity == "listening_challenge":
                    score += listening_acc * weight
                elif activity == "game":
                    avg_game = sum(game_scores.values()) / max(len(game_scores), 1)
                    score += avg_game * weight
                else:
                    score += game_scores.get(activity, 0) * weight
            style_scores[style] = round(score, 4)

        best_style = max(style_scores, key=style_scores.get)
        best_val = style_scores[best_style]
        total = sum(style_scores.values()) or 1
        confidence = round(best_val / total, 2) if total else 0.0

        return {
            "style": best_style,
            "confidence": min(confidence, 1.0),
            "breakdown": style_scores,
        }

    def calculate_optimal_time(self, performances: list[dict]) -> dict:
        """
        Determine the best hours and days for studying.

        Args:
            performances: list of dicts with 'hour', 'day', 'effectiveness'.

        Returns:
            dict with 'best_hours' (list[int], top 3), 'best_days' (list[int]),
            'confidence' (float 0-1).
        """
        if not performances:
            return {
                "best_hours": [9, 10, 11],
                "best_days": [0, 1, 2, 3, 4],
                "confidence": 0.0,
            }

        # ---- Hourly effectiveness ---
        hour_data: dict[int, list[float]] = {}
        day_data: dict[int, list[float]] = {}
        for p in performances:
            h = p.get("hour", 0)
            d = p.get("day", 0)
            eff = p.get("effectiveness", 0)
            hour_data.setdefault(h, []).append(eff)
            day_data.setdefault(d, []).append(eff)

        hour_avg = {h: sum(v) / len(v) for h, v in hour_data.items()}
        day_avg = {d: sum(v) / len(v) for d, v in day_data.items()}

        best_hours = sorted(hour_avg, key=hour_avg.get, reverse=True)[:3]
        # Days where avg > overall mean
        overall_day_mean = sum(day_avg.values()) / max(len(day_avg), 1)
        best_days = sorted(
            [d for d, avg in day_avg.items() if avg >= overall_day_mean]
        )
        if not best_days:
            best_days = [0, 1, 2, 3, 4]

        confidence = min(len(performances) / 50, 1.0)

        return {
            "best_hours": best_hours,
            "best_days": best_days,
            "confidence": round(confidence, 2),
        }

    def calculate_difficulty_adjustment(
        self,
        current_level: float,
        recent_accuracy: float,
        rate: float = 0.05,
    ) -> float:
        """
        Adjust difficulty based on recent accuracy.

        Args:
            current_level: current difficulty 0-1.
            recent_accuracy: recent accuracy 0-1.
            rate: adjustment step.

        Returns:
            New difficulty level clamped to [0, 1].
        """
        if recent_accuracy > 0.8:
            new_level = current_level + rate
        elif recent_accuracy < 0.5:
            new_level = current_level - rate
        else:
            new_level = current_level
        return round(max(0.0, min(1.0, new_level)), 4)
