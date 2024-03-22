import asyncio

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from config import dispatchers
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Starts telegram bot polling"

    def handle(self, *args, **options):
        session = AiohttpSession(proxy=settings.TELEGRAM_PROXY)
        bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)

        async def main() -> None:
            await dispatchers.dp.start_polling(bot)

        asyncio.run(main())
