from aiogram import Dispatcher

from say_core.blogging.dispatchers import router as commenting_router
from say_core.core.dispatchers import router as core_router
from say_core.telegram_bot.dispatchers import router as telegram_router

dp = Dispatcher()
dp.include_router(core_router)
dp.include_router(telegram_router)
dp.include_router(commenting_router)
