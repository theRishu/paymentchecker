import logging
import re
from datetime import datetime

from aiogram import Router, types, F

from config import SMS_INPUT_CHANNEL
from db.queries import record_sms, mark_redeemed
from utils import parse_sms
from bot.notify import notify_admin
from bot.services.grant import push_grant

logger = logging.getLogger(__name__)
router = Router()


@router.channel_post(F.chat.id == SMS_INPUT_CHANNEL)
async def on_sms_received(msg: types.Message):
    text = msg.text or msg.caption or ""
    received_at = msg.date.replace(tzinfo=None) if msg.date else datetime.now()

    parsed = parse_sms(text)
    if not parsed:
        return

    status, row = await record_sms(
        utr=parsed['utr'],
        amount=parsed['amount'],
        sender=parsed['sender'],
        sms_date=parsed['date'],
        raw_sms=text,
        received_at=received_at,
    )

    if status == "duplicate":
        user_info = f" by user <code>{row.user_id}</code>" if row.user_id else ""
        await notify_admin(
            msg.bot,
            f"🚨 <b>DUPLICATE SMS</b>\n"
            f"UTR <code>{row.utr}</code> already recorded{user_info}.\n"
            f"Amount: ₹{row.amount:,.2f}",
        )
        return

    note = ""
    if status == "auto_verified":
        if await push_grant(row):
            await mark_redeemed(row.utr)
            note = f"\n⚡ <b>Auto-verified & VIP Granted</b> to <code>{row.user_id}</code>"
        else:
            note = "\n⚡ <b>Auto-verified</b> — grant pending"

    if status in ("new", "auto_verified", "sms_only_updated"):
        await notify_admin(
            msg.bot,
            f"✅ <b>SMS Received</b>\n"
            f"UTR: <code>{parsed['utr']}</code> | ₹{parsed['amount']:,.2f}\n"
            f"From: {parsed['sender']}{note}",
        )
