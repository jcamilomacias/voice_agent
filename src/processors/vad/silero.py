try:
    import torch
    from silero_vad import load_silero_vad  # type: ignore[import]

    class SileroVADProvider:
        def __init__(self, sample_rate: int = 16000, threshold: float = 0.5):
            self._model = load_silero_vad()
            self._sample_rate = sample_rate
            self._threshold = threshold

        def is_speech(self, audio: bytes, sample_rate: int) -> bool:
            audio_tensor = torch.frombuffer(audio, dtype=torch.int16).float() / 32768.0
            confidence = self._model(audio_tensor, sample_rate).item()
            return confidence >= self._threshold

except ImportError:
    class SileroVADProvider:  # type: ignore[no-redef]
        def __init__(self, **kwargs):
            raise ImportError(
                "silero-vad and torch are required. Install with: uv add silero-vad torch"
            )

        def is_speech(self, audio: bytes, sample_rate: int) -> bool:
            raise ImportError(
                "silero-vad and torch are required. Install with: uv add silero-vad torch"
            )
