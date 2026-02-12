"""
Management command: seed_test_data

Seeds a test user with full data for testing all features.
Idempotent — safe to run multiple times.
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.infrastructure.models import (
    Badge,
    CustomUser,
    Notification,
    UserBadge,
    UserProgress,
    XPTransaction,
)
from apps.words.infrastructure.models import (
    ConfusingPair,
    DailyActivity,
    DailyChallenge,
    DailyStreak,
    Word,
    WordCategory,
)


WORDS_DATA = [
    # Daily Life (10) — easy/medium mix
    {"original_word": "abandon", "translation": "tark etmoq", "part_of_speech": "verb", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "To give up completely.", "example_sentence": "He decided to abandon the project.",
     "synonyms": ["desert", "forsake", "leave"], "antonyms": ["keep", "retain", "maintain"]},
    {"original_word": "beneath", "translation": "ostida", "part_of_speech": "preposition", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "In or to a lower position; under.", "example_sentence": "The cat hid beneath the table.",
     "synonyms": ["under", "below", "underneath"], "antonyms": ["above", "over", "atop"]},
    {"original_word": "enormous", "translation": "ulkan", "part_of_speech": "adjective", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "Very large in size, quantity, or extent.", "example_sentence": "The elephant was enormous.",
     "synonyms": ["huge", "vast", "immense"], "antonyms": ["tiny", "small", "minute"]},
    {"original_word": "valid", "translation": "haqiqiy/amalda", "part_of_speech": "adjective", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "Having a sound basis in logic or fact.", "example_sentence": "Your passport is still valid.",
     "synonyms": ["legitimate", "legal", "authentic"], "antonyms": ["invalid", "void", "null"]},
    {"original_word": "achieve", "translation": "erishmoq", "part_of_speech": "verb", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "Successfully bring about or reach a desired objective.", "example_sentence": "She achieved her goal of running a marathon.",
     "synonyms": ["accomplish", "attain", "reach"], "antonyms": ["fail", "miss", "lose"]},
    {"original_word": "brilliant", "translation": "yorqin/aqlli", "part_of_speech": "adjective", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "Exceptionally clever or talented.", "example_sentence": "She is a brilliant scientist.",
     "synonyms": ["bright", "clever", "genius"], "antonyms": ["dull", "stupid", "dim"]},
    {"original_word": "feature", "translation": "xususiyat", "part_of_speech": "noun", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "A distinctive attribute or aspect of something.", "example_sentence": "The phone has many useful features.",
     "synonyms": ["characteristic", "trait", "attribute"], "antonyms": []},
    {"original_word": "gather", "translation": "to'plamoq", "part_of_speech": "verb", "difficulty_level": "easy", "category": "Daily Life",
     "definition": "Come together; assemble or accumulate.", "example_sentence": "We gathered around the campfire.",
     "synonyms": ["collect", "assemble", "accumulate"], "antonyms": ["scatter", "disperse", "spread"]},
    {"original_word": "frequent", "translation": "tez-tez", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Daily Life",
     "definition": "Occurring or done many times at short intervals.", "example_sentence": "He is a frequent visitor to the library.",
     "synonyms": ["regular", "common", "repeated"], "antonyms": ["rare", "infrequent", "occasional"]},
    {"original_word": "keen", "translation": "ishtiyoqli", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Daily Life",
     "definition": "Having or showing eagerness or enthusiasm.", "example_sentence": "She is keen to learn new languages.",
     "synonyms": ["eager", "enthusiastic", "passionate"], "antonyms": ["indifferent", "apathetic", "reluctant"]},

    # Academic (10) — medium/hard
    {"original_word": "capture", "translation": "qo'lga olmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Academic",
     "definition": "Take into one's possession or control by force.", "example_sentence": "The soldiers captured the enemy stronghold.",
     "synonyms": ["seize", "catch", "apprehend"], "antonyms": ["release", "free", "liberate"]},
    {"original_word": "durable", "translation": "chidamli", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Academic",
     "definition": "Able to withstand wear, pressure, or damage.", "example_sentence": "This material is very durable.",
     "synonyms": ["sturdy", "robust", "lasting"], "antonyms": ["fragile", "flimsy", "delicate"]},
    {"original_word": "genuine", "translation": "haqiqiy", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Academic",
     "definition": "Truly what something is said to be; authentic.", "example_sentence": "Is this a genuine diamond?",
     "synonyms": ["authentic", "real", "true"], "antonyms": ["fake", "counterfeit", "artificial"]},
    {"original_word": "launch", "translation": "ishga tushirmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Academic",
     "definition": "Start or set in motion.", "example_sentence": "They plan to launch the new product next month.",
     "synonyms": ["start", "begin", "initiate"], "antonyms": ["end", "stop", "halt"]},
    {"original_word": "obstacle", "translation": "to'siq", "part_of_speech": "noun", "difficulty_level": "medium", "category": "Academic",
     "definition": "A thing that blocks one's way or prevents progress.", "example_sentence": "Lack of funding is a major obstacle.",
     "synonyms": ["barrier", "hindrance", "hurdle"], "antonyms": ["aid", "help", "advantage"]},
    {"original_word": "persuade", "translation": "ishontirmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Academic",
     "definition": "Cause someone to do something through reasoning.", "example_sentence": "She persuaded him to change his mind.",
     "synonyms": ["convince", "influence", "sway"], "antonyms": ["discourage", "dissuade", "deter"]},
    {"original_word": "inevitable", "translation": "muqarrar", "part_of_speech": "adjective", "difficulty_level": "hard", "category": "Academic",
     "definition": "Certain to happen; unavoidable.", "example_sentence": "Change is inevitable in any growing company.",
     "synonyms": ["unavoidable", "certain", "inescapable"], "antonyms": ["avoidable", "uncertain", "preventable"]},
    {"original_word": "juvenile", "translation": "o'smir", "part_of_speech": "adjective", "difficulty_level": "hard", "category": "Academic",
     "definition": "Of, for, or relating to young people.", "example_sentence": "The juvenile offender was given a warning.",
     "synonyms": ["young", "youthful", "adolescent"], "antonyms": ["adult", "mature", "grown-up"]},
    {"original_word": "negotiate", "translation": "muzokara qilmoq", "part_of_speech": "verb", "difficulty_level": "hard", "category": "Academic",
     "definition": "Try to reach an agreement or compromise by discussion.", "example_sentence": "They negotiated a peace treaty.",
     "synonyms": ["discuss", "bargain", "mediate"], "antonyms": ["dictate", "demand", "impose"]},
    {"original_word": "yield", "translation": "natija bermoq", "part_of_speech": "verb", "difficulty_level": "hard", "category": "Academic",
     "definition": "Produce or provide a result or gain.", "example_sentence": "The investment yielded high returns.",
     "synonyms": ["produce", "generate", "provide"], "antonyms": ["withhold", "deny", "refuse"]},

    # Emotions (10) — medium/hard
    {"original_word": "hesitate", "translation": "ikkilanmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Pause before saying or doing something.", "example_sentence": "Don't hesitate to ask for help.",
     "synonyms": ["pause", "waver", "falter"], "antonyms": ["decide", "resolve", "proceed"]},
    {"original_word": "magnificent", "translation": "ajoyib", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Extremely beautiful, elaborate, or impressive.", "example_sentence": "The view from the mountain was magnificent.",
     "synonyms": ["splendid", "grand", "glorious"], "antonyms": ["ordinary", "modest", "plain"]},
    {"original_word": "tremendous", "translation": "ulkan", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Very great in amount, scale, or intensity.", "example_sentence": "She made a tremendous effort to finish.",
     "synonyms": ["enormous", "immense", "vast"], "antonyms": ["tiny", "slight", "negligible"]},
    {"original_word": "ultimate", "translation": "yakuniy", "part_of_speech": "adjective", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Being or happening at the end of a process; final.", "example_sentence": "The ultimate goal is world peace.",
     "synonyms": ["final", "last", "supreme"], "antonyms": ["initial", "first", "beginning"]},
    {"original_word": "wander", "translation": "sarson yurmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Walk or move in a leisurely or aimless way.", "example_sentence": "We wandered through the old town.",
     "synonyms": ["roam", "stroll", "drift"], "antonyms": ["stay", "settle", "remain"]},
    {"original_word": "collapse", "translation": "qulamoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Suddenly fall down or give way.", "example_sentence": "The building collapsed during the earthquake.",
     "synonyms": ["fall", "crumble", "break down"], "antonyms": ["stand", "rise", "build"]},
    {"original_word": "disaster", "translation": "falokat", "part_of_speech": "noun", "difficulty_level": "medium", "category": "Emotions",
     "definition": "A sudden event causing great damage or suffering.", "example_sentence": "The flood was a major disaster.",
     "synonyms": ["catastrophe", "calamity", "tragedy"], "antonyms": ["blessing", "fortune", "miracle"]},
    {"original_word": "emerge", "translation": "paydo bo'lmoq", "part_of_speech": "verb", "difficulty_level": "medium", "category": "Emotions",
     "definition": "Move out of or away from something and become visible.", "example_sentence": "A new leader emerged from the crisis.",
     "synonyms": ["appear", "surface", "arise"], "antonyms": ["disappear", "vanish", "hide"]},
    {"original_word": "reluctant", "translation": "istaksiz", "part_of_speech": "adjective", "difficulty_level": "hard", "category": "Emotions",
     "definition": "Unwilling and hesitant; disinclined.", "example_sentence": "He was reluctant to admit his mistake.",
     "synonyms": ["unwilling", "hesitant", "resistant"], "antonyms": ["willing", "eager", "enthusiastic"]},
    {"original_word": "severe", "translation": "og'ir/qattiq", "part_of_speech": "adjective", "difficulty_level": "hard", "category": "Emotions",
     "definition": "Very great; intense.", "example_sentence": "The region suffered severe flooding.",
     "synonyms": ["harsh", "intense", "extreme"], "antonyms": ["mild", "gentle", "moderate"]},
]

CATEGORIES_DATA = {
    "Daily Life": {"color": "#6C5CE7", "icon": "home"},
    "Academic": {"color": "#00CEC9", "icon": "book-open"},
    "Emotions": {"color": "#FDCB6E", "icon": "heart"},
}

BADGES_DATA = [
    {"code": "first_word", "name": "First Word", "description": "Add your first word", "icon": "star", "category": "words", "rarity": "common", "xp_reward": 10},
    {"code": "word_10", "name": "Vocabulary Builder", "description": "Add 10 words", "icon": "book", "category": "words", "rarity": "common", "xp_reward": 25},
    {"code": "word_50", "name": "Word Collector", "description": "Add 50 words", "icon": "library", "category": "words", "rarity": "rare", "xp_reward": 50},
    {"code": "streak_3", "name": "On Fire", "description": "3-day streak", "icon": "flame", "category": "streak", "rarity": "common", "xp_reward": 15},
    {"code": "streak_7", "name": "Week Warrior", "description": "7-day streak", "icon": "zap", "category": "streak", "rarity": "rare", "xp_reward": 50},
    {"code": "streak_30", "name": "Monthly Champion", "description": "30-day streak", "icon": "trophy", "category": "streak", "rarity": "epic", "xp_reward": 200},
    {"code": "review_10", "name": "Reviewer", "description": "Complete 10 reviews", "icon": "check-circle", "category": "review", "rarity": "common", "xp_reward": 20},
    {"code": "perfect_review", "name": "Perfect Review", "description": "Get 100% in a review session", "icon": "award", "category": "review", "rarity": "rare", "xp_reward": 30},
    {"code": "test_first", "name": "Test Taker", "description": "Complete your first test", "icon": "clipboard", "category": "test", "rarity": "common", "xp_reward": 15},
    {"code": "test_perfect", "name": "Perfect Score", "description": "Score 100% on a test", "icon": "target", "category": "test", "rarity": "epic", "xp_reward": 100},
    {"code": "game_first", "name": "Player One", "description": "Play your first game", "icon": "play", "category": "game", "rarity": "common", "xp_reward": 10},
    {"code": "mastery_5", "name": "Master of Five", "description": "Master 5 words", "icon": "crown", "category": "mastery", "rarity": "rare", "xp_reward": 50},
    {"code": "level_5", "name": "Level 5", "description": "Reach level 5", "icon": "trending-up", "category": "level", "rarity": "common", "xp_reward": 25},
    {"code": "level_10", "name": "Level 10", "description": "Reach level 10", "icon": "arrow-up", "category": "level", "rarity": "rare", "xp_reward": 75},
]


class Command(BaseCommand):
    help = "Seed test data: user, words, categories, progress, streak, daily activities, badges, notifications"

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()

        # ─── 1. Create or get user ───
        try:
            user = CustomUser.objects.get(email="test@wordfix.com")
            self.stdout.write(self.style.WARNING("User test@wordfix.com already exists, skipping..."))
        except CustomUser.DoesNotExist:
            # Check if username exists
            username = "testuser"
            if CustomUser.objects.filter(username=username).exists():
                # Delete the old user with this username to avoid conflicts
                CustomUser.objects.filter(username=username).delete()
            user = CustomUser.objects.create_user(
                email="test@wordfix.com",
                username=username,
                password="TestPass123!",
                full_name="Test User",
                native_language="uz",
                learning_language="en",
                proficiency_level="B1",
                daily_goal=10,
            )
            self.stdout.write(self.style.SUCCESS("Created user: test@wordfix.com"))

        # ─── 2. Create badges (global) ───
        badges_created = 0
        for badge_data in BADGES_DATA:
            _, b_created = Badge.objects.get_or_create(
                code=badge_data["code"],
                defaults=badge_data,
            )
            if b_created:
                badges_created += 1
        if badges_created:
            self.stdout.write(self.style.SUCCESS(f"Created {badges_created} badges"))

        # ─── 3. Create categories ───
        categories = {}
        for cat_name, cat_info in CATEGORIES_DATA.items():
            cat, _ = WordCategory.objects.get_or_create(
                user=user,
                name=cat_name,
                defaults={"color": cat_info["color"], "icon": cat_info["icon"]},
            )
            categories[cat_name] = cat

        # ─── 4. Create words ───
        words_created = 0
        enriched_indices = set(random.sample(range(30), 10))  # 10 enriched

        mastered_indices = set(random.sample(range(30), 5))  # 5 mastered

        all_words = []
        for i, wd in enumerate(WORDS_DATA):
            cat_name = wd.pop("category")
            syns = wd.pop("synonyms", [])
            ants = wd.pop("antonyms", [])
            defn = wd.pop("definition", "")
            example = wd.pop("example_sentence", "")

            is_enriched = i in enriched_indices
            is_mastered = i in mastered_indices

            review_count = random.randint(0, 15)
            correct_count = int(review_count * random.uniform(0.4, 0.8))
            incorrect_count = review_count - correct_count
            confidence = random.uniform(95, 100) if is_mastered else random.uniform(0, 80)

            # Some words due for review (next_review_at in past or today)
            if i % 3 == 0:
                next_review = now - timedelta(hours=random.randint(1, 48))
            elif i % 3 == 1:
                next_review = now + timedelta(days=random.randint(1, 14))
            else:
                next_review = None

            word_defaults = {
                "translation": wd["translation"],
                "part_of_speech": wd["part_of_speech"],
                "difficulty_level": wd["difficulty_level"],
                "category": categories.get(cat_name),
                "synonyms": syns if is_enriched else [],
                "antonyms": ants if is_enriched else [],
                "definition": defn if is_enriched else "",
                "example_sentence": example if is_enriched else "",
                "is_enriched": is_enriched,
                "enrichment_status": "enriched" if is_enriched else "pending",
                "enriched_at": now if is_enriched else None,
                "mnemonic": f"Think of '{wd['original_word']}' as related to {syns[0] if syns else wd['translation']}" if is_enriched else "",
                "confidence_score": round(confidence, 1),
                "review_count": review_count,
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "next_review_at": next_review,
                "is_mastered": is_mastered,
                "last_reviewed_at": now - timedelta(hours=random.randint(1, 72)) if review_count > 0 else None,
            }

            word, w_created = Word.objects.get_or_create(
                user=user,
                original_word=wd["original_word"],
                defaults=word_defaults,
            )
            if w_created:
                words_created += 1
            all_words.append(word)

        # Update category word counts
        for cat_name, cat_obj in categories.items():
            count = Word.objects.filter(user=user, category=cat_obj).count()
            cat_obj.words_count = count
            cat_obj.save(update_fields=["words_count"])

        self.stdout.write(self.style.SUCCESS(f"Created {words_created} words in {len(categories)} categories"))

        # ─── 5. Confusing pairs ───
        pairs_created = 0
        pairs_data = [
            ("genuine", "generous"),
            ("abandon", "abundant"),
            ("inevitable", "ultimate"),
        ]
        for w1_str, w2_str in pairs_data:
            try:
                w1 = Word.objects.get(user=user, original_word=w1_str)
                w2 = Word.objects.get(user=user, original_word=w2_str)
                _, cp_created = ConfusingPair.objects.get_or_create(
                    user=user, word_1=w1, word_2=w2,
                    defaults={"confusion_count": random.randint(2, 8)},
                )
                if cp_created:
                    pairs_created += 1
            except Word.DoesNotExist:
                pass
        if pairs_created:
            self.stdout.write(self.style.SUCCESS(f"Created {pairs_created} confusing pairs"))

        # ─── 6. User progress ───
        progress, _ = UserProgress.objects.update_or_create(
            user=user,
            defaults={
                "total_xp": 750,
                "level": 5,
                "words_learned_total": 30,
                "words_mastered_total": 5,
                "tests_completed": 3,
                "games_played": 2,
                "reviews_completed": 15,
                "perfect_scores": 1,
                "total_study_time_seconds": 3600,
            },
        )

        # ─── 7. Daily streak ───
        DailyStreak.objects.update_or_create(
            user=user,
            defaults={
                "current_streak": 3,
                "longest_streak": 7,
                "last_activity_date": today,
                "total_review_days": 15,
            },
        )

        # ─── 8. Daily activities (last 7 days) ───
        for day_offset in range(7):
            date = today - timedelta(days=day_offset)
            words_reviewed = random.randint(3, 10)
            correct = random.randint(2, min(8, words_reviewed))
            xp = random.randint(20, 80)
            DailyActivity.objects.update_or_create(
                user=user,
                date=date,
                defaults={
                    "words_reviewed": words_reviewed,
                    "words_added": random.randint(0, 3),
                    "words_mastered": random.randint(0, 1),
                    "correct_answers": correct,
                    "incorrect_answers": words_reviewed - correct,
                    "total_time_seconds": random.randint(300, 1200),
                    "goal_completed": words_reviewed >= 10,
                    "xp_earned": xp,
                },
            )

        # ─── 9. XP transactions ───
        if not XPTransaction.objects.filter(user=user).exists():
            xp_reasons = [
                ("word_added", 50, "Added 10 words"),
                ("review_correct", 100, "Review correct answers"),
                ("review_complete", 75, "Completed review sessions"),
                ("test_complete", 150, "Completed tests"),
                ("game_complete", 100, "Completed games"),
                ("daily_goal", 75, "Daily goals achieved"),
                ("streak_7", 50, "7-day streak bonus"),
                ("word_mastered", 150, "Mastered 5 words"),
            ]
            for reason, amount, desc in xp_reasons:
                XPTransaction.objects.create(
                    user=user,
                    amount=amount,
                    reason=reason,
                    description=desc,
                )

        # ─── 10. Badges for user ───
        earned_badge_codes = ["first_word", "word_10", "streak_3", "review_10", "level_5"]
        for code in earned_badge_codes:
            try:
                badge = Badge.objects.get(code=code)
                UserBadge.objects.get_or_create(user=user, badge=badge)
            except Badge.DoesNotExist:
                pass

        # ─── 11. Notifications ───
        if not Notification.objects.filter(user=user).exists():
            notifications_data = [
                ("badge_earned", "Badge Earned!", "You earned the 'First Word' badge!", {"badge_code": "first_word"}),
                ("level_up", "Level Up!", "You reached level 5!", {"new_level": 5}),
                ("review_reminder", "Time to Review", "You have 10 words due for review.", {}),
                ("daily_goal_complete", "Daily Goal Complete!", "You completed your daily goal of 10 words.", {}),
                ("streak_warning", "Streak Warning!", "Don't lose your 3-day streak! Study today.", {}),
            ]
            for n_type, title, message, data in notifications_data:
                Notification.objects.create(
                    user=user,
                    type=n_type,
                    title=title,
                    message=message,
                    data=data,
                    is_read=False,
                )

        # ─── 12. Daily challenges ───
        DailyChallenge.objects.update_or_create(
            user=user,
            date=today,
            defaults={
                "challenges": [
                    {"id": 1, "type": "review", "title": "Review 5 words", "target": 5, "current": 3, "completed": False, "xp_reward": 20},
                    {"id": 2, "type": "test", "title": "Take a test", "target": 1, "current": 0, "completed": False, "xp_reward": 30},
                    {"id": 3, "type": "game", "title": "Play a game", "target": 1, "current": 0, "completed": False, "xp_reward": 25},
                ],
                "all_completed": False,
                "bonus_claimed": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Created user progress, streak, daily activities"))
        self.stdout.write(self.style.SUCCESS("Seed data complete!"))
