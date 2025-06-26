import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.utils import extract_formats, download_video

user_video_info = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📽️ Send a webpage or m3u8 link to download video.")

async def process_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🔍 Extracting video info...")
    try:
        formats, title = extract_formats(url)
        if not formats:
            await update.message.reply_text("❌ No downloadable formats found.")
            return

        keyboard = [
            [InlineKeyboardButton(f"{f['resolution']} ({f['ext']})", callback_data=f['url'])]
            for f in formats[:10]  # max 10 buttons
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_video_info[update.effective_user.id] = (title, url)
        await update.message.reply_text(f"🎬 *{title}*\nChoose quality to download:", reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to extract video.\n{str(e)}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    url = query.data
    user_id = query.from_user.id
    title, _ = user_video_info.get(user_id, ("video", url))

    filename = f"{title.replace(' ', '_')}.mp4"
    await query.edit_message_text("📥 Downloading...")
    download_video(url, filename)
    await context.bot.send_video(chat_id=query.message.chat_id, video=open(filename, 'rb'), caption=title)
    os.remove(filename)
