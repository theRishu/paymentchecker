import logging
import sys

import uvicorn
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET
from db.queries import init_db
from bot.router import router as bot_router
from api import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)


async def main():
    await init_db()
    logger.info("Database initialized.")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(bot_router)

    me = await bot.get_me()
    logger.info(f"Bot started: @{me.username}")

    # Long-polling silently misses an update occasionally (confirmed: no
    # crash, no error log, just a gap where the bot's next getUpdates call
    # never surfaces a message that genuinely reached Telegram). A webhook
    # doesn't have this failure mode the same way — Telegram pushes the
    # update and retries delivery if our endpoint doesn't ack it, instead of
    # relying on us to poll at the right moment.
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=False,
    )
    logger.info(f"Webhook set to {WEBHOOK_URL}")

    app = create_app(bot, dp)

    config = uvicorn.Config(app, host="0.0.0.0", port=8087, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
