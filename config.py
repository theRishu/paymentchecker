BOT_TOKEN     = "8745643689:AAGOPhtvnFbUy0RRnWwCEWaSP3ULAue3eos"

SMS_INPUT_CHANNEL   = -1003936723766
SUBMISSION_CHANNEL = -1003938967069   # channel for user-submitted UTRs & screenshots
ADMIN_CHAT_ID      = 8419808109
API_KEY       = "botspheresecret123"

DATABASE_URL  = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/payment"

DASHBOARD_PASSCODE = "rishu"

# Map each bot_name to its internal callback URL.
# Add one entry per bot using the port assigned in botsrc/bots.json.
BOT_CALLBACKS: dict[str, str] = {
    "botsrc": "http://127.0.0.1:8088/internal/grant_vip",
}
