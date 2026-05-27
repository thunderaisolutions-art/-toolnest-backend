from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import uuid
import os
import shutil
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ffmpeg detection ─────────────────────────────────────────────────────────
FFMPEG_PATH = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
print(f"[startup] ffmpeg resolved to: {FFMPEG_PATH}")


# ─── Cookies Setup ────────────────────────────────────────────────────────────
COOKIES_PATH = "/tmp/yt_cookies.txt"

def _setup_cookies():
    raw = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if raw:
        with open(COOKIES_PATH, "w") as f:
            f.write(raw)
        print(f"[startup] YouTube cookies loaded ({len(raw)} bytes)")
    else:
        print("[startup] No YOUTUBE_COOKIES env var found — running in cookieless mode (iOS/TV client)")

_setup_cookies()

def _cookies_opt() -> dict:
    if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0:
        return {"cookiefile": COOKIES_PATH}
    return {}


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    cookies_loaded = os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0
    return {
        "status": "Vexora Tools Backend Running",
        "ffmpeg": FFMPEG_PATH,
        "cookies": "loaded" if cookies_loaded else "not set (using client bypass)",
    }


# ─── Shared helpers ───────────────────────────────────────────────────────────

def _tmp(ext: str) -> str:
    return f"/tmp/{uuid.uuid4()}.{ext}"


def _base_opts() -> dict:
    """
    Common yt-dlp options for every call.

    YouTube's bot-detection fires when yt-dlp uses the default 'web' player
    client without cookies. Rotating through ios -> tv_embedded -> android_vr
    uses clients YouTube doesn't enforce the sign-in wall on.
    If cookies ARE available they're added on top as extra assurance.
    """
    opts = {
        "quiet": True,
        "ffmpeg_location": FFMPEG_PATH,
        # Use non-web player clients to bypass bot detection without cookies.
        # yt-dlp tries each in order and falls back automatically.
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "tv_embedded", "android_vr"],
            }
        },
        # Add cookies on top if available (belt-and-suspenders)
        **_cookies_opt(),
    }
    return opts


def _extract_info(url: str, extra: dict = None) -> dict:
    opts = {"noplaylist": True, **_base_opts(), **(extra or {})}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


# ─── 1. Video Info ────────────────────────────────────────────────────────────

@app.get("/video-info")
def video_info(url: str):
    try:
        info = _extract_info(url)
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    seen_res: set = set()
    formats = []

    for f in reversed(info.get("formats", [])):
        res    = f.get("resolution") or "audio only"
        ext    = f.get("ext", "")
        vcodec = f.get("vcodec", "none")
        acodec = f.get("acodec", "none")
        fid    = f.get("format_id", "")

        if vcodec == "none" and ext not in ("m4a", "mp3", "webm"):
            continue
        if vcodec != "none" and ext not in ("mp4", "webm"):
            continue
        if res in seen_res:
            continue

        seen_res.add(res)
        formats.append({
            "format_id":  fid,
            "ext":        ext,
            "resolution": res,
            "has_audio":  acodec != "none",
            "filesize":   f.get("filesize") or f.get("filesize_approx"),
        })

    video_fmts = [f for f in formats if f["resolution"] != "audio only"]
    audio_fmts = [f for f in formats if f["resolution"] == "audio only"]

    def _height(fmt):
        try:
            return int(fmt["resolution"].split("x")[-1])
        except Exception:
            return 0

    video_fmts.sort(key=_height, reverse=True)

    return {
        "title":     info.get("title", "video"),
        "thumbnail": info.get("thumbnail"),
        "duration":  info.get("duration"),
        "uploader":  info.get("uploader"),
        "platform":  info.get("extractor_key"),
        "formats":   video_fmts + audio_fmts,
    }


# ─── 2. Video Download ────────────────────────────────────────────────────────

@app.get("/download")
def download(url: str, format_id: str):
    out_tmpl = f"/tmp/{uuid.uuid4()}.%(ext)s"
    ydl_opts = {
        **_base_opts(),
        "format":  f"{format_id}+bestaudio[ext=m4a]/bestaudio/{format_id}/{format_id}",
        "outtmpl": out_tmpl,
        "merge_output_format": "mp4",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info     = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            if not os.path.exists(filepath):
                base = os.path.splitext(filepath)[0]
                for ext in ("mp4", "webm", "mkv"):
                    if os.path.exists(f"{base}.{ext}"):
                        filepath = f"{base}.{ext}"
                        break
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    safe_title = "".join(c for c in info.get("title", "video") if c.isalnum() or c in " _-")
    ext        = os.path.splitext(filepath)[-1].lstrip(".")
    return FileResponse(filepath, filename=f"{safe_title}.{ext}", media_type="application/octet-stream")


# ─── 3. Audio / MP3 Download ─────────────────────────────────────────────────

@app.get("/audio-download")
def audio_download(url: str):
    out_path = _tmp("%(ext)s")
    ydl_opts = {
        **_base_opts(),
        "format":  "bestaudio/best",
        "outtmpl": out_path,
        "postprocessors": [{
            "key":              "FFmpegExtractAudio",
            "preferredcodec":   "mp3",
            "preferredquality": "192",
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base = os.path.splitext(ydl.prepare_filename(info))[0]
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    filepath = f"{base}.mp3"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail="MP3 conversion failed.")

    safe_title = "".join(c for c in info.get("title", "audio") if c.isalnum() or c in " _-")
    return FileResponse(filepath, filename=f"{safe_title}.mp3", media_type="audio/mpeg")


# ─── 4. Video to GIF ─────────────────────────────────────────────────────────

@app.get("/video-to-gif")
def video_to_gif(url: str, start: float = 0, duration: float = 5, width: int = 480):
    if duration > 30:
        raise HTTPException(status_code=400, detail="Maximum GIF duration is 30 seconds.")
    if width > 1280:
        raise HTTPException(status_code=400, detail="Maximum GIF width is 1280 px.")

    src_path = _tmp("mp4")
    ydl_opts = {
        **_base_opts(),
        "format":  "bestvideo[height<=720][ext=mp4]/bestvideo[height<=720]/best[height<=720]",
        "outtmpl": src_path,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            src  = ydl.prepare_filename(info)
            if not os.path.exists(src):
                src = src_path
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    palette_path = _tmp("png")
    out_gif      = _tmp("gif")

    try:
        subprocess.run([
            FFMPEG_PATH, "-y",
            "-ss", str(start), "-t", str(duration), "-i", src,
            "-vf", f"fps=12,scale={width}:-1:flags=lanczos,palettegen",
            palette_path,
        ], check=True, capture_output=True)

        subprocess.run([
            FFMPEG_PATH, "-y",
            "-ss", str(start), "-t", str(duration), "-i", src,
            "-i", palette_path,
            "-filter_complex", f"fps=12,scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
            out_gif,
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="GIF conversion failed: " + e.stderr.decode(errors="ignore"))

    safe_title = "".join(c for c in info.get("title", "clip") if c.isalnum() or c in " _-")
    return FileResponse(out_gif, filename=f"{safe_title}.gif", media_type="image/gif")


# ─── 5. Video Trimmer ────────────────────────────────────────────────────────

@app.get("/video-trim")
def video_trim(url: str, start: float = 0, end: float = 30):
    if end <= start:
        raise HTTPException(status_code=400, detail="end must be greater than start.")
    if (end - start) > 600:
        raise HTTPException(status_code=400, detail="Maximum clip length is 10 minutes.")

    src_path = _tmp("mp4")
    ydl_opts = {
        **_base_opts(),
        "format":  "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": src_path,
        "merge_output_format": "mp4",
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            src  = ydl.prepare_filename(info)
            if not os.path.exists(src):
                base = os.path.splitext(src)[0]
                for ext in ("mp4", "mkv", "webm"):
                    if os.path.exists(f"{base}.{ext}"):
                        src = f"{base}.{ext}"
                        break
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    out_mp4 = _tmp("mp4")
    try:
        subprocess.run([
            FFMPEG_PATH, "-y",
            "-ss", str(start), "-to", str(end),
            "-i", src,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            out_mp4,
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Trim failed: " + e.stderr.decode(errors="ignore"))

    safe_title = "".join(c for c in info.get("title", "clip") if c.isalnum() or c in " _-")
    return FileResponse(out_mp4, filename=f"{safe_title}_trimmed.mp4", media_type="video/mp4")
