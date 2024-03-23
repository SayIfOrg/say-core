from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from say_core.graphql.schema import schema
from say_core.graphql.views import GraphQLView
from say_core.telegram_bot.webhook import get_webhook_view
from say_core.utils.decorators import csrf_exempt

from .dispatchers import dp

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Telegram webhook handler
    path(settings.TELEGRAM_WEBHOOK_URL, csrf_exempt(get_webhook_view(dp))),
    # Graphql url
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.GRAPHIQL, schema=schema))),
    # REST API base url
    path("rest/", include("say_core.rest.api_router")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.PLUGGABLE_FUNCS.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls)),
    )
