from aiogram import Dispatcher

from say_core.core.dispatchers import router as core_router

dp = Dispatcher()
dp.include_router(core_router)
