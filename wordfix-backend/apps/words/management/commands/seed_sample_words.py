"""
Management command: seed_sample_words

Seeds 20 sample English words for a given user or the default admin.
Idempotent — skips words that already exist for the user.
"""

from django.core.management.base import BaseCommand

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import Word


SAMPLE_WORDS = [
    {"original_word": "achieve", "translation": "erishmoq", "part_of_speech": "verb", "definition": "To successfully bring about or reach a desired objective.", "example_sentence": "She worked hard to achieve her goals.", "example_translation": "U maqsadlariga erishish uchun qattiq ishladi.", "difficulty_level": "medium"},
    {"original_word": "abundant", "translation": "mo'l-ko'l", "part_of_speech": "adjective", "definition": "Existing or available in large quantities.", "example_sentence": "The region has abundant natural resources.", "example_translation": "Mintaqada tabiiy resurslar mo'l-ko'l.", "difficulty_level": "hard"},
    {"original_word": "analyze", "translation": "tahlil qilmoq", "part_of_speech": "verb", "definition": "Examine something methodically and in detail.", "example_sentence": "Scientists analyze the data carefully.", "example_translation": "Olimlar ma'lumotlarni sinchiklab tahlil qilishadi.", "difficulty_level": "medium"},
    {"original_word": "benefit", "translation": "foyda", "part_of_speech": "noun", "definition": "An advantage or profit gained from something.", "example_sentence": "Exercise has many health benefits.", "example_translation": "Jismoniy mashqlarning ko'p sog'liq foydalari bor.", "difficulty_level": "easy"},
    {"original_word": "collaborate", "translation": "hamkorlik qilmoq", "part_of_speech": "verb", "definition": "Work jointly on an activity or project.", "example_sentence": "The two companies decided to collaborate.", "example_translation": "Ikki kompaniya hamkorlik qilishga qaror qildi.", "difficulty_level": "medium"},
    {"original_word": "demonstrate", "translation": "ko'rsatmoq", "part_of_speech": "verb", "definition": "Clearly show the existence or truth of something.", "example_sentence": "The experiment demonstrated the theory.", "example_translation": "Tajriba nazariyani ko'rsatdi.", "difficulty_level": "medium"},
    {"original_word": "efficient", "translation": "samarali", "part_of_speech": "adjective", "definition": "Achieving maximum productivity with minimum wasted effort.", "example_sentence": "The new system is more efficient.", "example_translation": "Yangi tizim yanada samarali.", "difficulty_level": "medium"},
    {"original_word": "fluctuate", "translation": "o'zgarmoq", "part_of_speech": "verb", "definition": "Rise and fall irregularly in number or amount.", "example_sentence": "Prices fluctuate throughout the year.", "example_translation": "Narxlar yil davomida o'zgarib turadi.", "difficulty_level": "hard"},
    {"original_word": "generate", "translation": "yaratmoq", "part_of_speech": "verb", "definition": "Cause something to arise or come about.", "example_sentence": "Wind turbines generate electricity.", "example_translation": "Shamol turbinalari elektr energiya yaratadi.", "difficulty_level": "easy"},
    {"original_word": "hypothesis", "translation": "gipoteza", "part_of_speech": "noun", "definition": "A supposition made as a starting point for further investigation.", "example_sentence": "The scientist tested her hypothesis.", "example_translation": "Olim o'z gipotezasini sinab ko'rdi.", "difficulty_level": "hard"},
    {"original_word": "implement", "translation": "amalga oshirmoq", "part_of_speech": "verb", "definition": "Put a decision, plan, or agreement into effect.", "example_sentence": "We need to implement the new policy.", "example_translation": "Yangi siyosatni amalga oshirishimiz kerak.", "difficulty_level": "medium"},
    {"original_word": "justify", "translation": "oqlash", "part_of_speech": "verb", "definition": "Show or prove to be right or reasonable.", "example_sentence": "How can you justify such expenses?", "example_translation": "Bunday xarajatlarni qanday oqlaysiz?", "difficulty_level": "medium"},
    {"original_word": "knowledge", "translation": "bilim", "part_of_speech": "noun", "definition": "Facts, information, and skills acquired through experience or education.", "example_sentence": "Knowledge is power.", "example_translation": "Bilim — kuch.", "difficulty_level": "easy"},
    {"original_word": "legislation", "translation": "qonunchilik", "part_of_speech": "noun", "definition": "Laws, considered collectively.", "example_sentence": "New legislation was passed last week.", "example_translation": "O'tgan hafta yangi qonun qabul qilindi.", "difficulty_level": "hard"},
    {"original_word": "maintain", "translation": "saqlamoq", "part_of_speech": "verb", "definition": "Cause or enable a condition or state of affairs to continue.", "example_sentence": "It is important to maintain good health.", "example_translation": "Yaxshi sog'liqni saqlab qolish muhim.", "difficulty_level": "easy"},
    {"original_word": "negotiate", "translation": "muzokaralar olib bormoq", "part_of_speech": "verb", "definition": "Try to reach an agreement or compromise by discussion.", "example_sentence": "They are negotiating a new contract.", "example_translation": "Ular yangi shartnoma bo'yicha muzokaralar olib borishmoqda.", "difficulty_level": "hard"},
    {"original_word": "obvious", "translation": "aniq", "part_of_speech": "adjective", "definition": "Easily perceived or understood; clear.", "example_sentence": "The answer was obvious to everyone.", "example_translation": "Javob hammaga aniq edi.", "difficulty_level": "easy"},
    {"original_word": "perspective", "translation": "nuqtai nazar", "part_of_speech": "noun", "definition": "A particular attitude toward or way of regarding something.", "example_sentence": "Try to see it from my perspective.", "example_translation": "Uni mening nuqtai nazarimdan ko'rishga harakat qiling.", "difficulty_level": "medium"},
    {"original_word": "relevant", "translation": "tegishli", "part_of_speech": "adjective", "definition": "Closely connected or appropriate to what is being done.", "example_sentence": "Please provide relevant information.", "example_translation": "Iltimos, tegishli ma'lumotlarni bering.", "difficulty_level": "medium"},
    {"original_word": "sufficient", "translation": "yetarli", "part_of_speech": "adjective", "definition": "Enough; adequate.", "example_sentence": "We have sufficient funds for the project.", "example_translation": "Loyiha uchun yetarli mablag'imiz bor.", "difficulty_level": "medium"},
]


class Command(BaseCommand):
    help = "Seed 20 sample English words for a user (default: admin@wordfix.com)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="admin@wordfix.com",
            help="Email of the user to seed words for.",
        )
        parser.add_argument(
            "--user_email",
            type=str,
            default=None,
            help="Alias for --email.",
        )

    def handle(self, *args, **options):
        email = options["user_email"] or options["email"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{email}' not found. Create the user first."))
            return

        created_count = 0
        skipped_count = 0

        for word_data in SAMPLE_WORDS:
            original_word = word_data["original_word"]
            if Word.objects.filter(user=user, original_word=original_word).exists():
                skipped_count += 1
                continue

            Word.objects.create(user=user, **word_data)
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} created, {skipped_count} skipped."
            )
        )
