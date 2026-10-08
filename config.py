BOT_TOKEN     = "8745643689:AAHAnscoVFv9uxbt2T0wmdAOjgPLGlHP69E"

# Webhook delivery instead of long-polling: Telegram retries delivery on
# failure, so we no longer depend on catching every getUpdates cycle at
# exactly the right moment.
WEBHOOK_PATH   = "/pc-hook/tg/8f3a1c9e2b7d4f6091ac5e8b3d2f7a41"
WEBHOOK_URL    = "https://randommeetbot.com" + WEBHOOK_PATH
WEBHOOK_SECRET = "nUgx8tU_ewonV_e1SS3ZxkNNiI9Hh4G-"

SMS_INPUT_CHANNEL   = -1003936723766
SUBMISSION_CHANNEL = -1003938967069   # channel for user-submitted UTRs & screenshots
ADMIN_CHAT_ID      = 8419808109
API_KEY       = "botspheresecret123"

DATABASE_URL  = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/payment"

DASHBOARD_PASSCODE = "rishu"

# Map each bot's real Telegram @username (as stored in utrs.bot_name) to its
# internal grant_vip callback URL. Ports must match botsrc/config.py's
# FLEET_API_PORTS exactly — one process per bot, one port per process.
# Bots not listed here (e.g. RandomMeetBot, TalkNGo) don't need an entry: they
# were never listening for a push anyway and rely entirely on their own local
# 30s poller, which already works independently of this.
BOT_CALLBACKS: dict[str, str] = {
    "ArabMeetBot": "http://127.0.0.1:8201/internal/grant_vip",
    "BengaliMeetbot": "http://127.0.0.1:8202/internal/grant_vip",
    "ChatIncognitoinBot": "http://127.0.0.1:8203/internal/grant_vip",
    "DonutBanana_Robot": "http://127.0.0.1:8204/internal/grant_vip",
    "EnglishMeetBot": "http://127.0.0.1:8205/internal/grant_vip",
    "GayMeetBot": "http://127.0.0.1:8206/internal/grant_vip",
    "GlobalMeetBot": "http://127.0.0.1:8207/internal/grant_vip",
    "IndoMeetBot": "http://127.0.0.1:8208/internal/grant_vip",
    "IndonesiaMeetBot": "http://127.0.0.1:8209/internal/grant_vip",
    "KannadaMeetBot": "http://127.0.0.1:8210/internal/grant_vip",
    "KeralaMeetBot": "http://127.0.0.1:8211/internal/grant_vip",
    "MalluMeetBot": "http://127.0.0.1:8212/internal/grant_vip",
    "RandChatsBot": "http://127.0.0.1:8213/internal/grant_vip",
    "RandomModebot": "http://127.0.0.1:8214/internal/grant_vip",
    "RandomlyMeetBot": "http://127.0.0.1:8220/internal/grant_vip",
    "RandsChatBot": "http://127.0.0.1:8215/internal/grant_vip",
    "sextingbuddiesbot": "http://127.0.0.1:8216/internal/grant_vip",
    "sextingchatbot": "http://127.0.0.1:8217/internal/grant_vip",
    "TeluguMeetBot": "http://127.0.0.1:8218/internal/grant_vip",
    "xo_xorobot": "http://127.0.0.1:8219/internal/grant_vip",
}
