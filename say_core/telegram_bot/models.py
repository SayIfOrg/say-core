from typing import TYPE_CHECKING

from asgiref.sync import async_to_sync

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as __

from say_core.utils.models import TimeStampedModel

if TYPE_CHECKING:
    from aiogram.types import User as TUser

UserModel = get_user_model()


class TelegramUserProfileManager(models.Manager):
    @transaction.atomic
    def auto_new_from_user_tevent(self, tuser: "TUser"):
        username = async_to_sync(UserModel.objects.make_username)(base=tuser.username)
        user = UserModel.objects.create_user(username=username)
        obj = self.model()
        obj.user = user
        obj.user_oid = tuser.id
        obj.username = tuser.username
        obj.is_default = True
        obj.save()
        return obj


class TelegramUserProfileModel(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegramuserprofile_set"
    )
    user_oid = models.BigIntegerField(unique=True, db_index=True)
    is_default = models.BooleanField(default=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    objects = TelegramUserProfileManager()

    class Meta:
        verbose_name = __("Telegram User Profile")
        db_table = "telegrambot_telegramuserprofile"
        constraints = [
            models.UniqueConstraint(
                fields=("user",), condition=Q(is_default=True), name="only_one_default_telegram_profile_per_user"
            )
        ]


class TChannelRegisterModel(TimeStampedModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tchannelregister_set")
    tchannel = models.OneToOneField("TChannelModel", on_delete=models.CASCADE, related_name="tchannelregister_set")


class TChannelModel(TimeStampedModel, models.Model):
    channel_oid = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = __("Telegram Channel")
        db_table = "telegrambot_telegramchannel"


class TGroupRegisterManager(models.Manager):
    async def new_registered(self, *, user: UserModel, tgroup: "TGroupModel"):
        assert not await self.filter(
            tgroup=tgroup, is_active=True
        ).aexists(), "only_one_active_tgrouprequest_per_tgroup"
        tgroup_register_obj = self.model()
        tgroup_register_obj.user = user
        tgroup_register_obj.tgroup = tgroup
        tgroup_register_obj.is_active = True
        await tgroup_register_obj.asave()
        return tgroup_register_obj


class TGroupRegisterModel(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tgroupregister_set", null=True, blank=True
    )
    tgroup = models.ForeignKey("TGroupModel", on_delete=models.CASCADE, related_name="tgroupregister_set")
    is_active = models.BooleanField(default=True)

    objects = TGroupRegisterManager()

    class Meta:
        verbose_name = __("Telegram Group Register")
        db_table = "telegrambot_tgroupregister"
        constraints = [
            models.UniqueConstraint(
                fields=("tgroup",), condition=Q(is_active=True), name="only_one_active_tgrouprequest_per_tgroup"
            )
        ]

    async def no_longer_a_member(self):
        self.is_active = False
        await self.asave()


class TGroupManager(models.Manager):
    async def on_add_event(self, tgroup_oid: int, group_type: "TGroupModel.Type", group_title: str):
        tgroup_obj, is_created = await self.aget_or_create(
            group_oid=tgroup_oid, defaults={"type": group_type, "title": group_title}
        )
        return tgroup_obj, is_created


class TGroupModel(TimeStampedModel, models.Model):
    class Type(models.TextChoices):
        GROUP = "group", __("telegram simple group")
        SUPERGROUP = "supergroup", __("telegram super group")

    group_oid = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=31, choices=Type.choices)
    title = models.CharField(max_length=255)

    objects = TGroupManager()

    class Meta:
        verbose_name = __("Telegram Group")
        db_table = "telegrambot_tgroup"

    async def current_register(self) -> "TGroupRegisterModel":
        return await self.tgroupregister_set.aget(is_active=True)
