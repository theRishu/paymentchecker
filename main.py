import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db.queries import init_db
from bot.router import router as bot_router
from api import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def start_bot(bot: Bot, dp: Dispatcher):
    try:
        me = await bot.get_me()
        logger.info(f"Bot started: @{me.username}")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot failed: {e}")


async def start_server(app):
    config = uvicorn.Config(app, host="0.0.0.0", port=8087, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await init_db()
    logger.info("Database initialized.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(bot_router)

    app = create_app(bot)

    await asyncio.gather(start_server(app), start_bot(bot, dp))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
