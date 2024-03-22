import asyncio

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("base_domain", type=str)

    def handle(self, *args, **options):
        session = AiohttpSession(proxy=settings.TELEGRAM_PROXY)
        bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)

        async def main() -> None:
            url = f"{options['base_domain']}/{settings.TELEGRAM_WEBHOOK_URL}"
            await bot.set_webhook(url, secret_token=settings.TELEGRAM_WEBHOOK_SECRET)

        asyncio.run(main())
