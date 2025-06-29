
import yt_dlp, asyncio, functools, os

async def download_video(url: str, out_dir: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None,
        functools.partial(_sync_download, url, out_dir))

def _sync_download(url: str, out_dir: str) -> str:
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
