
import asyncio, os, time

async def schedule_cleanup(path: str, after_minutes: int = 10) -> None:
    await asyncio.sleep(after_minutes * 60)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
