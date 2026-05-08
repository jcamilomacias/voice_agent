# 07 — Error handling via ErrorFrame

## What to build

Add graceful error handling so that provider failures (dropped Deepgram connection, Cartesia timeout, Groq API error) emit an `ErrorFrame` rather than crashing the pipeline. `pipeline.py` handles `ErrorFrame` centrally: logs all errors, sends `EndFrame` for fatal ones to shut down cleanly.

Includes: `frames.py` additions (`ErrorFrame` with `error: Exception`, `processor: str`, `fatal: bool`), try/except wrapping in all provider calls across STT, LLM, and TTS processors, central `ErrorFrame` handler in `pipeline.py`.

## Acceptance criteria

- [ ] A simulated Deepgram failure emits `ErrorFrame` and logs the error without crashing
- [ ] A simulated Groq failure emits `ErrorFrame` and logs the error without crashing
- [ ] A simulated Cartesia failure emits `ErrorFrame` and logs the error without crashing
- [ ] `ErrorFrame` with `fatal: True` causes `pipeline.py` to emit `EndFrame` and shut down
- [ ] `ErrorFrame` with `fatal: False` is logged and the pipeline continues listening
- [ ] `ErrorFrame.processor` identifies which stage produced the error

## Tests to write (tests/test_error_handling.py)

Define `FailingSTTProvider`, `FailingLLMProvider`, `FailingTTSProvider` — mock providers whose methods raise an exception. Use them to test error behavior without touching real APIs.

- [ ] Test: `FailingSTTProvider` raises → `ErrorFrame(processor="stt", fatal=False)` emitted, no crash
- [ ] Test: `FailingLLMProvider` raises → `ErrorFrame(processor="llm", fatal=False)` emitted, no crash
- [ ] Test: `FailingTTSProvider` raises → `ErrorFrame(processor="tts", fatal=False)` emitted, no crash
- [ ] Test: `ErrorFrame(fatal=True)` received by `pipeline.py` → `EndFrame` emitted and pipeline exits
- [ ] Test: `ErrorFrame(fatal=False)` received by `pipeline.py` → logged, pipeline continues (next input processed)
- [ ] Test: `ErrorFrame.processor` field correctly identifies the failing stage
- [ ] `make test` passes with no API keys and no network

## Blocked by

- #05 — TTS stage — full end-to-end voice loop
