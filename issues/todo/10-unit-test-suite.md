# 10 — Unit test suite

## What to build

Write a comprehensive unit test suite covering all deep modules. Tests inject frames directly into real `asyncio.Queue` instances using mock providers — no real hardware, no API calls, no network. Each test verifies observable external behavior: what frames come out given specific frames as input.

Covers: `frames.py` (instantiation, field defaults), `conversation.py` (sliding window, turn accumulation, system prompt), `utils/sentence_aggregator.py` (boundary detection, partial accumulation, CancelFrame flush), `processors/vad/` (correct speaking state frame emission), `processors/stt/` (TranscriptionFrame emission, partial vs final), `processors/llm/` (LLMResponseFrame streaming, ConversationContext updates, CancelFrame passthrough), `processors/tts/` (TTSAudioFrame chunks, CancelFrame buffer flush), `pipeline.py` (end-to-end frame flow with all-mock providers, CancelFrame propagation across full pipeline).

## Acceptance criteria

- [ ] `make test` runs all unit tests with no API keys required
- [ ] All processor tests use mock providers that implement the relevant Protocol
- [ ] `ConversationContext` sliding window is tested at boundary (exactly `max_turns`, over limit)
- [ ] `SentenceAggregator` tested for: single sentence, multi-sentence, partial (no boundary yet), flush on CancelFrame
- [ ] Full pipeline `CancelFrame` propagation test: frames in-flight are discarded, pipeline resets
- [ ] No test imports sounddevice, makes network calls, or touches the filesystem
- [ ] Tests are in `tests/` and separated from integration tests by marker

## Blocked by

- #06 — Interruption handling via CancelFrame
- #07 — Error handling via ErrorFrame
