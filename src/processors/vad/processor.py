import asyncio
from src.frames import AudioRawFrame, EndFrame, UserStartedSpeakingFrame, UserStoppedSpeakingFrame
from src.processors.vad.base import VADProvider


class VADProcessor:
    def __init__(self, provider: VADProvider, input_q: asyncio.Queue, output_q: asyncio.Queue):
        self._provider = provider
        self._input_q = input_q
        self._output_q = output_q
        self._speaking = False

    async def run(self) -> None:
        while True:
            frame = await self._input_q.get()
            if isinstance(frame, AudioRawFrame):
                is_speech = self._provider.is_speech(frame.audio, frame.sample_rate)
                if is_speech and not self._speaking:
                    self._speaking = True
                    await self._output_q.put(UserStartedSpeakingFrame())
                elif not is_speech and self._speaking:
                    self._speaking = False
                    await self._output_q.put(UserStoppedSpeakingFrame())
                await self._output_q.put(frame)
            elif isinstance(frame, EndFrame):
                await self._output_q.put(frame)
                return
            else:
                await self._output_q.put(frame)
