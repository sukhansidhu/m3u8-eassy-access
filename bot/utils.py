import yt_dlp
import os

# Domain to cookies mapping
COOKIE_MAP = {
    "sonyliv.com": "cookies/sonyliv.txt",
    "zee5.com": "cookies/zee5.txt",
    "jiocinema.com": "cookies/jio.txt",
    "hotstar.com": "cookies/hotstar.txt",
}

# Get correct cookies file
def get_cookie_path(url):
    for domain, path in COOKIE_MAP.items():
        if domain in url:
            full_path = os.path.join(os.getcwd(), path)
            if os.path.exists(full_path):
                return full_path
    return None

# Extract formats (m3u8/mp4)
def extract_formats(url):
    cookie_file = get_cookie_path(url)
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookies': cookie_file,
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

# Download selected format
def download_video(url, output_path):
    cookie_file = get_cookie_path(url)
    ydl_opts = {
        'outtmpl': output_path,
        'quiet': False,
        'cookies': cookie_file,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
