import asyncio
import sounddevice as sd
from src.frames import AudioRawFrame, EndFrame
from src.config import Settings


async def run_audio_output(queue: asyncio.Queue, settings: Settings) -> None:
    """Read AudioRawFrames from the queue and play them through the speaker."""
    with sd.RawOutputStream(
        samplerate=settings.sample_rate,
        channels=1,
        dtype="int16",
    ) as stream:
        while True:
            frame = await queue.get()
            if isinstance(frame, EndFrame):
                break
            if isinstance(frame, AudioRawFrame):
                stream.write(frame.audio)
