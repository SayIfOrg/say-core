from enum import Enum

from aiogram import Bot, Router
from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from say_core.blogging.models import WPRegisterModel
from say_core.core.dispatchers import MainMenuType

router = Router(name="blogging")
UserModel = get_user_model()

class SimpleCallbackDataType(str, Enum):
    I_HAVE_THE_WP_PLUGIN_NOW_NEXT = "i_have_the_wp_plugin_now_next"


@router.callback_query(lambda query: query.data == MainMenuType.WP_COMMENTING)
async def wp_commenting_menu_handler(query: CallbackQuery, *args, **kwargs):
    ikbuilder = InlineKeyboardBuilder()
    ikbuilder.button(text=_("get from راست چین"), url="https://www.rtl-theme.com/")
    ikbuilder.button(text=_("already got it"), callback_data=SimpleCallbackDataType.I_HAVE_THE_WP_PLUGIN_NOW_NEXT)
    ikbuilder.adjust(1, 1)
    await query.message.edit_text(
        _("get the sayif WordPress plugin and then press proceed."), reply_markup=ikbuilder.as_markup()
    )


@router.callback_query(lambda query: query.data == SimpleCallbackDataType.I_HAVE_THE_WP_PLUGIN_NOW_NEXT)
async def register_wp_plugin_handler(query: CallbackQuery, user: UserModel):
    wp_register_obj = await WPRegisterModel.objects.new(actor=user)
    await query.message.edit_text(
        _("enter this code to your plugin and you are done:") + f"\n\n{wp_register_obj.code}"
    )


class NewCommentFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.chat.type == ChatType.SUPERGROUP
            and message.reply_to_message
            and is_commentable_tmessage_id(message.reply_to_message.message_id)
        )


@router.message(NewCommentFilter())
async def new_comment_handler(message: Message, bot: Bot) -> None:
    user_profile_photoes = await bot.get_user_profile_photos(user_id=message.from_user.id)
    reply_to_message_id = message.reply_to_message.message_id if message.reply_to_message else None
    await message.answer("menu", reply_markup=builder.as_markup())
