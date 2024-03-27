import random
import string

from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as __


class UserManager(BaseUserManager):
    async def make_username(self, base=None, length=15) -> str:
        base = base or ""
        length -= len(base)
        characters = string.ascii_letters + string.digits
        while True:
            username = base + "".join(random.choice(characters) for _ in range(length))
            if not await self.filter(username=username).aexists():
                return username

class UserModel(AbstractUser):
    """
    Default custom user model for say_core.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(__("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    objects = UserManager()

    class Meta:
        db_table = "users_user"
        verbose_name = __("User")
