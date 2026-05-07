# 01 — Project scaffold + silent echo loop

## What to build

Bootstrap the full project structure and wire a minimal mic→speaker echo pipeline end-to-end. No processing — raw audio captured from the microphone is immediately played back through the speaker. This proves audio I/O works, the asyncio/sounddevice bridge is correct, and the queue-based pipeline skeleton runs without errors.

Includes: `pyproject.toml` (uv), `Makefile` (`make install`, `make test`, `make run`), `.env.example`, `frames.py` (AudioRawFrame, StartFrame, EndFrame only), `config.py` (pydantic BaseSettings with audio settings), `audio_input.py` (sounddevice → asyncio queue bridge at 16000 Hz / 512 samples), `audio_output.py` (queue → speaker), `pipeline.py` (queue wiring + task launcher).

## Acceptance criteria

- [ ] `make install` sets up the environment via `uv` with no errors
- [ ] `make run` starts the pipeline and echoes microphone audio through the speaker in real time
- [ ] `AudioRawFrame` carries `audio: bytes`, `sample_rate: int`, `num_channels: int`
- [ ] Audio is captured at 16000 Hz, 512-sample chunks
- [ ] sounddevice callback bridges to asyncio via `loop.call_soon_threadsafe`
- [ ] `EndFrame` propagates through all stages and shuts the pipeline down cleanly
- [ ] All settings (sample rate, chunk size) are loaded from `config.py` / `.env`
- [ ] `.env.example` documents all required environment variables

## Blocked by

None — can start immediately.
