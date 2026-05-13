from typing import Protocol, runtime_checkable


@runtime_checkable
class VADProvider(Protocol):
    def is_speech(self, audio: bytes, sample_rate: int) -> bool: ...
