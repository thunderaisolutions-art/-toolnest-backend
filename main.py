from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import uuid

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
        formats = []
        seen = set()
        for f in info["formats"]:
            res = f.get("resolution", "audio only")
            ext = f.get("ext")
            if res not in seen and f.get("url") and ext in ["mp4", "webm", "m4a"]:
                seen.add(res)
                formats.append({
                    "format_id": f["format_id"],
                    "ext": ext,
                    "resolution": res,
                })
        return {
            "title": info["title"],
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        }

@app.get("/download")
def download(url: str, format_id: str):
    filename = f"/tmp/{uuid.uuid4()}.%(ext)s"
    ydl_opts = {
        "format": format_id,
        "outtmpl": filename,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
    return FileResponse(
        filepath,
        filename=info["title"] + "." + info["ext"],
        media_type="application/octet-stream"
    )
