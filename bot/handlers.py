import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from .utils import extract_formats, download_video

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 *Welcome to the Video Downloader Bot!*\n\n"
        "Just send a video link (m3u8, mp4, or page), and I'll fetch the formats for you.",
        parse_mode="Markdown"
    )

# Handle plain text URL message
async def process_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🔍 Extracting formats, please wait...")

    try:
        formats, title = extract_formats(url)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
        return

    if not formats:
        await update.message.reply_text("⚠️ No downloadable formats found.")
        return

    # Save link and formats in user context
    context.user_data['url'] = url
    context.user_data['formats'] = formats
    context.user_data['title'] = title

    # Create button list
    buttons = [
        [InlineKeyboardButton(f"{f['resolution']} ({f['ext']})", callback_data=f["format_id"])]
        for f in formats
    ]
    markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"✅ Found *{len(formats)}* formats for *{title}*\n\nSelect one to download:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Handle button click
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_format = query.data
    formats = context.user_data.get("formats", [])
    url = context.user_data.get("url")
    title = context.user_data.get("title", "video")

    match = next((f for f in formats if f["format_id"] == selected_format), None)
    if not match:
        await query.edit_message_text("❌ Format not found.")
        return

    filename = f"{title.replace(' ', '_')}.{match['ext']}"
    await query.edit_message_text(f"📥 Downloading {match['resolution']}...")

    try:
        download_video(url, filename)
        await query.message.reply_video(video=open(filename, "rb"), caption=title)
        os.remove(filename)
    except Exception as e:
        await query.edit_message_text(f"❌ Download failed: {str(e)}")
