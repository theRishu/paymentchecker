import logging
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import ADMIN_CHAT_ID
from db.queries import record_sms, get_utr
from views import get_state

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("id", "start"))
async def cmd_id(msg: types.Message):
    await msg.reply(
        f"Your Chat ID is: <code>{msg.chat.id}</code>",
        parse_mode=ParseMode.HTML,
    )
    logger.info(f"ID command from: {msg.chat.id}")


@router.message(Command("check"))
async def cmd_check(msg: types.Message):
    parts = (msg.text or "").split(maxsplit=1)
    if len(parts) < 2:
        return await msg.reply("Usage: /check <UTR>")
    r = await get_utr(parts[1].strip())
    if not r:
        return await msg.reply("❌ No record found.")
    label, _ = get_state(r)
    await msg.reply(
        f"🔍 <b>UTR:</b> <code>{r.utr}</code>\n"
        f"<b>Status:</b> {label}\n"
        f"<b>Amount:</b> ₹{r.amount or 0:,.2f}",
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("addpayment"))
async def cmd_add(msg: types.Message):
    if ADMIN_CHAT_ID and msg.from_user.id != ADMIN_CHAT_ID:
        return
    parts = (msg.text or "").split(maxsplit=3)
    if len(parts) < 3:
        return await msg.reply("Usage: /addpayment <utr> <amount>")
    try:
        await record_sms(parts[1], float(parts[2]), "Manual", datetime.now(), "manual")
        await msg.reply(f"✅ Added <code>{parts[1]}</code>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.reply(f"❌ Error: {e}")
