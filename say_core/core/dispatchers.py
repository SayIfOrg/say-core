from enum import Enum
from typing import Union

from aiogram import Bot, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_startgroup_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from say_core.blogging.models import WPSiteModel
from say_core.telegram_bot.models import TGroupRegisterModel

router = Router(name="core")

UserModel = get_user_model()


class MainMenuType(str, Enum):
    WP_REGISTER = "wp_register"
    WP_LIST = "wp_list"
    TGROUP_REGISTER = "tgroup_register"
    TGROUP_LIST = "tgroup_list"


class WPSiteCallbackData(CallbackData, prefix="wp_site"):
    id: int


@router.message(CommandStart(), lambda message: message.chat.type == ChatType.PRIVATE)
@router.callback_query(lambda query: query.data == "main_menu")
async def command_start_handler(update: Union[Message, CallbackQuery], user: UserModel, bot: Bot) -> None:
    ikbuilder = InlineKeyboardBuilder()
    ikbuilder.button(text=_("Register a new WordPress Site"), callback_data=MainMenuType.WP_REGISTER)
    if await WPSiteModel.objects.filter(wpregister_set__user=user).aexists():
        ikbuilder.button(text=_("Your WordPress sites"), callback_data=MainMenuType.WP_LIST)
    startgroup_link = await create_startgroup_link(bot=bot, payload=f"user_id_{user.id}")
    ikbuilder.button(text=_("Register a new Telegram group"), url=startgroup_link)
    if await TGroupRegisterModel.objects.filter(user=user).aexists():
        ikbuilder.button(text=_("Your Telegram groups"), callback_data=MainMenuType.TGROUP_LIST)
    ikbuilder.adjust(1)
    if type(update) == Message:
        await update.answer(_("menu"), reply_markup=ikbuilder.as_markup())
    else:
        await update.message.edit_text(_("menu"), reply_markup=ikbuilder.as_markup())
