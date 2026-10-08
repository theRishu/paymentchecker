import asyncio
import logging
from datetime import datetime

from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import Update

from config import API_KEY, WEBHOOK_PATH, WEBHOOK_SECRET
from db.queries import submit_utr, get_utr
from bot.notify import notify_admin, notify_channel
from bot.handlers.sms import process_incoming_sms
from api.schemas import SmsIngestBody

logger = logging.getLogger(__name__)
router = APIRouter()

_key_hdr = APIKeyHeader(name="X-API-Key", auto_error=False)


@router.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Bad secret token")

    dp = request.app.state.dp
    bot = request.app.state.bot
    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


async def verify_api_key(key: str = Depends(_key_hdr)):
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/status/{utr}", dependencies=[Depends(verify_api_key)])
async def api_status(utr: str):
    """Lets the channel-history reconciliation job check whether a UTR was
    already recorded before re-submitting it, so a gap-fill pass doesn't spam
    duplicate-SMS alerts for messages the live channel_post handler already
    caught."""
    row = await get_utr(utr)
    return {"recorded": bool(row and row.amount is not None)}


@router.post("/ingest/sms", dependencies=[Depends(verify_api_key)])
async def ingest_sms(request: Request, body: SmsIngestBody):
    """Direct HTTP ingestion path, in case BotPay ever needs it instead of
    posting to the Telegram channel (Telegram doesn't deliver a channel_post
    update back to the same bot that posted it)."""
    bot = request.app.state.bot
    await process_incoming_sms(bot, body.text, datetime.now())
    return {"status": "received"}


@router.post("/verify/{utr}", dependencies=[Depends(verify_api_key)])
async def api_verify(
    request: Request, 
    utr: str,
    user_id: int = Form(...),
    username: Optional[str] = Form(None),
    bot_name: str = Form("unknown"),
    days: int = Form(0),
    expected_amount: float = Form(0.0),
    screenshot: Optional[UploadFile] = File(None)
):
    status, data = await submit_utr(
        utr, user_id, bot_name, days,
        expected_amount, username=username,
    )

    bot = request.app.state.bot
    
    # Read screenshot bytes if provided
    photo_bytes = None
    if screenshot:
        photo_bytes = await screenshot.read()

    if status == "ok":
        asyncio.create_task(notify_channel(
            bot,
            f"✅ <b>UTR Verified</b>\n"
            f"UTR: <code>{utr}</code>\n"
            f"User: <code>{user_id}</code> (@{username or 'NoUser'})\n"
            f"Bot: {bot_name} | Amount: ₹{data.get('amount', 0):,.2f} | Days: {days}",
            photo=photo_bytes
        ))
        return {"status": "verified", **data}
    if status == "pending":
        # Bank SMS sometimes never arrives (carrier/bank-side failure, not a
        # bug in our pipeline) — this button lets the admin grant on the spot,
        # trusting the amount the user already claimed, instead of having to
        # dig up the UTR/amount and type /addpayment by hand.
        approve_kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=f"✅ Approve & Grant ₹{expected_amount:,.2f}",
                callback_data=f"approve_utr:{utr}:{expected_amount}",
            )
        ]])
        asyncio.create_task(notify_channel(
            bot,
            f"⏳ <b>UTR Submitted</b>\n"
            f"UTR: <code>{utr}</code>\n"
            f"User: <code>{user_id}</code> (@{username or 'NoUser'})\n"
            f"Bot: {bot_name} | Expected: ₹{expected_amount:,.2f} | Days: {days}",
            photo=photo_bytes,
            reply_markup=approve_kb,
        ))
        return JSONResponse({"status": "pending", "utr": utr}, status_code=202)
    if status == "already_pending":
        return JSONResponse({"status": "already_pending"}, status_code=208)
    if status == "amount_mismatch":
        return JSONResponse({"status": "amount_mismatch", **data}, status_code=422)
    if status == "too_many_pending":
        return JSONResponse({"status": "too_many_pending"}, status_code=429)
    if status in ("already_submitted", "claimed_by_other"):
        msg = (
            f"🚨 <b>UTR CONFLICT DETECTED</b>\n"
            f"UTR: <code>{utr}</code>\n"
            f"Attempt by: <code>{user_id}</code> "
            f"(@{username or 'NoUser'}) [{bot_name}]\n"
            f"Current Owner: <code>{data.get('user_id')}</code> "
            f"(@{data.get('username') or 'NoUser'}) [{data.get('bot_name')}]\n"
            f"Status: {status}"
        )
        asyncio.create_task(notify_admin(bot, msg))
        return JSONResponse({"status": status, "detail": status, "owner": data}, status_code=409)

    return JSONResponse({"status": status}, status_code=400)
