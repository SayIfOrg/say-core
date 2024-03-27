from django.contrib import admin

from say_core.blogging.models import WPPostModel, WPSiteModel


@admin.register(WPSiteModel)
class WPSiteAdmin(admin.ModelAdmin):
    pass


@admin.register(WPPostModel)
class WPPostAdmin(admin.ModelAdmin):
    pass
