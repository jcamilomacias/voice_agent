import asyncio
import pytest
from src.frames import (
    AudioRawFrame,
    CancelFrame,
    EndFrame,
    TranscriptionFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
)
from src.processors.stt.base import STTProvider


class MockSTTProvider:
    def __init__(self, responses: list[tuple[str, bool]]):
        self._responses = responses

    async def transcribe(self, audio: bytes, sample_rate: int):
        for item in self._responses:
            yield item


def make_audio_frame() -> AudioRawFrame:
    return AudioRawFrame(audio=b"\x00" * 32, sample_rate=16000, num_channels=1)


# ── Cycle 1: Protocol ────────────────────────────────────────────────────────

def test_mock_stt_provider_satisfies_protocol():
    provider = MockSTTProvider([("hello", False)])
    assert isinstance(provider, STTProvider)


# ── Cycle 2: partials during speech ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_audio_during_speech_emits_partial_transcriptions():
    from src.processors.stt.processor import STTProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(UserStartedSpeakingFrame())
    await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockSTTProvider([("hello", False)])
    await asyncio.wait_for(STTProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    partials = [f for f in frames if isinstance(f, TranscriptionFrame) and not f.is_final]
    assert len(partials) == 1
    assert partials[0].text == "hello"


# ── Cycle 3: final on UserStoppedSpeakingFrame ───────────────────────────────

@pytest.mark.asyncio
async def test_user_stopped_speaking_emits_final_transcription():
    from src.processors.stt.processor import STTProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(UserStartedSpeakingFrame())
    await input_q.put(make_audio_frame())
    await input_q.put(UserStoppedSpeakingFrame())
    await input_q.put(EndFrame())

    provider = MockSTTProvider([("hello world", False)])
    await asyncio.wait_for(STTProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    finals = [f for f in frames if isinstance(f, TranscriptionFrame) and f.is_final]
    assert len(finals) == 1
    assert finals[0].text == "hello world"


# ── Cycle 4: silence → no transcription ─────────────────────────────────────

@pytest.mark.asyncio
async def test_audio_during_silence_emits_no_transcription():
    from src.processors.stt.processor import STTProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(make_audio_frame())
    await input_q.put(make_audio_frame())
    await input_q.put(EndFrame())

    provider = MockSTTProvider([("hello", False)])
    await asyncio.wait_for(STTProcessor(provider, input_q, output_q).run(), timeout=2.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    transcriptions = [f for f in frames if isinstance(f, TranscriptionFrame)]
    assert transcriptions == []


# ── Cycle 5: EndFrame propagates ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_end_frame_propagates():
    from src.processors.stt.processor import STTProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    await input_q.put(EndFrame())

    provider = MockSTTProvider([])
    await asyncio.wait_for(STTProcessor(provider, input_q, output_q).run(), timeout=1.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    assert len(frames) == 1
    assert isinstance(frames[0], EndFrame)


# ── Cycle 6: CancelFrame propagates without transcript ───────────────────────

@pytest.mark.asyncio
async def test_cancel_frame_propagates_without_transcript():
    from src.processors.stt.processor import STTProcessor

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    # Speaking state set but CancelFrame arrives before any audio
    await input_q.put(UserStartedSpeakingFrame())
    await input_q.put(CancelFrame())

    provider = MockSTTProvider([("hello", False)])
    await asyncio.wait_for(STTProcessor(provider, input_q, output_q).run(), timeout=1.0)

    frames = []
    while not output_q.empty():
        frames.append(output_q.get_nowait())

    transcriptions = [f for f in frames if isinstance(f, TranscriptionFrame)]
    cancel_frames = [f for f in frames if isinstance(f, CancelFrame)]
    assert transcriptions == []
    assert len(cancel_frames) == 1
