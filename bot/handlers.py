import aiohttp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def live_matches(update, context):
    await update.message.reply_text("Fetching SonyLIV Live Matches...")

    async with aiohttp.ClientSession() as session:
        async with session.get("https://raw.githubusercontent.com/abid58b/SonyLivPlayList/main/sonyliv.json") as resp:
            if resp.status != 200:
                await update.message.reply_text("Failed to fetch live data.")
                return
            data = await resp.json()

    keyboard = []
    for match in data.get("matches", []):
        name = match.get("match_name") or match["event_name"]
        url = match["video_url"]
        keyboard.append([InlineKeyboardButton(text=name, url=url)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎥 Select a Live Match:", reply_markup=reply_markup)
