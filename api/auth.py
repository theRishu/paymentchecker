from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from config import DASHBOARD_PASSCODE

router = APIRouter()

_LOGIN_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Inter','Segoe UI',sans-serif;
     background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}
.box{background:#fff;padding:40px;border-radius:12px;
     box-shadow:0 4px 24px rgba(0,0,0,.08);width:340px}
.brand{font-size:1.05rem;font-weight:700;color:#0f172a;margin-bottom:4px;letter-spacing:-.02em}
.sub{font-size:.83rem;color:#64748b;margin-bottom:28px}
label{display:block;font-size:.72rem;font-weight:600;color:#94a3b8;
      margin-bottom:6px;letter-spacing:.05em;text-transform:uppercase}
input{width:100%;padding:11px 13px;border:1px solid #e2e8f0;border-radius:6px;
      outline:none;font-size:.9rem;color:#0f172a;transition:border-color .15s}
input:focus{border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.12)}
button{width:100%;padding:12px;background:#6366f1;color:#fff;border:none;
       border-radius:6px;cursor:pointer;font-weight:600;font-size:.9rem;
       margin-top:16px;transition:background .15s}
button:hover{background:#4f46e5}
.error{margin-top:12px;color:#ef4444;font-size:.82rem;text-align:center}
"""


def _login_html(error: bool = False) -> str:
    err = "<p class='error'>Incorrect access code. Try again.</p>" if error else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login — Botsphere Payments</title>
<style>{_LOGIN_CSS}</style>
</head><body>
<div class="box">
  <div class="brand">Botsphere Payments</div>
  <p class="sub">Enter your access code to continue.</p>
  <form action="/login" method="post">
    <label>Access Code</label>
    <input type="password" name="code" placeholder="••••••••" required autofocus>
    <button type="submit">Unlock Dashboard</button>
  </form>
  {err}
</div>
</body></html>"""


def is_authenticated(request: Request) -> bool:
    return request.cookies.get("access_code") == DASHBOARD_PASSCODE


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/", status_code=302)
    error = bool(request.query_params.get("error"))
    return _login_html(error)


@router.post("/login")
async def do_login(request: Request):
    form = await request.form()
    code = form.get("code", "")
    if code == DASHBOARD_PASSCODE:
        resp = RedirectResponse(url="/", status_code=302)
        resp.set_cookie(key="access_code", value=code, httponly=True, samesite="lax")
        return resp
    return RedirectResponse(url="/login?error=1", status_code=302)


@router.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=302)
    resp.delete_cookie("access_code")
    return resp
