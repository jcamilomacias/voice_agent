import asyncio
import sounddevice as sd
from src.frames import AudioRawFrame
from src.config import Settings


def start_audio_input(queue: asyncio.Queue, loop: asyncio.AbstractEventLoop, settings: Settings) -> sd.InputStream:
    """Open a sounddevice InputStream and bridge each callback chunk into the asyncio queue."""
    def callback(indata, frames, time, status):
        audio_bytes = bytes(indata)
        frame = AudioRawFrame(audio=audio_bytes, sample_rate=settings.sample_rate, num_channels=1)
        loop.call_soon_threadsafe(queue.put_nowait, frame)

    stream = sd.InputStream(
        samplerate=settings.sample_rate,
        blocksize=settings.chunk_size,
        channels=1,
        dtype="int16",
        callback=callback,
    )
    stream.start()
    return stream
