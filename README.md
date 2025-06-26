# Telegram Video Downloader Bot

This bot allows users to download videos from public webpages and `.m3u8` streams by extracting available resolutions and formats using `yt-dlp`.

## Features

- Send webpage or M3U8 link
- Shows multiple download qualities
- Downloads and sends selected resolution

## Setup

1. Clone the repo
2. Add `.env` with your Telegram Bot Token
3. Run locally or deploy via Docker:

```bash
docker build -t video-bot .
docker run -e BOT_TOKEN=your_token video-bot
