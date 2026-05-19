try:
    from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
except ImportError as exc:
    raise ImportError(
        "deepgram-sdk is required for DeepgramSTTProvider. "
        "Install it with: pip install 'voice-agent[stt]'"
    ) from exc

from typing import AsyncIterator


class DeepgramSTTProvider:
    def __init__(self, api_key: str, model: str = "nova-2", language: str = "en"):
        self._client = DeepgramClient(api_key)
        self._model = model
        self._language = language

    async def transcribe(self, audio: bytes, sample_rate: int) -> AsyncIterator[tuple[str, bool]]:
        # Placeholder — full streaming implementation wires up Deepgram LiveClient
        raise NotImplementedError("DeepgramSTTProvider.transcribe() not yet wired up")
        yield  # makes this an async generator
