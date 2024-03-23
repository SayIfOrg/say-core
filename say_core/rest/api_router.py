from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

app_name = "rest"
urlpatterns = [
    # REST API JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token /refresh/", TokenRefreshView.as_view(), name="token_refresh"),
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
]
