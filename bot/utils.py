import yt_dlp
import os

# Load cookies file from ENV or default path
COOKIES_PATH = os.getenv("COOKIES_PATH", "cookies.txt")

def extract_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookies': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        'force_generic_extractor': False,  # Let yt-dlp detect extractor
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
    ydl_opts = {
        'outtmpl': output_path,
        'quiet': False,
        'cookies': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
