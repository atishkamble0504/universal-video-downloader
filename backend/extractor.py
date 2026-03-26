import yt_dlp
import re


def get_youtube_id(url: str):
    """Extract YouTube video ID from any YouTube URL"""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def extract_video_info(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,

        "js_runtimes": {
            "node": {
                "path": "C:\\Program Files\\nodejs\\node.exe"
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []
    all_formats = info.get("formats", [])

    # ==============================
    # 🔥 THUMBNAIL (FINAL SOLUTION)
    # ==============================

    thumbnail_url = ""

    # ✅ 1. FORCE YouTube thumbnail (PRIMARY FIX)
    youtube_id = get_youtube_id(url)
    if youtube_id:
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"

    # ✅ 2. fallback to yt-dlp thumbnails
    if not thumbnail_url:
        thumbnails = info.get("thumbnails", []) or []
        if thumbnails:
            thumbnail_url = thumbnails[-1].get("url", "")

    # ✅ 3. fallback to single thumbnail
    if not thumbnail_url:
        thumbnail_url = info.get("thumbnail", "") or ""

    # ✅ 4. final fallback
    if not thumbnail_url:
        thumbnail_url = "https://via.placeholder.com/400x220?text=No+Preview"

    # ==============================
    # 🔍 BEST AUDIO SIZE
    # ==============================

    best_audio_size = 0

    for f in all_formats:
        if f.get("acodec") != "none" and f.get("vcodec") == "none":
            size = f.get("filesize") or f.get("filesize_approx") or 0
            if size > best_audio_size:
                best_audio_size = size

    # ==============================
    # 🎯 VIDEO FORMATS
    # ==============================

    duration = info.get("duration", 0)

    for f in all_formats:

        if f.get("vcodec") == "none":
            continue

        if f.get("protocol") in ["m3u8", "m3u8_native"]:
            continue

        if not f.get("height"):
            continue

        format_id = f.get("format_id")
        height = f.get("height")
        quality = f.get("format_note") or f"{height}p"

        video_size = (
            f.get("filesize") or
            f.get("filesize_approx") or
            (f.get("tbr", 0) * 1024 * duration / 8)
        )

        total_size = video_size + best_audio_size

        size_mb = round(total_size / (1024 * 1024), 2) if total_size else 0

        formats.append({
            "format_id": format_id,
            "quality": quality,
            "height": height,
            "filesize": size_mb,
        })

    formats = sorted(formats, key=lambda x: x["height"], reverse=True)

    return {
        "title": info.get("title"),
        "thumbnail": thumbnail_url,   # 🔥 ALWAYS WORKS NOW
        "duration": info.get("duration"),
        "formats": formats
    }