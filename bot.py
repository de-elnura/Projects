import os
import sys
import asyncio

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from core.telegram_bot import run_telegram_bot


if __name__ == '__main__':
    try:
        asyncio.run(run_telegram_bot())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Telegram Bot to'xtatildi.")
