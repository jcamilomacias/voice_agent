"""Entry point for `make run` — mic → speaker echo loop."""
import asyncio
import signal
from src.config import Settings
from src.frames import EndFrame
from src.audio_input import start_audio_input
from src.audio_output import run_audio_output
from src.pipeline import run_echo_pipeline


async def main() -> None:
    settings = Settings()
    loop = asyncio.get_running_loop()

    input_q: asyncio.Queue = asyncio.Queue()
    output_q: asyncio.Queue = asyncio.Queue()

    stream = start_audio_input(input_q, loop, settings)

    pipeline_task = asyncio.create_task(run_echo_pipeline(input_q, output_q))
    output_task = asyncio.create_task(run_audio_output(output_q, settings))

    def shutdown(*_):
        input_q.put_nowait(EndFrame())

    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    print("Echo loop running — speak into the microphone. Ctrl-C to stop.")
    await asyncio.gather(pipeline_task, output_task)
    stream.stop()
    stream.close()


if __name__ == "__main__":
    asyncio.run(main())
