"""
Domain Coverage use case – recalculate coverage per topic domain.
"""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class UpdateDomainCoverageUseCase:
    """Recalculate domain coverage for a user."""

    DOMAIN_KEYWORDS = {
        "academic": ["analyze", "evaluate", "theory", "concept", "research", "hypothesis",
                      "methodology", "evidence", "conclude", "demonstrate"],
        "business": ["profit", "revenue", "market", "invest", "strategy", "negotiate",
                      "budget", "contract", "stakeholder", "competitor"],
        "technology": ["algorithm", "database", "software", "network", "interface",
                        "compile", "debug", "deploy", "server", "protocol"],
        "daily_life": ["breakfast", "kitchen", "weather", "grocery", "neighbour",
                        "schedule", "appointment", "commute", "recipe", "laundry"],
        "science": ["experiment", "molecule", "gravity", "organism", "evolution",
                     "hypothesis", "particle", "equation", "specimen", "catalyst"],
        "arts": ["canvas", "sculpture", "melody", "rhythm", "genre",
                  "portrait", "exhibition", "compose", "aesthetic", "inspiration"],
        "travel": ["passport", "itinerary", "destination", "departure", "accommodation",
                    "currency", "embassy", "luggage", "customs", "boarding"],
        "medical": ["diagnosis", "symptom", "prescription", "surgery", "therapy",
                     "chronic", "immune", "dosage", "patient", "clinic"],
        "legal": ["contract", "verdict", "plaintiff", "legislation", "jurisdiction",
                   "attorney", "testimony", "statute", "amendment", "liability"],
        "social": ["community", "volunteer", "tradition", "celebrate", "cooperate",
                    "negotiate", "empathy", "diversity", "solidarity", "advocate"],
    }

    MAX_DOMAIN_WORDS = 50  # 50 words = 100 % coverage

    def __init__(self, domain_repo, word_repo=None):
        self.domain_repo = domain_repo
        self.word_repo = word_repo

    def execute(self, user_id: UUID) -> dict:
        # Get user's words
        user_words: list[str] = []
        if self.word_repo:
            try:
                words, _ = self.word_repo.get_all_by_user(user_id, page=1, page_size=500)
                user_words = [w.original_word.lower() for w in words if w.original_word]
            except Exception:
                pass

        result = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            coverage_obj = self.domain_repo.get_or_create(user_id, domain)
            matched = [w for w in user_words if w in keywords]
            total = len(matched)
            coverage_pct = min(total / self.MAX_DOMAIN_WORDS * 100, 100.0)

            coverage_obj.total_words_in_domain = total
            coverage_obj.coverage_percentage = round(coverage_pct, 1)
            # Simple mastery: if word exists, count mastered as half
            coverage_obj.mastered_count = total // 2
            coverage_obj.learning_count = total - (total // 2)
            self.domain_repo.save(coverage_obj)

            result[domain] = {
                "total": total,
                "coverage": round(coverage_pct, 1),
                "mastered": coverage_obj.mastered_count,
                "learning": coverage_obj.learning_count,
            }

        return result
