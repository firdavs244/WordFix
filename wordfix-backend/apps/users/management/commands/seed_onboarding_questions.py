"""
Seed onboarding level assessment questions.

18 questions total — 3 per level (A1-C2). Idempotent.
"""

from django.core.management.base import BaseCommand

from apps.users.infrastructure.models import OnboardingQuestion


QUESTIONS = [
    # A1 — Beginner
    {
        "level": "A1",
        "question_text": "What ___ your name?",
        "correct_answer": "is",
        "options": ["is", "are", "am", "do"],
        "order": 1,
    },
    {
        "level": "A1",
        "question_text": "She ___ a student.",
        "correct_answer": "is",
        "options": ["is", "are", "am", "do"],
        "order": 2,
    },
    {
        "level": "A1",
        "question_text": "I ___ from Uzbekistan.",
        "correct_answer": "am",
        "options": ["am", "is", "are", "do"],
        "order": 3,
    },
    # A2 — Elementary
    {
        "level": "A2",
        "question_text": "I ___ to school every day.",
        "correct_answer": "go",
        "options": ["go", "goes", "going", "went"],
        "order": 1,
    },
    {
        "level": "A2",
        "question_text": "She ___ reading a book now.",
        "correct_answer": "is",
        "options": ["is", "are", "am", "does"],
        "order": 2,
    },
    {
        "level": "A2",
        "question_text": "They ___ football yesterday.",
        "correct_answer": "played",
        "options": ["played", "play", "playing", "plays"],
        "order": 3,
    },
    # B1 — Intermediate
    {
        "level": "B1",
        "question_text": "If I ___ rich, I would travel the world.",
        "correct_answer": "were",
        "options": ["were", "am", "was", "be"],
        "order": 1,
    },
    {
        "level": "B1",
        "question_text": "She has ___ here since 2020.",
        "correct_answer": "lived",
        "options": ["lived", "living", "live", "lives"],
        "order": 2,
    },
    {
        "level": "B1",
        "question_text": "The book ___ by millions of people.",
        "correct_answer": "has been read",
        "options": ["has been read", "has read", "reading", "reads"],
        "order": 3,
    },
    # B2 — Upper Intermediate
    {
        "level": "B2",
        "question_text": "Had I known, I ___ differently.",
        "correct_answer": "would have acted",
        "options": ["would have acted", "acted", "will act", "act"],
        "order": 1,
    },
    {
        "level": "B2",
        "question_text": "Not until she left ___ realize her importance.",
        "correct_answer": "did he",
        "options": ["did he", "he did", "he does", "does he"],
        "order": 2,
    },
    {
        "level": "B2",
        "question_text": "The project is worth ___.",
        "correct_answer": "pursuing",
        "options": ["pursuing", "to pursue", "pursue", "pursued"],
        "order": 3,
    },
    # C1 — Advanced
    {
        "level": "C1",
        "question_text": "Hardly ___ arrived when it started raining.",
        "correct_answer": "had he",
        "options": ["had he", "he had", "has he", "he has"],
        "order": 1,
    },
    {
        "level": "C1",
        "question_text": "She demanded that he ___ immediately.",
        "correct_answer": "leave",
        "options": ["leave", "leaves", "left", "leaving"],
        "order": 2,
    },
    {
        "level": "C1",
        "question_text": "The implications ___ far-reaching.",
        "correct_answer": "are deemed",
        "options": ["are deemed", "deemed", "deeming", "to deem"],
        "order": 3,
    },
    # C2 — Proficient
    {
        "level": "C2",
        "question_text": "Were it not for his ___, we would have failed.",
        "correct_answer": "perspicacity",
        "options": ["perspicacity", "reading", "view", "idea"],
        "order": 1,
    },
    {
        "level": "C2",
        "question_text": "___ notwithstanding, the law prevails.",
        "correct_answer": "Objections",
        "options": ["Objections", "Although", "Despite", "However"],
        "order": 2,
    },
    {
        "level": "C2",
        "question_text": "The argument is ___ at best.",
        "correct_answer": "specious",
        "options": ["specious", "special", "specific", "spectacular"],
        "order": 3,
    },
]


class Command(BaseCommand):
    help = "Seed onboarding level assessment questions (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for q_data in QUESTIONS:
            _, was_created = OnboardingQuestion.objects.update_or_create(
                level=q_data["level"],
                order=q_data["order"],
                defaults={
                    "question_text": q_data["question_text"],
                    "correct_answer": q_data["correct_answer"],
                    "options": q_data["options"],
                },
            )
            if was_created:
                created += 1

        total = OnboardingQuestion.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Done: {created} created, {total} total onboarding questions."
            )
        )
