# 06 — Interruption handling via CancelFrame

## What to build

Add interruption support so that when the user starts speaking while the agent is playing TTS audio, the pipeline immediately stops playback, flushes all in-flight frames, and returns to the listening state. Implemented via `CancelFrame` — a system frame that propagates through all processors, each of which clears its internal buffer on receipt.

Includes: `frames.py` additions (`CancelFrame`), `CancelFrame` handling in all processors (VAD, STT, LLM, TTS, audio output), `UserStartedSpeakingFrame` during TTS playback triggers `CancelFrame` emission, `SentenceAggregator` flush on `CancelFrame`.

## Acceptance criteria

- [ ] Speaking while the agent is talking immediately stops audio playback
- [ ] All queued `LLMResponseFrame`s and `TTSAudioFrame`s are discarded on `CancelFrame`
- [ ] `SentenceAggregator` buffer is flushed without emitting on `CancelFrame`
- [ ] Pipeline returns to clean listening state after interruption
- [ ] `CancelFrame` propagates through every processor in order
- [ ] A new utterance after interruption produces a correct, complete response

## Tests to write (tests/test_cancel_propagation.py)

This is the most important test in the project. Use all the mock providers from Issues 02-05 together to run a full pipeline and inject a `CancelFrame` mid-flight.

- [ ] Test: `CancelFrame` injected while `LLMResponseFrame`s are queued → all subsequent `LLMResponseFrame`s discarded
- [ ] Test: `CancelFrame` injected while `TTSAudioFrame`s are queued → all subsequent `TTSAudioFrame`s discarded
- [ ] Test: `SentenceAggregator` buffer is empty after `CancelFrame` (no partial sentence leaked)
- [ ] Test: pipeline accepts new `TranscriptionFrame` input after interruption and produces a correct response
- [ ] Test: `CancelFrame` reaches the audio output stage (no frames stuck in queues)
- [ ] `make test` passes with all-mock providers, no hardware, no API keys

## Blocked by

- #05 — TTS stage — full end-to-end voice loop
