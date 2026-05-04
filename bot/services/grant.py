import aiohttp

from config import API_KEY, BOT_CALLBACKS


async def push_grant(row) -> bool:
    """POST grant request to the bot that owns this UTR. Returns True on HTTP 200."""
    callback_url = BOT_CALLBACKS.get(row.bot_name)
    if not callback_url:
        return False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                callback_url,
                json={
                    "user_id": row.user_id,
                    "bot_name": row.bot_name,
                    "amount": row.amount,
                    "utr": row.utr,
                    "days": row.days or 0,
                },
                headers={"X-API-Key": API_KEY},
                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                return resp.status == 200
    except Exception:
        return False
