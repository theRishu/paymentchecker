import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from api.auth import is_authenticated
from db.queries import get_recent_sms, get_recent_pending, get_recent_redeemed, delete_utr
from views import render_page, render_row, render_stats, render_table_card

logger = logging.getLogger(__name__)
router = APIRouter()


def _guard(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/login", status_code=302)
    return None


@router.post("/delete/{utr}")
async def api_delete_utr(utr: str, request: Request):
    redir = _guard(request)
    if redir: return redir
    
    success = await delete_utr(utr)
    if success:
        return {"status": "ok"}
    return {"status": "error", "message": "Not found"}, 404


@router.get("/", response_class=HTMLResponse)
async def page_overview(request: Request):
    redir = _guard(request)
    if redir:
        return redir
    try:
        sms  = await get_recent_sms(100)
        pend = await get_recent_pending(100)
        red  = await get_recent_redeemed(100)
    except Exception as e:
        logger.error(f"DB error on overview: {e}")
        return HTMLResponse(
            "<h3 style='font-family:sans-serif;padding:40px;color:#ef4444'>"
            "Database unavailable. Make sure PostgreSQL is running.</h3>",
            status_code=503,
        )

    combined = {r.utr: r for r in (sms + pend + red)}
    rows = sorted(combined.values(), key=lambda x: x.created_at, reverse=True)[:100]
    rows_html = "".join(render_row(r) for r in rows)
    body = render_stats(sms, pend, red) + render_table_card(
        "All Activity", len(rows), rows_html, "No records yet."
    )
    return render_page("Overview", "all", body)


@router.get("/pending", response_class=HTMLResponse)
async def page_pending(request: Request):
    redir = _guard(request)
    if redir:
        return redir
    try:
        rows = await get_recent_pending(100)
    except Exception as e:
        logger.error(f"DB error on pending: {e}")
        return HTMLResponse("<h3 style='font-family:sans-serif;padding:40px;color:#ef4444'>Database unavailable.</h3>", status_code=503)

    rows_html = "".join(render_row(r) for r in rows)
    table = render_table_card("Pending Submissions", len(rows), rows_html, "No pending submissions.")
    return render_page("Pending", "pending", table)


@router.get("/redeemed", response_class=HTMLResponse)
async def page_redeemed(request: Request):
    redir = _guard(request)
    if redir:
        return redir
    try:
        rows = await get_recent_redeemed(100)
    except Exception as e:
        logger.error(f"DB error on redeemed: {e}")
        return HTMLResponse("<h3 style='font-family:sans-serif;padding:40px;color:#ef4444'>Database unavailable.</h3>", status_code=503)

    rows_html = "".join(render_row(r) for r in rows)
    table = render_table_card("Redeemed Payments", len(rows), rows_html, "No redeemed payments.")
    return render_page("Redeemed", "redeem", table)


@router.get("/sms", response_class=HTMLResponse)
async def page_sms(request: Request):
    redir = _guard(request)
    if redir:
        return redir
    try:
        rows = await get_recent_sms(100)
    except Exception as e:
        logger.error(f"DB error on sms: {e}")
        return HTMLResponse("<h3 style='font-family:sans-serif;padding:40px;color:#ef4444'>Database unavailable.</h3>", status_code=503)

    rows_html = "".join(render_row(r) for r in rows)
    table = render_table_card("SMS Inbox", len(rows), rows_html, "No SMS received yet.")
    return render_page("SMS Inbox", "sms", table)
