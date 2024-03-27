from collections.abc import Awaitable, Callable
from typing import Any

from asgiref.sync import sync_to_async
from say_core.telegram_bot.models import TelegramUserProfileModel

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

UserModel = get_user_model()


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_chat: Chat = data["event_chat"]
        event_from_user: User = data["event_from_user"]
        try:
            telegram_user_profile_obj = await TelegramUserProfileModel.objects.select_related("user").aget(
                user_oid=event_from_user.id
            )
            if not telegram_user_profile_obj.is_default:
                raise NotImplementedError
        except TelegramUserProfileModel.DoesNotExist:
            if event_chat.type == "private":
                telegram_user_profile_obj = await sync_to_async(
                    TelegramUserProfileModel.objects.auto_new_from_user_tevent
                )(event_from_user)
            else:
                telegram_user_profile_obj = None

        data.update(user=telegram_user_profile_obj.user if telegram_user_profile_obj else AnonymousUser())
        return await handler(event, data)
