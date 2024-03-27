from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _


class TelegramBotConfig(AppConfig):
    name = "say_core.telegram_bot"
    verbose_name = _("Telegram Bot")

    def ready(self):
        from config import dispatchers

        for middleware_path in settings.TELEGRAM_MIDDLEWARE:
            Middleware = import_string(middleware_path)
            dispatchers.dp.update.middleware(Middleware())
