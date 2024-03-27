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
