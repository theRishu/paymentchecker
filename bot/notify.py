import logging

from aiogram.enums import ParseMode

from config import ADMIN_CHAT_ID, SUBMISSION_CHANNEL

logger = logging.getLogger(__name__)


async def notify_admin(bot, text: str):
    if not ADMIN_CHAT_ID:
        return
    try:
        await bot.send_message(ADMIN_CHAT_ID, text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Admin notify failed: {e}")


from aiogram.types import BufferedInputFile

async def notify_channel(bot, text: str, photo: bytes = None):
    # List of channels to notify
    target_channels = [ch for ch in [SUBMISSION_CHANNEL] if ch]
    
    for channel_id in target_channels:
        try:
            if photo:
                await bot.send_photo(
                    channel_id, 
                    BufferedInputFile(photo, filename="screenshot.jpg"),
                    caption=text,
                    parse_mode=ParseMode.HTML
                )
            else:
                await bot.send_message(channel_id, text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Notify failed for channel {channel_id}: {e}")
