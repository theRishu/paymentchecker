from datetime import datetime
from config import DASHBOARD_PASSCODE

# ── CSS ─────────────────────────────────────────────────────────────────────

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:        #f0f2f5;
  --surface:   #ffffff;
  --border:    #e2e8f0;
  --border-2:  #edf0f4;
  --text-1:    #0f172a;
  --text-2:    #475569;
  --text-3:    #94a3b8;
  --accent:    #6366f1;
  --accent-lt: #eef2ff;
  --green:     #10b981;
  --green-lt:  #d1fae5;
  --amber:     #f59e0b;
  --amber-lt:  #fef3c7;
  --blue:      #3b82f6;
  --blue-lt:   #dbeafe;
  --red:       #ef4444;
  --red-lt:    #fee2e2;
  --radius:    10px;
  --shadow:    0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text-1);
  font-size: 13.5px;
  line-height: 1.6;
  min-height: 100vh;
}

/* ── Layout ── */
.layout { display: flex; flex-direction: column; min-height: 100vh; }

.topbar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 28px;
  height: 58px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: .95rem;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -.02em;
}

.brand-dot {
  width: 8px; height: 8px;
  background: var(--accent);
  border-radius: 50%;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--green-lt);
  color: #065f46;
  font-size: .72rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  letter-spacing: .03em;
  text-transform: uppercase;
}

.live-badge::before {
  content: '';
  width: 6px; height: 6px;
  background: var(--green);
  border-radius: 50%;
  animation: pulse 1.8s infinite;
}

@keyframes pulse { 0%,100%{opacity:.5} 50%{opacity:1} }

.logout-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--text-2);
  font-size: .8rem;
  font-weight: 500;
  text-decoration: none;
  padding: 6px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  transition: all .15s;
}
.logout-btn:hover { background: var(--bg); color: var(--text-1); }

/* ── Nav ── */
.subnav {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 28px;
  display: flex;
  gap: 2px;
}

.subnav a {
  padding: 11px 14px;
  color: var(--text-2);
  text-decoration: none;
  font-weight: 500;
  font-size: .85rem;
  border-bottom: 2px solid transparent;
  transition: all .15s;
}
.subnav a:hover { color: var(--text-1); }
.subnav a.active { color: var(--accent); border-bottom-color: var(--accent); }

/* ── Main content ── */
.main { padding: 28px; flex: 1; }

/* ── Stats ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 22px;
  box-shadow: var(--shadow);
}

.stat-label {
  font-size: .7rem;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -.03em;
  line-height: 1;
}

.stat-value.accent { color: var(--accent); }
.stat-value.green  { color: var(--green); }
.stat-value.amber  { color: var(--amber); }

.stat-sub {
  font-size: .75rem;
  color: var(--text-3);
  margin-top: 6px;
}

/* ── Card ── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}

.card-head {
  padding: 14px 20px;
  border-bottom: 1px solid var(--border-2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #fafbfc;
}

.card-head h2 {
  font-size: .9rem;
  font-weight: 600;
  color: var(--text-1);
}

.card-meta {
  font-size: .78rem;
  color: var(--text-3);
  margin-left: 6px;
  font-weight: 400;
}

.search {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 11px;
  font-size: .82rem;
  width: 210px;
  outline: none;
  color: var(--text-1);
  font-family: inherit;
  transition: border-color .15s, box-shadow .15s;
}
.search:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(99,102,241,.12);
}

/* ── Table ── */
.table-wrap { overflow-x: auto; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: .84rem;
}

thead th {
  font-size: .68rem;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: .06em;
  text-align: left;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
  background: #fafbfc;
  white-space: nowrap;
}

tbody td {
  padding: 13px 16px;
  border-bottom: 1px solid var(--border-2);
  color: var(--text-1);
  vertical-align: middle;
}

tbody tr:last-child td { border-bottom: 0; }
tbody tr:hover td { background: #f8fafc; }

/* ── Table cell types ── */
.utr-cell {
  font-family: 'SF Mono', 'Fira Code', Menlo, monospace;
  font-size: .8rem;
  color: var(--text-1);
  background: var(--bg);
  padding: 3px 8px;
  border-radius: 5px;
  border: 1px solid var(--border);
  font-weight: 500;
  white-space: nowrap;
}

.amount-cell {
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  color: var(--text-1);
}

.amount-cell.zero { color: var(--text-3); font-weight: 400; }

.muted { color: var(--text-2); font-size: .8rem; font-variant-numeric: tabular-nums; }
.dash  { color: var(--text-3); }

/* ── Badges ── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 9px;
  border-radius: 20px;
  font-size: .72rem;
  font-weight: 600;
  letter-spacing: .01em;
  white-space: nowrap;
}

.badge::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

.badge-green  { background: var(--green-lt); color: #065f46; }
.badge-green::before  { background: var(--green); }

.badge-blue   { background: var(--blue-lt);  color: #1e40af; }
.badge-blue::before   { background: var(--blue); }

.badge-amber  { background: var(--amber-lt); color: #92400e; }
.badge-amber::before  { background: var(--amber); }

.badge-neutral{ background: var(--border);   color: var(--text-2); }
.badge-neutral::before{ background: var(--text-3); }

/* ── Empty state ── */
.empty {
  text-align: center;
  padding: 64px 20px;
  color: var(--text-3);
}
.empty-icon { font-size: 2rem; margin-bottom: 10px; opacity: .5; }
.empty p { font-size: .85rem; }

/* ── Footer bar ── */
.footbar {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 8px 28px;
  font-size: .76rem;
  color: var(--text-3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}

.refresh-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.refresh-indicator::before {
  content: '';
  width: 6px; height: 6px;
  background: var(--accent);
  border-radius: 50%;
  animation: pulse 1.8s infinite;
}
"""

# ── Helpers ─────────────────────────────────────────────────────────────────

def get_state(r) -> tuple[str, str]:
    if r.redeemed:                 return ("Redeemed",    "badge-green")
    if r.amount and r.user_id:     return ("Processing",  "badge-blue")
    if r.amount and not r.user_id: return ("SMS Only",    "badge-neutral")
    if not r.amount and r.user_id: return ("Pending SMS", "badge-amber")
    return ("Unknown", "badge-neutral")


def _td_time(d) -> str:
    if not d:
        return "<td class='dash'>—</td>"
    full = d.strftime('%d %b %Y, %H:%M:%S')
    short = d.strftime('%d %b · %H:%M')
    return f"<td class='muted' title='{full}'>{short}</td>"


def render_row(r) -> str:
    label, klass = get_state(r)
    amt   = f"<td><span class='amount-cell'>₹{r.amount:,.2f}</span></td>" if r.amount else "<td><span class='amount-cell zero'>—</span></td>"
    user  = f"<td><span class='utr-cell'>{r.user_id}</span></td>" if r.user_id else "<td class='dash'>—</td>"
    uname = f"<td class='muted'>@{r.username}</td>" if r.username else "<td class='dash'>—</td>"
    bot   = f"<td class='muted'>{r.bot_name}</td>" if r.bot_name else "<td class='dash'>—</td>"
    days  = f"<td><span class='badge badge-neutral'>{r.days}d</span></td>" if r.days else "<td class='dash'>—</td>"
    sndr  = f"<td class='muted'>{r.sender[:30]}</td>" if r.sender else "<td class='dash'>—</td>"

    del_btn = f"<button class='del-btn' onclick='delUtr(\"{r.utr}\")'>🗑️</button>"

    return (
        f"<tr id='row-{r.utr}'>"
        f"<td><span class='utr-cell'>{r.utr}</span></td>"
        f"<td><span class='badge {klass}'>{label}</span></td>"
        f"{amt}{sndr}{user}{uname}{bot}{days}"
        f"{_td_time(r.sms_at)}{_td_time(r.submitted_at)}{_td_time(r.redeemed_at)}"
        f"<td>{del_btn}</td>"
        f"</tr>"
    )


# ── Page shell ───────────────────────────────────────────────────────────────

def render_page(title: str, active: str, body: str) -> str:
    now = datetime.now().strftime("%d %b %Y · %H:%M:%S")

    def nav_link(href, label, key):
        cls = " class='active'" if active == key else ""
        return f"<a href='{href}'{cls}>{label}</a>"

    # Add delete button styles to CSS
    extra_css = """
    .del-btn {
        background: none; border: none; cursor: pointer; padding: 4px 8px;
        border-radius: 4px; color: var(--red); opacity: 0.6; transition: all 0.15s;
    }
    .del-btn:hover { background: var(--red-lt); opacity: 1; transform: scale(1.1); }
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Botsphere Payments</title>
  <style>{_CSS}{extra_css}</style>
</head>
<body>
<div class="layout">

  <header class="topbar">
    <div class="brand">
      <span class="brand-dot"></span>
      Botsphere Payments
    </div>
    <div class="topbar-right">
      <span class="live-badge">Live · Admin</span>
      <a href="/logout" class="logout-btn">Sign out</a>
    </div>
  </header>

  <nav class="subnav">
    {nav_link("/",         "Overview",  "all")}
    {nav_link("/pending",  "Pending",   "pending")}
    {nav_link("/redeemed", "Redeemed",  "redeem")}
    {nav_link("/sms",      "SMS Inbox", "sms")}
  </nav>

  <main class="main">
    {body}
  </main>

</div>

<div class="footbar">
  <span>Updated {now}</span>
  <span class="refresh-indicator">Refresh in <span id="cd">15</span>s</span>
</div>

<script>
  let t = 15;
  const timer = setInterval(() => {{
    const el = document.getElementById('cd');
    if (el) el.textContent = --t;
    if (t <= 0) location.reload();
  }}, 1000);

  async function delUtr(utr) {{
    if (!confirm(`Delete UTR ${{utr}}?`)) return;
    try {{
      const r = await fetch(`/delete/${{utr}}`, {{ method: 'POST' }});
      if (r.ok) {{
        document.getElementById(`row-${{utr}}`)?.remove();
      }} else {{
        alert('Delete failed');
      }}
    }} catch (e) {{
      alert('Error: ' + e);
    }}
  }}

  document.querySelectorAll('.search').forEach(s => {{
    s.addEventListener('input', e => {{
      const q = e.target.value.toLowerCase();
      s.closest('.card').querySelectorAll('tbody tr').forEach(r => {{
        r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
      }});
    }});
  }});
</script>
</body>
</html>"""


# ── Stats cards ──────────────────────────────────────────────────────────────

def render_stats(sms_rows, pending_rows, redeemed_rows) -> str:
    total_amount = sum(r.amount for r in redeemed_rows if r.amount)
    return f"""<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-label">SMS Received</div>
    <div class="stat-value accent">{len(sms_rows)}</div>
    <div class="stat-sub">last 100 records</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Pending</div>
    <div class="stat-value amber">{len(pending_rows)}</div>
    <div class="stat-sub">awaiting SMS match</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Redeemed</div>
    <div class="stat-value green">{len(redeemed_rows)}</div>
    <div class="stat-sub">VIP granted</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Total Redeemed</div>
    <div class="stat-value green">₹{total_amount:,.0f}</div>
    <div class="stat-sub">confirmed payments</div>
  </div>
</div>"""


# ── Table card ───────────────────────────────────────────────────────────────

_TH = (
    "<thead><tr>"
    "<th>UTR</th><th>Status</th><th>Amount</th><th>Sender</th>"
    "<th>User ID</th><th>Username</th><th>Bot</th><th>Plan</th>"
    "<th>SMS At</th><th>Submitted</th><th>Redeemed</th>"
    "<th>Actions</th>"
    "</tr></thead>"
)


def render_table_card(title: str, count: int, rows_html: str, empty_msg: str) -> str:
    empty = (
        f"<tr><td colspan='12'>"
        f"<div class='empty'><div class='empty-icon'>💳</div><p>{empty_msg}</p></div>"
        f"</td></tr>"
        f"<script>t=999;</script>" # Pause refresh on error/empty
    )
    return f"""<div class="card">
  <div class="card-head">
    <h2>{title}<span class="card-meta">· {count} records</span></h2>
    <input class="search" type="text" placeholder="Search UTR, user, sender…">
  </div>
  <div class="table-wrap">
    <table>{_TH}<tbody>
      {rows_html if rows_html else empty}
    </tbody></table>
  </div>
</div>"""
