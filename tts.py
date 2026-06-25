import asyncio
import io
import functools
import edge_tts

VOICE = "hi-IN-SwaraNeural"  # Natural Hindi female voice

async def _synthesize(text: str) -> bytes:
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate="+0%", pitch="+0Hz")
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    buf.seek(0)
    return buf.read()

@functools.lru_cache(maxsize=64)
def _cached_speak(text: str) -> bytes:
    return asyncio.run(_synthesize(text))

def speak(text: str) -> bytes:
    return _cached_speak(text.strip())