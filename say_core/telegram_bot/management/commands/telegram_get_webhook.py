import asyncio

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        session = AiohttpSession(proxy=settings.TELEGRAM_PROXY)
        bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)

        async def main() -> None:
            info = await bot.get_webhook_info()
            res = f"current url is {info.url}, "
            self.stdout.write(res)

        asyncio.run(main())
