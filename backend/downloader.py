import yt_dlp
import uuid
import os
import re

# ==============================
# Download Progress
# ==============================

progress_status = {
    "percent": "0%",
    "speed": "",
    "eta": "",
    "downloaded": ""
}

# ==============================
# Remove ANSI color codes
# ==============================

def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\x1b\[[0-9;]*m", "", str(text)).strip()

# ==============================
# Progress Hook
# ==============================

def progress_hook(d):
    if d["status"] == "downloading":
        progress_status["percent"] = clean_text(d.get("_percent_str", "0%"))
        progress_status["speed"] = clean_text(d.get("_speed_str", ""))
        progress_status["eta"] = clean_text(d.get("_eta_str", ""))
        progress_status["downloaded"] = clean_text(d.get("_downloaded_bytes_str", ""))

    elif d["status"] == "finished":
        progress_status["percent"] = "100%"
        progress_status["speed"] = ""
        progress_status["eta"] = ""

# ==============================
# Download Function
# ==============================

def download_video(url: str, format_id: str):
    print("SELECTED FORMAT ID:", format_id)

    # Reset progress
    progress_status["percent"] = "0%"
    progress_status["speed"] = ""
    progress_status["eta"] = ""
    progress_status["downloaded"] = ""

    os.makedirs("storage", exist_ok=True)

    # ==============================
    # COMMON SETTINGS
    # ==============================

    common_opts = {
        # ✅ FORCE NODE
        "js_runtimes": {
            "node": {
                "path": "C:\\Program Files\\nodejs\\node.exe"
            }
        },

        # ✅ FORCE CORRECT FFMPEG PATH (THIS FIXES AUDIO 🔥)
        "ffmpeg_location": "C:\\ffmpeg\\ffmpeg-8.0.1-essentials_build\\bin",

        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "quiet": False,

        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        }
    }

    # ==============================
    # MP3 DOWNLOAD
    # ==============================

    if format_id == "mp3":
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("storage", filename)

        ydl_opts = {
            **common_opts,
            "format": "bestaudio/best",
            "outtmpl": filepath,

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return filepath

    # ==============================
    # VIDEO DOWNLOAD
    # ==============================

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join("storage", filename)

    ydl_opts = {
        **common_opts,

        # ✅ ALWAYS MERGE VIDEO + AUDIO
        "format": f"{format_id}+bestaudio[ext=m4a]/{format_id}+bestaudio/best",

        "merge_output_format": "mp4",
        "outtmpl": os.path.join("storage", "%(id)s.%(ext)s"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]

    # ==============================
    # Find merged file
    # ==============================

    merged_file = None

    for f in os.listdir("storage"):
        if f.startswith(video_id) and f.endswith((".mp4", ".mkv", ".webm")):
            merged_file = os.path.join("storage", f)
            break

    if not merged_file:
        raise Exception("Merged file not found after download")

    os.rename(merged_file, filepath)

    return filepath