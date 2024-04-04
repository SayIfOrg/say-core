from datetime import timedelta

from environ import environ

import aiogram.utils.token

from ._setup import env

# Project's apps stuff...
# ------------------------------------------------------------------------------
# graphql
# ------------------------------------------------------------------------------
# show graphiql panel or not
GRAPHIQL = env.bool("GRAPHIQL", False)

# blogging
# ------------------------------------------------------------------------------
WP_PLUGIN = {"ping_url": "/sayif/ping"}
WP_GENERATED_CODE_VALID_TIME = timedelta(minutes=10)

# telegram_bot
# ------------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
aiogram.utils.token.validate_token(TELEGRAM_BOT_TOKEN)
TELEGRAM_WEBHOOK_URL = env.str("TELEGRAM_WEBHOOK_URL", "telegram-webhook/")
TELEGRAM_WEBHOOK_SECRET = env.str("TELEGRAM_WEBHOOK_SECRET")
TELEGRAM_PROXY = env.url("TELEGRAM_PROXY", default=None)
if TELEGRAM_PROXY:
    TELEGRAM_PROXY = environ.urlunparse(TELEGRAM_PROXY)
TELEGRAM_MIDDLEWARE = [
    "say_core.telegram_bot.t_middleware.AuthenticationMiddleware",
]
