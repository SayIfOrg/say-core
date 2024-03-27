import string
import random

from django_fsm import FSMField

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as __

from say_core.utils.models import TimeStampedModel

UserModel = get_user_model()


class WPRegisterManager(models.Manager):
    async def new(self, actor: UserModel):
        obj: "WPRegisterModel" = self.model()
        obj.status = self.model.Status.WAIT_FOR_CODE_ENTRANCE
        obj.user = actor
        obj.code = self.model.generate_code()
        obj.code_generated_at = timezone.now()
        await obj.asave()
        return obj


class WPRegisterModel(TimeStampedModel, models.Model):
    class Status(models.TextChoices):
        WAIT_FOR_CODE_ENTRANCE = "wait_for_code_entrance", __("waiting for code to be used")
        REGISTERED = "registered", __("registered")

    status = FSMField(choices=Status.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="wpregister_set")
    site = models.OneToOneField(
        "WPSiteModel", on_delete=models.CASCADE, related_name="wpregister_set", null=True, blank=True
    )
    code = models.CharField(max_length=127)
    code_generated_at = models.DateTimeField()
    code_used_at = models.DateTimeField(null=True, blank=True)
    apikey = models.ForeignKey("rest_framework_api_key.APIKey", related_name="wpregister_set", on_delete=models.PROTECT, null=True, blank=True)

    objects = WPRegisterManager()

    class Meta:
        db_table = "blogging_wpregister"
        verbose_name = "WordPress Register"

    @staticmethod
    def generate_code():
        letters = string.digits
        length = 7
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str


class WPSiteModel(TimeStampedModel, models.Model):
    url = models.URLField()

    class Meta:
        db_table = "blogging_wpsite"
        verbose_name = "WordPress Site"


class WPPostModel(TimeStampedModel, models.Model):
    site = models.ForeignKey(WPSiteModel, on_delete=models.CASCADE, related_name="wpsite_set")
    post_oid = models.IntegerField()

    class Meta:
        db_table = "blogging_wppost"
        verbose_name = "WordPress Post"
