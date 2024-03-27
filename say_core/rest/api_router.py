from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView
from say_core.blogging.rest import views as blogging_views
from django.urls import path

app_name = "rest"
urlpatterns = [
    # REST API JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # REST API schema
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    # REST API docs
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("wp-site-apikey/", blogging_views.WPSiteAPIKeyViewSet.as_view({"post": "create"})),
]
