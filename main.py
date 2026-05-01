from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ToolNest Backend Running"}

@app.get("/download-info")
def download_info(url: str):
    ydl_opts = {"quiet": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                "format_id": f["format_id"],
                "ext": f["ext"],
                "resolution": f.get("resolution", "audio only"),
                "url": f["url"],
            }
            for f in info["formats"]
            if f.get("url")
        ]
        return {"title": info["title"], "thumbnail": info.get("thumbnail"), "formats": formats}
