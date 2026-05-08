import asyncio
from src.frames import EndFrame


async def run_echo_pipeline(input_q: asyncio.Queue, output_q: asyncio.Queue) -> None:
    """Pass every frame from input_q to output_q; stop after EndFrame."""
    while True:
        frame = await input_q.get()
        await output_q.put(frame)
        if isinstance(frame, EndFrame):
            break
