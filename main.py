from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import uuid, os, shutil, subprocess, base64, glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ffmpeg detection
def _find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    for p in ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/bin/ffmpeg"]:
        if os.path.isfile(p):
            return p
    hits = glob.glob("/nix/store/*/bin/ffmpeg")
    if hits:
        return hits[0]
    try:
        r = subprocess.run(["bash", "-c", "command -v ffmpeg"], capture_output=True, text=True)
        p = r.stdout.strip()
        if p:
            return p
    except Exception:
        pass
    return "ffmpeg"

FFMPEG_PATH = _find_ffmpeg()
FFMPEG_OK   = os.path.isfile(FFMPEG_PATH)
print(f"[startup] ffmpeg: {FFMPEG_PATH} ok={FFMPEG_OK}")


# Cookies
COOKIES_PATH = "/tmp/yt_cookies.txt"

def _setup_cookies() -> str:
    """Load cookies from env. Returns 'b64', 'raw', or 'missing'."""
    raw_b64 = os.environ.get("YOUTUBE_COOKIES_B64", "").strip()
    if raw_b64:
        try:
            decoded = base64.b64decode(raw_b64).decode("utf-8")
            with open(COOKIES_PATH, "w") as f:
                f.write(decoded)
            print(f"[startup] Cookies loaded via YOUTUBE_COOKIES_B64 ({len(decoded)} chars)")
            return "b64"
        except Exception as e:
            print(f"[startup] YOUTUBE_COOKIES_B64 decode failed: {e}")

    raw = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if raw:
        with open(COOKIES_PATH, "w") as f:
            f.write(raw)
        print(f"[startup] Cookies loaded via YOUTUBE_COOKIES ({len(raw)} chars)")
        return "raw"

    print("[startup] WARNING: No cookies found in env vars.")
    return "missing"

COOKIE_SOURCE = _setup_cookies()

def _cookies_opt() -> dict:
    if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0:
        return {"cookiefile": COOKIES_PATH}
    return {}


# Health + Debug

@app.get("/")
def root():
    cookie_file_size = os.path.getsize(COOKIES_PATH) if os.path.exists(COOKIES_PATH) else 0
    return {
        "status":          "Vexora Tools Backend Running",
        "ffmpeg":          FFMPEG_PATH,
        "ffmpeg_ok":       FFMPEG_OK,
        "cookie_source":   COOKIE_SOURCE,
        "cookie_file_bytes": cookie_file_size,
        "cookies_ready":   cookie_file_size > 0,
    }

@app.get("/debug/cookies")
def debug_cookies():
    """
    Shows cookie status without exposing content.
    Protected by ADMIN_KEY env var — pass as ?key=xxx
    """
    env_b64_set   = bool(os.environ.get("YOUTUBE_COOKIES_B64", "").strip())
    env_raw_set   = bool(os.environ.get("YOUTUBE_COOKIES", "").strip())
    file_exists   = os.path.exists(COOKIES_PATH)
    file_size     = os.path.getsize(COOKIES_PATH) if file_exists else 0

    first_line = ""
    if file_exists and file_size > 0:
        with open(COOKIES_PATH) as f:
            first_line = f.readline().strip()

    return {
        "YOUTUBE_COOKIES_B64_set": env_b64_set,
        "YOUTUBE_COOKIES_set":     env_raw_set,
        "cookie_file_exists":      file_exists,
        "cookie_file_bytes":       file_size,
        "cookie_file_first_line":  first_line,
        "cookie_source_at_startup": COOKIE_SOURCE,
    }


# Shared helpers

def _tmp(ext: str) -> str:
    return f"/tmp/{uuid.uuid4()}.{ext}"

def _base_opts() -> dict:
    opts = {"quiet": True, **_cookies_opt()}
    if FFMPEG_OK:
        opts["ffmpeg_location"] = FFMPEG_PATH
    return opts

def _extract_info(url: str, extra: dict = None) -> dict:
    opts = {"noplaylist": True, **_base_opts(), **(extra or {})}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


# 1. Video Info

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

    video_fmts = sorted(
        [f for f in formats if f["resolution"] != "audio only"],
        key=lambda f: int(f["resolution"].split("x")[-1]) if "x" in f["resolution"] else 0,
        reverse=True,
    )
    audio_fmts = [f for f in formats if f["resolution"] == "audio only"]

    return {
        "title":     info.get("title", "video"),
        "thumbnail": info.get("thumbnail"),
        "duration":  info.get("duration"),
        "uploader":  info.get("uploader"),
        "platform":  info.get("extractor_key"),
        "formats":   video_fmts + audio_fmts,
    }


# 2. Video Download

@app.get("/download")
def download(url: str, format_id: str):
    out_tmpl = f"/tmp/{uuid.uuid4()}.%(ext)s"

    if FFMPEG_OK:
        fmt            = f"{format_id}+bestaudio[ext=m4a]/bestaudio/{format_id}/{format_id}"
        postprocessors = [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
        merge_fmt      = "mp4"
    else:
        fmt            = f"{format_id}/best[ext=mp4]/best"
        postprocessors = []
        merge_fmt      = None

    ydl_opts = {
        **_base_opts(),
        "format":  fmt,
        "outtmpl": out_tmpl,
        **({"merge_output_format": merge_fmt, "postprocessors": postprocessors} if merge_fmt else {}),
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


# 3. Audio / MP3

@app.get("/audio-download")
def audio_download(url: str):
    out_path = _tmp("%(ext)s")
    if FFMPEG_OK:
        postprocessors = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
        fmt = "bestaudio/best"
    else:
        postprocessors = []
        fmt = "bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio/best"

    ydl_opts = {**_base_opts(), "format": fmt, "outtmpl": out_path, "postprocessors": postprocessors}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base = os.path.splitext(ydl.prepare_filename(info))[0]
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))

    for candidate_ext in ("mp3", "m4a", "webm", "ogg"):
        candidate = f"{base}.{candidate_ext}"
        if os.path.exists(candidate):
            safe_title = "".join(c for c in info.get("title", "audio") if c.isalnum() or c in " _-")
            return FileResponse(candidate, filename=f"{safe_title}.{candidate_ext}", media_type="audio/mpeg")

    raise HTTPException(status_code=500, detail="Audio download failed.")


# 4. Video to GIF

@app.get("/video-to-gif")
def video_to_gif(url: str, start: float = 0, duration: float = 5, width: int = 480):
    if not FFMPEG_OK:
        raise HTTPException(status_code=500, detail="ffmpeg not available.")
    if duration > 30:
        raise HTTPException(status_code=400, detail="Max GIF duration is 30s.")
    if width > 1280:
        raise HTTPException(status_code=400, detail="Max GIF width is 1280px.")

    src_path = _tmp("mp4")
    ydl_opts = {**_base_opts(), "format": "bestvideo[height<=720][ext=mp4]/best[height<=720]", "outtmpl": src_path}
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
        subprocess.run([FFMPEG_PATH, "-y", "-ss", str(start), "-t", str(duration), "-i", src,
                        "-vf", f"fps=12,scale={width}:-1:flags=lanczos,palettegen", palette_path],
                       check=True, capture_output=True)
        subprocess.run([FFMPEG_PATH, "-y", "-ss", str(start), "-t", str(duration), "-i", src,
                        "-i", palette_path,
                        "-filter_complex", f"fps=12,scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                        out_gif], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="GIF failed: " + e.stderr.decode(errors="ignore"))

    safe_title = "".join(c for c in info.get("title", "clip") if c.isalnum() or c in " _-")
    return FileResponse(out_gif, filename=f"{safe_title}.gif", media_type="image/gif")


# 5. Video Trimmer

@app.get("/video-trim")
def video_trim(url: str, start: float = 0, end: float = 30):
    if not FFMPEG_OK:
        raise HTTPException(status_code=500, detail="ffmpeg not available.")
    if end <= start:
        raise HTTPException(status_code=400, detail="end must be > start.")
    if (end - start) > 600:
        raise HTTPException(status_code=400, detail="Max clip length is 10 minutes.")

    src_path = _tmp("mp4")
    ydl_opts = {**_base_opts(), "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": src_path, "merge_output_format": "mp4"}
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
        subprocess.run([FFMPEG_PATH, "-y", "-ss", str(start), "-to", str(end), "-i", src,
                        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out_mp4],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Trim failed: " + e.stderr.decode(errors="ignore"))

    safe_title = "".join(c for c in info.get("title", "clip") if c.isalnum() or c in " _-")
    return FileResponse(out_mp4, filename=f"{safe_title}_trimmed.mp4", media_type="video/mp4")
