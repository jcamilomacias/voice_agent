from typing import AsyncIterator, Protocol, runtime_checkable


@runtime_checkable
class STTProvider(Protocol):
    def transcribe(self, audio: bytes, sample_rate: int) -> AsyncIterator[tuple[str, bool]]: ...
