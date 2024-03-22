from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.refresh_token.signals import refresh_token_rotated

from django.dispatch import receiver


# https://django-graphql-jwt.domake.io/refresh_token.html#one-time-only-use-refresh-token
@receiver(refresh_token_rotated)
def revoke_refresh_token(sender, request, refresh_token: RefreshToken, **kwargs):
    refresh_token.revoke(request)
