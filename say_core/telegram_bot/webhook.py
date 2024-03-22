import json

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import Update
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework import status

from say_core.utils.decorators import require_http_methods


def get_webhook_view(dp: Dispatcher):
    session = AiohttpSession(proxy=settings.TELEGRAM_PROXY)
    bot = Bot(settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)

    @require_http_methods(["POST"])
    async def webhook_view(request):
        if request.headers.get("x-telegram-bot-api-secret-token") != settings.TELEGRAM_WEBHOOK_SECRET:
            return HttpResponseForbidden()
        update = Update.model_validate(json.loads(request.body), context={"bot": bot})
        await dp.feed_webhook_update(bot=bot, update=update)
        return HttpResponse(status=status.HTTP_200_OK)

    return webhook_view
