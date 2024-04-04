import logging

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter, CommandStart
from aiogram.types import CallbackQuery, ChatMemberUpdated
from aiogram.utils.keyboard import InlineKeyboardBuilder
from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.utils.translation import gettext as _

from say_core.core.dispatchers import MainMenuType
from say_core.telegram_bot.models import TelegramUserProfileModel, TGroupModel, TGroupRegisterModel

router = Router(name="telegram_bot")
UserModel = get_user_model()
logger = logging.getLogger(__name__)


@router.callback_query(lambda query: query.data == MainMenuType.TGROUP_LIST)
async def list_tgroup_handler(query: CallbackQuery, user: UserModel):
    tgroup_register_qs = TGroupRegisterModel.objects.filter(user=user, is_active=True).select_related("tgroup")
    ikbuilder = InlineKeyboardBuilder()
    async for tgroup_register_obj in tgroup_register_qs:
        ikbuilder.button(text=tgroup_register_obj.tgroup.title, callback_data="dummy")
    ikbuilder.button(text=_("back"), callback_data="main_menu")
    ikbuilder.adjust(1, 1)
    text = _("this is the list of your Telegram groups.")
    await query.message.edit_text(text=text, reply_markup=ikbuilder.as_markup())


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def removed_from_group_handler(update: ChatMemberUpdated, bot: Bot):
    tgroup_obj = await TGroupModel.objects.aget(group_oid=update.chat.id)
    tgroup_register_obj = await tgroup_obj.current_register()
    await tgroup_register_obj.no_longer_a_member()
    registerar_tuser = await TelegramUserProfileModel.objects.aget(
        user_id=tgroup_register_obj.user_id, is_default=True
    )
    text = _("bot removed from group({group_title})").format(group_title=tgroup_obj.title)
    await bot.send_message(chat_id=registerar_tuser.user_oid, text=text)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def added_to_group_handler(update: ChatMemberUpdated):
    tgroup_obj, is_created = await TGroupModel.objects.on_add_event(
        tgroup_oid=update.chat.id, group_type=update.chat.type, group_title=update.chat.title
    )
    if not is_created:
        try:
            active_tgroup_register_obj = await tgroup_obj.tgroupregister_set.aget(is_active=True)
            await active_tgroup_register_obj.no_longer_a_member()
            logger.info(f"bot added to a tgroup with active TGroupRegisterModel: {str(active_tgroup_register_obj)}")
        except TGroupRegisterModel.DoesNotExist:
            pass
    await caches["logical"].aset(f"just_joined_tgroup_oid_{update.chat.id}", True, timeout=10)


@router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(r"user_id_\d")),
    lambda message: message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP),
)
async def after_added_to_group_handler(update: ChatMemberUpdated, user: UserModel, bot: Bot):
    if await caches["logical"].aget(f"just_joined_tgroup_oid_{update.chat.id}") is None:
        await update.answer(_("usage of this command is expired."))
        return
    command_args = CommandStart(deep_link=True, ignore_mention=True).extract_command(update.text).args
    actor_user_id = command_args.split("_")[2]
    actor_user = await UserModel.objects.aget(id=actor_user_id)
    tgroup_obj = await TGroupModel.objects.aget(group_oid=update.chat.id)
    tgroup_register_obj = await TGroupRegisterModel.objects.new_registered(user=actor_user, tgroup=tgroup_obj)
    text = _("bot successfully added to your group({group_title})").format(
        group_title=tgroup_register_obj.tgroup.title
    )
    actor_tuser = await actor_user.atelegram_profile
    await bot.send_message(chat_id=actor_tuser.user_oid, text=text)
