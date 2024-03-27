from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.utils.translation import gettext as _

router = Router(name="core")


class MainMenuType(str, Enum):
    WP_COMMENTING = "wp_commenting"


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ikbuilder = InlineKeyboardBuilder()
    ikbuilder.button(text=_("WordPress commenting"), callback_data=MainMenuType.WP_COMMENTING)
    await message.answer(_("menu"), reply_markup=ikbuilder.as_markup())
