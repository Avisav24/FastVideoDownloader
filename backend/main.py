# backend/main.py

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import uuid
import os
import asyncio
import shutil

app = FastAPI()

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class VideoRequest(BaseModel):
    url: str
    format_type: str = "mp4"

@app.post("/download")
async def download_video(data: VideoRequest):
    unique_id = str(uuid.uuid4())

    output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": data.format_type,
    }

    # If format requires merging (e.g., bestvideo+bestaudio), ensure ffmpeg is available
    needs_merge = "+" in ydl_opts.get("format", "")
    ffmpeg_path = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    if needs_merge and not ffmpeg_path:
        return JSONResponse(
            status_code=500,
            content={
                "error": (
                    "ffmpeg not found. Merging video and audio requires ffmpeg. "
                    "Install ffmpeg and add it to your PATH. See https://ffmpeg.org/download.html"
                )
            },
        )

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(data.url, download=True)

        info = await asyncio.to_thread(download)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    # find the downloaded file name in the downloads folder
    filename = None
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(unique_id):
            filename = f
            break

    if not filename:
        return JSONResponse(status_code=500, content={"error": "download failed or file not found"})

    return {
        "download_url": f"/file/{filename}",
        "title": info.get("title")
    }

@app.get("/file/{filename}")
async def get_file(filename: str):

    path = os.path.join(DOWNLOAD_DIR, filename)

    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=filename
    )


# Allow CORS from local frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)