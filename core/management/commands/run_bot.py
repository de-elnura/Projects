import asyncio
from django.core.management.base import BaseCommand
from core.telegram_bot import run_telegram_bot


class Command(BaseCommand):
    help = "EduQuiz / SkillUp LMS Telegram Botini ishga tushirish (aiogram 3.x)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🤖 Telegram Bot ishga tushirilmoqda..."))
        try:
            asyncio.run(run_telegram_bot())
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.WARNING("\n🛑 Telegram Bot to'xtatildi."))
