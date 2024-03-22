from celery import shared_task
from graphql_jwt.refresh_token.utils import get_refresh_token_model

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


@shared_task
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task
def clear_expired_refresh_tokens():
    """Removes expired refresh tokens from db."""
    qs = get_refresh_token_model().objects
    query = Q(revoked__isnull=False)
    qs = qs.expired()
    query |= Q(expired=True)

    deleted, _ = qs.filter(query).delete()

    return deleted
