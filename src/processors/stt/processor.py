import asyncio
from src.frames import (
    AudioRawFrame,
    CancelFrame,
    EndFrame,
    TranscriptionFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
)
from src.processors.stt.base import STTProvider


class STTProcessor:
    def __init__(self, provider: STTProvider, input_q: asyncio.Queue, output_q: asyncio.Queue):
        self._provider = provider
        self._input_q = input_q
        self._output_q = output_q
        self._speaking = False
        self._last_text = ""

    async def run(self) -> None:
        while True:
            frame = await self._input_q.get()
            if isinstance(frame, UserStartedSpeakingFrame):
                self._speaking = True
                self._last_text = ""
                await self._output_q.put(frame)
            elif isinstance(frame, UserStoppedSpeakingFrame):
                if self._speaking:
                    await self._output_q.put(TranscriptionFrame(text=self._last_text, is_final=True))
                self._speaking = False
                await self._output_q.put(frame)
            elif isinstance(frame, AudioRawFrame):
                if self._speaking:
                    async for text, is_final in self._provider.transcribe(frame.audio, frame.sample_rate):
                        self._last_text = text
                        if not is_final:
                            await self._output_q.put(TranscriptionFrame(text=text, is_final=False))
                await self._output_q.put(frame)
            elif isinstance(frame, (EndFrame, CancelFrame)):
                await self._output_q.put(frame)
                return
            else:
                await self._output_q.put(frame)
