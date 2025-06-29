
from fastapi import FastAPI, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from backend.downloader import download_video
from backend.cleanup import schedule_cleanup
import os

APP_DIR      = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR     = os.path.dirname(APP_DIR)
FRONT_DIR    = os.path.join(ROOT_DIR, "frontend")
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = FastAPI(title="SnapDown – Video Downloader")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory=FRONT_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    with open(os.path.join(FRONT_DIR, "index.html"), encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/download")
async def download(background_tasks: BackgroundTasks,
                   url: str = Form(...)) -> FileResponse:
    try:
        filepath = await download_video(url, DOWNLOAD_DIR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    background_tasks.add_task(schedule_cleanup, filepath, after_minutes=10)

    filename = os.path.basename(filepath)
    return FileResponse(path=filepath,
                        media_type="application/octet-stream",
                        filename=filename)
