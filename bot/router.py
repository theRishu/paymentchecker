from aiogram import Router

from bot.handlers.sms import router as sms_router
from bot.handlers.commands import router as commands_router

router = Router()
router.include_router(sms_router)
router.include_router(commands_router)
