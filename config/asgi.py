"""
ASGI config for say_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from channels.routing import ProtocolTypeRouter

from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# my_awesome_project directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "say_core"))
# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
    }
)
