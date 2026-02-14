"""
Mistake Pattern Domain Service.

Pure business logic for detecting recurring error patterns.
No Django/ORM imports.
"""


class MistakePatternService:
    """Service for detecting and categorising mistake patterns."""

    PATTERN_RULES: dict[str, list[tuple[str, str, str]]] = {
        "l1_interference": [
            ("am agree", "agree", "Remove 'am' before verbs"),
            ("i am agree", "i agree", "Remove 'am' before verbs"),
            ("he have", "he has", "Third person singular 'has'"),
            ("she have", "she has", "Third person singular 'has'"),
            ("i am like", "i like", "Remove 'am' before verbs"),
            ("informations", "information", "Uncountable noun"),
            ("advices", "advice", "Uncountable noun"),
            ("furnitures", "furniture", "Uncountable noun"),
        ],
        "morphological": [
            ("goed", "went", "Irregular past tense"),
            ("maked", "made", "Irregular past tense"),
            ("taked", "took", "Irregular past tense"),
            ("runned", "ran", "Irregular past tense"),
            ("childs", "children", "Irregular plural"),
            ("mans", "men", "Irregular plural"),
            ("womans", "women", "Irregular plural"),
            ("tooths", "teeth", "Irregular plural"),
        ],
        "semantic": [
            ("borrow", "lend", "Direction of transfer"),
            ("lend", "borrow", "Direction of transfer"),
            ("rob", "steal", "Target vs. object"),
            ("steal", "rob", "Target vs. object"),
            ("say", "tell", "Direct vs. indirect speech"),
            ("tell", "say", "Direct vs. indirect speech"),
            ("learn", "teach", "Direction of knowledge transfer"),
            ("teach", "learn", "Direction of knowledge transfer"),
        ],
    }

    def detect_pattern(
        self,
        wrong_answer: str,
        correct_answer: str,
        context: str = "",
    ) -> dict | None:
        """
        Detect which error pattern (if any) matches the wrong answer.

        Args:
            wrong_answer: what the user answered.
            correct_answer: the expected answer.
            context: optional surrounding text.

        Returns:
            dict with 'type', 'description', 'related_words', 'example'
            or None if no pattern detected.
        """
        wrong_lower = wrong_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()

        # Check known rule patterns
        for pattern_type, rules in self.PATTERN_RULES.items():
            for wrong_form, correct_form, description in rules:
                if wrong_lower == wrong_form or wrong_form in wrong_lower:
                    if correct_lower == correct_form or correct_form in correct_lower:
                        return {
                            "type": pattern_type,
                            "description": description,
                            "related_words": [wrong_form, correct_form],
                            "example": {
                                "wrong": wrong_answer,
                                "correct": correct_answer,
                                "context": context,
                            },
                        }

        # Spelling error check (Levenshtein distance <= 2)
        if self._levenshtein(wrong_lower, correct_lower) <= 2 and wrong_lower != correct_lower:
            return {
                "type": "spelling",
                "description": f"Spelling error: '{wrong_answer}' → '{correct_answer}'",
                "related_words": [wrong_answer, correct_answer],
                "example": {
                    "wrong": wrong_answer,
                    "correct": correct_answer,
                    "context": context,
                },
            }

        return None

    def get_drill_for_pattern(self, pattern_type: str) -> dict:
        """
        Return an appropriate drill type for a given pattern.

        Args:
            pattern_type: one of the PATTERN_TYPE_CHOICES values.

        Returns:
            dict with 'type', 'instructions', 'focus'.
        """
        drills = {
            "l1_interference": {
                "type": "fill_blank",
                "instructions": "Choose the correct English form (avoid native-language patterns).",
                "focus": "natural English structure",
            },
            "morphological": {
                "type": "conjugation",
                "instructions": "Practice irregular forms until they become automatic.",
                "focus": "irregular verbs and plurals",
            },
            "semantic": {
                "type": "context_match",
                "instructions": "Match the word to the correct context.",
                "focus": "meaning distinction",
            },
            "phonological": {
                "type": "listening",
                "instructions": "Listen and choose the correct word.",
                "focus": "sound distinction",
            },
            "spelling": {
                "type": "typing",
                "instructions": "Type the correct spelling of the word.",
                "focus": "accurate spelling",
            },
            "collocation": {
                "type": "matching",
                "instructions": "Match word pairs that commonly go together.",
                "focus": "natural word combinations",
            },
            "grammar": {
                "type": "fill_blank",
                "instructions": "Choose the grammatically correct option.",
                "focus": "grammar rules",
            },
        }
        return drills.get(pattern_type, {
            "type": "multiple_choice",
            "instructions": "Select the correct answer.",
            "focus": "general practice",
        })

    @staticmethod
    def _levenshtein(s1: str, s2: str) -> int:
        """Compute the Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return MistakePatternService._levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev[j + 1] + 1
                deletions = curr[j] + 1
                substitutions = prev[j] + (c1 != c2)
                curr.append(min(insertions, deletions, substitutions))
            prev = curr
        return prev[-1]
