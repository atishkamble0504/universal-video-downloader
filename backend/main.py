from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os
import time
import re
import traceback

from extractor import extract_video_info
from downloader import download_video, progress_status
from cleanup import cleanup
from database import cursor, conn

app = FastAPI()

# ==============================
# Ensure storage folder exists
# ==============================

os.makedirs("storage", exist_ok=True)

# ==============================
# Enable CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Startup Cleanup
# ==============================

@app.on_event("startup")
def run_cleanup():
    cleanup()

# ==============================
# Request Models
# ==============================

class URLRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    format_id: str


# ==============================
# Validate URL
# ==============================

def is_valid_url(url: str):
    pattern = re.compile(r"^https?://")
    return pattern.match(url)


# ==============================
# Extract Video Metadata
# ==============================

@app.post("/extract")
def extract(data: URLRequest):

    if not data.url or not is_valid_url(data.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:

        info = extract_video_info(data.url)

        if not info or not info.get("formats"):
            raise HTTPException(
                status_code=400,
                detail="Unable to extract video formats"
            )

        return info

    except Exception as e:

        print("\n========= EXTRACT ERROR =========")
        print(str(e))
        traceback.print_exc()
        print("=================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==============================
# Download Video
# ==============================

@app.post("/download")
def download(data: DownloadRequest):

    if not data.url or not data.format_id:
        raise HTTPException(status_code=400, detail="Missing parameters")

    try:

        file_path = download_video(data.url, data.format_id)

        if not file_path or not os.path.exists(file_path):
            raise Exception("Download failed or file missing")

        filename = os.path.basename(file_path)

        # Try extracting title
        try:
            info = extract_video_info(data.url)
            title = info.get("title", "Unknown")
        except Exception:
            title = "Unknown"

        # Save history
        try:
            cursor.execute(
                "INSERT INTO downloads(title, filename) VALUES (?, ?)",
                (title, filename)
            )
            conn.commit()
        except Exception as db_error:
            print("Database error:", db_error)

        return {
            "download_url": f"http://127.0.0.1:8000/download-file/{filename}"
        }

    except Exception as e:

        print("\n========= DOWNLOAD ERROR =========")
        print(str(e))
        traceback.print_exc()
        print("==================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==============================
# Delete file after sending
# ==============================

def delete_file(path: str):

    time.sleep(300)

    if os.path.exists(path):
        os.remove(path)


# ==============================
# Force Browser Download
# ==============================

@app.get("/download-file/{filename}")
def download_file(filename: str, background_tasks: BackgroundTasks):

    path = os.path.join("storage", filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    background_tasks.add_task(delete_file, path)

    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=filename
    )


# ==============================
# Progress Endpoint
# ==============================

@app.get("/progress")
def get_progress():
    return progress_status


# ==============================
# Download History
# ==============================

@app.get("/history")
def get_history():

    rows = cursor.execute(
        "SELECT id, title, filename FROM downloads ORDER BY id DESC LIMIT 20"
    ).fetchall()

    return [
        {
            "id": r[0],
            "title": r[1],
            "filename": r[2]
        }
        for r in rows
    ]


# ==============================
# Delete One History Item
# ==============================

@app.delete("/history/{item_id}")
def delete_history_item(item_id: int):

    row = cursor.execute(
        "SELECT filename FROM downloads WHERE id=?",
        (item_id,)
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="History item not found")

    filename = row[0]
    filepath = os.path.join("storage", filename)

    # delete file
    if os.path.exists(filepath):
        os.remove(filepath)

    # delete database record
    cursor.execute(
        "DELETE FROM downloads WHERE id=?",
        (item_id,)
    )

    conn.commit()

    return {"message": "History item deleted"}


# ==============================
# Clear All History
# ==============================

@app.delete("/history")
def clear_history():

    rows = cursor.execute(
        "SELECT filename FROM downloads"
    ).fetchall()

    for r in rows:
        filepath = os.path.join("storage", r[0])
        if os.path.exists(filepath):
            os.remove(filepath)

    cursor.execute("DELETE FROM downloads")
    conn.commit()

    return {"message": "All history cleared"}


# ==============================
# Manual Cleanup
# ==============================

@app.get("/cleanup")
def manual_cleanup():

    now = time.time()

    for f in os.listdir("storage"):

        path = os.path.join("storage", f)

        if os.path.isfile(path):

            age = now - os.path.getmtime(path)

            if age > 3600:
                os.remove(path)

    return {"message": "Old files cleaned"}


# ==============================
# Static Storage Access
# ==============================

app.mount("/storage", StaticFiles(directory="storage"), name="storage")