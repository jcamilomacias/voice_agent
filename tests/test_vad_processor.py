import asyncio
import pytest
from src.frames import AudioRawFrame, EndFrame, UserStartedSpeakingFrame, UserStoppedSpeakingFrame
from src.processors.vad.base import VADProvider


class MockVADProvider:
    def __init__(self, responses: list[bool]):
        self._responses = iter(responses)

    def is_speech(self, audio: bytes, sample_rate: int) -> bool:
        return next(self._responses)


def make_audio_frame() -> AudioRawFrame:
    return AudioRawFrame(audio=b"\x00" * 32, sample_rate=16000, num_channels=1)


def test_mock_vad_provider_satisfies_protocol():
    provider = MockVADProvider([True, False])
    assert isinstance(provider, VADProvider)


@pytest.mark.asyncio
async def test_silence_frames_emit_no_speaking_state_frames():
    from src.processors.vad.processor import VADProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    for _ in range(3):
        await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockVADProvider([False, False, False])
    await asyncio.wait_for(VADProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    speaking_frames = [f for f in frames if isinstance(f, (UserStartedSpeakingFrame, UserStoppedSpeakingFrame))]
    assert speaking_frames == []


@pytest.mark.asyncio
async def test_silence_to_speech_emits_exactly_one_started_frame():
    from src.processors.vad.processor import VADProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    # silence, then speech, then continued speech
    for _ in range(3):
        await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockVADProvider([False, True, True])
    await asyncio.wait_for(VADProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    started = [f for f in frames if isinstance(f, UserStartedSpeakingFrame)]
    stopped = [f for f in frames if isinstance(f, UserStoppedSpeakingFrame)]
    assert len(started) == 1
    assert len(stopped) == 0


@pytest.mark.asyncio
async def test_speech_to_silence_emits_exactly_one_stopped_frame():
    from src.processors.vad.processor import VADProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    # speech then silence
    for _ in range(3):
        await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockVADProvider([True, False, False])
    await asyncio.wait_for(VADProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    started = [f for f in frames if isinstance(f, UserStartedSpeakingFrame)]
    stopped = [f for f in frames if isinstance(f, UserStoppedSpeakingFrame)]
    assert len(started) == 1  # first frame triggers speech start
    assert len(stopped) == 1  # second frame triggers speech stop


@pytest.mark.asyncio
async def test_audio_frames_pass_through_regardless_of_vad_state():
    from src.processors.vad.processor import VADProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    audio_frames = [make_audio_frame() for _ in range(4)]
    for f in audio_frames:
        await input_q.put(f)
    await input_q.put(EndFrame())

    # alternating speech/silence
    provider = MockVADProvider([False, True, True, False])
    await asyncio.wait_for(VADProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    audio_out = [f for f in frames if isinstance(f, AudioRawFrame)]
    assert len(audio_out) == 4
    assert audio_out == audio_frames


@pytest.mark.asyncio
async def test_end_frame_propagates_and_processor_exits():
    from src.processors.vad.processor import VADProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockVADProvider([False])
    # must complete without hanging
    await asyncio.wait_for(VADProcessor(provider, input_q, output_q).run(), timeout=1.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    end_frames = [f for f in frames if isinstance(f, EndFrame)]
    assert len(end_frames) == 1
    assert isinstance(frames[-1], EndFrame)
