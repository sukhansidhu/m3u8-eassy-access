import yt_dlp
import os

def get_cookies_for_url(url):
    if "zee5.com" in url:
        return "cookies/zee5.txt"
    elif "sonyliv.com" in url:
        return "cookies/sonyliv.txt"
    elif "hotstar.com" in url:
        return "cookies/hotstar.txt"
    return None

def extract_formats(url):
    cookies = get_cookies_for_url(url)
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookies': cookies if cookies and os.path.exists(cookies) else None,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") != "none":
                formats.append({
                    "format_id": f["format_id"],
                    "ext": f["ext"],
                    "resolution": f.get("resolution") or f"{f.get('width')}x{f.get('height')}",
                    "url": f["url"]
                })
        return formats, info.get("title", "Video")

def download_video(url, output_path):
    cookies = get_cookies_for_url(url)
    ydl_opts = {
        'outtmpl': output_path,
        'quiet': False,
        'cookies': cookies if cookies and os.path.exists(cookies) else None,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
