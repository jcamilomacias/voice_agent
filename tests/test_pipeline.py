import asyncio
import pytest
from src.frames import AudioRawFrame, EndFrame
from src.pipeline import run_echo_pipeline


@pytest.mark.asyncio
async def test_echo_pipeline_passes_frames_in_order():
    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    frames = [
        AudioRawFrame(audio=bytes([i]), sample_rate=16000, num_channels=1)
        for i in range(3)
    ]
    for f in frames:
        await input_q.put(f)
    await input_q.put(EndFrame())

    await asyncio.wait_for(run_echo_pipeline(input_q, output_q), timeout=2.0)

    received = []
    while not output_q.empty():
        received.append(output_q.get_nowait())

    assert len(received) == 4  # 3 audio frames + EndFrame
    for i, frame in enumerate(received[:3]):
        assert isinstance(frame, AudioRawFrame)
        assert frame.audio == bytes([i])
    assert isinstance(received[3], EndFrame)


@pytest.mark.asyncio
async def test_echo_pipeline_exits_cleanly_on_end_frame():
    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(EndFrame())

    # Must complete without hanging
    await asyncio.wait_for(run_echo_pipeline(input_q, output_q), timeout=1.0)

    result = output_q.get_nowait()
    assert isinstance(result, EndFrame)
