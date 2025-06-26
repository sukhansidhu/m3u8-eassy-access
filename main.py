import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from bot.handlers import start, process_url, button_handler, live_matches

# Load environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in .env or environment variables")

# Build Telegram app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register command and message handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("live", live_matches))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_url))
app.add_handler(CallbackQueryHandler(button_handler))

# Start bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    app.run_polling()
