import yt_dlp

def extract_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                "format_id": f["format_id"],
                "ext": f["ext"],
                "resolution": f.get("resolution") or f"{f.get('width')}x{f.get('height')}",
                "url": f["url"]
            }
            for f in info.get("formats", []) if f.get("vcodec") != "none"
        ]
        return formats, info.get("title", "Video")

def download_video(url, output):
    ydl_opts = {
        'outtmpl': output,
        'quiet': True,
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
