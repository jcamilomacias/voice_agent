# 11 — Integration test suite

## What to build

Write integration tests that hit real APIs and assert on end-to-end behavior including latency. Tests are tagged `@pytest.mark.integration`, excluded from `make test`, and run via `make test-integration`. Real API keys must be present in `.env`.

Covers: Deepgram streaming transcription round-trip, Groq completion with streaming, Cartesia synthesis producing valid audio bytes, end-to-end latency assertions using `LatencyTracker` (STT < 500ms, LLM TTFT < 400ms, TTS TTFA < 300ms, end-to-end < 1500ms).

## Acceptance criteria

- [ ] `make test` does NOT run integration tests
- [ ] `make test-integration` runs integration tests (requires real API keys in `.env`)
- [ ] Deepgram test: audio bytes in → `TranscriptionFrame` with non-empty text out
- [ ] Groq test: transcript in → at least one `LLMResponseFrame` with `is_final: False` before final
- [ ] Cartesia test: sentence text in → `TTSAudioFrame` bytes are valid PCM audio
- [ ] Latency assertions use `LatencyTracker` and fail with a clear message if thresholds are exceeded
- [ ] CI configuration documents that integration tests require secrets

## Blocked by

- #09 — Latency tracking — LatencyTracker integration
- #10 — Unit test suite
