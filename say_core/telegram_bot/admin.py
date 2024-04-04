from django.contrib import admin

from say_core.telegram_bot.models import TelegramUserProfileModel, TGroupModel, TGroupRegisterModel


@admin.register(TelegramUserProfileModel)
class TelegramUserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(TGroupRegisterModel)
class TGroupRegisterAdmin(admin.ModelAdmin):
    pass


@admin.register(TGroupModel)
class TGroupAdmin(admin.ModelAdmin):
    pass
