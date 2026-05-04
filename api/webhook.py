import asyncio
import logging

from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader

from config import API_KEY
from db.queries import submit_utr
from bot.notify import notify_admin, notify_channel

logger = logging.getLogger(__name__)
router = APIRouter()

_key_hdr = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str = Depends(_key_hdr)):
    if not key or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.get("/health")
async def health():
    return {"status": "ok"}


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
        asyncio.create_task(notify_channel(
            bot,
            f"⏳ <b>UTR Submitted</b>\n"
            f"UTR: <code>{utr}</code>\n"
            f"User: <code>{user_id}</code> (@{username or 'NoUser'})\n"
            f"Bot: {bot_name} | Expected: ₹{expected_amount:,.2f} | Days: {days}",
            photo=photo_bytes
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
