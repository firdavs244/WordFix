"""
Scoring service for immersive game sessions.

Calculates per-turn and overall session scores.
"""


class ImmersiveScoringService:
    """Calculates scores for immersive game sessions."""

    HINT_PENALTIES = {1: 5, 2: 10, 3: 15}  # Percentage penalty per hint level

    def calculate_turn_score(
        self,
        grammar_score: float,
        vocabulary_score: float,
        relevance_score: float,
        hint_level: int = 0,
    ) -> int:
        """Calculate score for a single conversation turn (0-100)."""
        raw = (grammar_score * 40 + vocabulary_score * 30 + relevance_score * 30)
        penalty = self.HINT_PENALTIES.get(hint_level, 0)
        return max(0, int(raw - penalty))

    def calculate_session_scores(
        self,
        turns: list[dict],
        hints_used: int,
        max_turns: int,
    ) -> dict:
        """Calculate final session scores from all turns."""
        if not turns:
            return {
                "fluency_score": 0.0,
                "accuracy_score": 0.0,
                "vocabulary_score": 0.0,
                "task_completion_score": 0.0,
                "total_score": 0,
            }

        grammar_scores = [t.get("grammar_score", 0.0) for t in turns]
        vocab_scores = [t.get("vocabulary_score_turn", 0.0) for t in turns]
        relevance_scores = [t.get("relevance_score", 0.0) for t in turns]

        fluency = sum(grammar_scores) / len(grammar_scores) * 100
        accuracy = sum(grammar_scores) / len(grammar_scores) * 100
        vocabulary = sum(vocab_scores) / len(vocab_scores) * 100
        task_completion = min(len(turns) / max(max_turns, 1), 1.0) * sum(relevance_scores) / len(relevance_scores) * 100

        total_turn_scores = sum(t.get("score", 0) for t in turns)
        max_possible = len(turns) * 100
        total = int(total_turn_scores / max(max_possible, 1) * 100)

        return {
            "fluency_score": round(fluency, 1),
            "accuracy_score": round(accuracy, 1),
            "vocabulary_score": round(vocabulary, 1),
            "task_completion_score": round(task_completion, 1),
            "total_score": total,
        }
