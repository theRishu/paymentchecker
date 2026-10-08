import logging
from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

from config import ADMIN_CHAT_ID
from db.queries import record_sms, get_utr, mark_redeemed
from bot.services.grant import push_grant
from views import get_state

logger = logging.getLogger(__name__)
router = Router()


async def _finalize_manual_payment(bot, utr: str, amount: float, sender: str) -> str:
    """Records a payment the bank's SMS never sent (or was too slow to wait
    on) and tries to grant VIP immediately. Falls back to the user's own bot
    process picking it up via its 30s poller if the instant push fails —
    same safety net the automatic SMS path already relies on."""
    status, row = await record_sms(utr, amount, sender, datetime.now(), f"[manual] {sender}")
    if status == "auto_verified":
        if await push_grant(row):
            await mark_redeemed(utr)
            return f"✅ Granted VIP to <code>{row.user_id}</code> for ₹{amount:,.2f}"
        return f"✅ Recorded — will auto-grant to <code>{row.user_id}</code> within ~30s"
    if status == "duplicate":
        return "⚠️ Already recorded — no action taken."
    if status == "amount_mismatch":
        return (f"⚠️ Amount mismatch — recorded ₹{amount:,.2f} but user expected "
                f"₹{row.expected_amount:,.2f}. Not auto-granting.")
    if status == "sms_only_updated":
        return "ℹ️ Recorded — no user has submitted this UTR yet."
    return "✅ Recorded as new entry."


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
        result = await _finalize_manual_payment(msg.bot, parts[1], float(parts[2]), "Manual")
        await msg.reply(result, parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.reply(f"❌ Error: {e}")


@router.callback_query(F.data.startswith("approve_utr:"))
async def cb_approve_utr(call: types.CallbackQuery):
    if ADMIN_CHAT_ID and call.from_user.id != ADMIN_CHAT_ID:
        return await call.answer("Not authorized.", show_alert=True)

    _, utr, amount_str = call.data.split(":", 2)
    try:
        amount = float(amount_str)
    except ValueError:
        return await call.answer("Bad amount in button data.", show_alert=True)

    row = await get_utr(utr)
    if row and row.redeemed:
        result = "⚠️ Already redeemed — no action taken."
    else:
        result = await _finalize_manual_payment(call.bot, utr, amount, "Manual (admin approved)")
    await call.answer("Done")

    try:
        if call.message.photo:
            await call.message.edit_caption(
                caption=f"{call.message.caption}\n\n{result}",
                parse_mode=ParseMode.HTML,
            )
        else:
            await call.message.edit_text(
                f"{call.message.text}\n\n{result}",
                parse_mode=ParseMode.HTML,
            )
    except Exception:
        pass
