# 09 — Latency tracking — LatencyTracker integration

## What to build

Add per-stage latency measurement using `LatencyTracker`, integrated into the pipeline so that STT latency, LLM time-to-first-token, TTS time-to-first-audio, and end-to-end latency are printed to stdout after each conversation turn.

Includes: `utils/timing.py` (`LatencyTracker` with `record(stage, timestamp)` and per-turn summary), timestamps added to relevant frames or recorded inline in processors, stdout display of latency report after each assistant turn.

## Acceptance criteria

- [ ] After each turn, stdout shows: STT latency, LLM time-to-first-token, TTS time-to-first-audio, end-to-end latency
- [ ] All timestamps use `time.perf_counter()` for precision
- [ ] `LatencyTracker` is reset at the start of each new user utterance
- [ ] Latency display does not block or delay audio playback
- [ ] `LatencyTracker` is a standalone utility with no queue dependencies

## Tests to write (tests/test_timing.py)

`LatencyTracker` is a pure utility — it has no I/O, no queues, no providers. Test it immediately after writing it.

- [ ] `record(stage, t)` stores a timestamp for the given stage
- [ ] `summary()` returns correct per-stage deltas (STT latency, LLM TTFT, TTS TTFA, end-to-end)
- [ ] `reset()` clears all stored timestamps
- [ ] `summary()` on an empty tracker returns `{}` or a zero-filled structure without raising
- [ ] Tracker is reset when a new `UserStartedSpeakingFrame` is received by the processor that uses it
- [ ] `make test` passes with no hardware, no API keys, no network

## Blocked by

- #05 — TTS stage — full end-to-end voice loop
