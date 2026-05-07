# 05 — TTS stage — full end-to-end voice loop

## What to build

Add a Text-to-Speech stage that synthesizes sentence-chunked `LLMResponseFrame`s into `TTSAudioFrame`s, played back through the speaker. This completes the full voice conversation loop: microphone → VAD → STT → LLM → TTS → speaker. Default TTS provider is Cartesia (streaming, ~150ms first chunk). TTS synthesis begins as soon as the first sentence is available — before the LLM finishes generating — using the `is_final: False` frames from the sentence aggregator.

Includes: `frames.py` additions (`TTSAudioFrame` with `audio: bytes`), `processors/tts/base.py` (`TTSProvider` Protocol), `processors/tts/cartesia.py` (Cartesia streaming implementation), pipeline fully wired end-to-end, `CARTESIA_API_KEY` added to `.env.example`.

## Acceptance criteria

- [ ] Speaking to the agent produces a spoken voice response — full loop is working
- [ ] TTS synthesis begins on the first complete sentence, before LLM finishes
- [ ] `TTSAudioFrame` chunks are played back in order without gaps or distortion
- [ ] `TTSProvider` Protocol is defined in `base.py` with a clear interface
- [ ] Swapping the TTS implementation requires only changing the injected provider object
- [ ] `CARTESIA_API_KEY` is loaded from `.env` via `config.py`
- [ ] End-to-end perceived latency from stop-speaking to first audio is under 1.5 seconds
- [ ] `make run` starts a full working voice session

## Tests to write (tests/test_tts_processor.py)

Define `MockTTSProvider` implementing `TTSProvider`. It takes a list of audio byte chunks and returns them as an async generator when `synthesize()` is called, without touching any network.

- [ ] `MockTTSProvider` satisfies the `TTSProvider` Protocol
- [ ] Test: `LLMResponseFrame(is_final=False)` with sentence text → `TTSAudioFrame` chunks emitted in order
- [ ] Test: synthesis starts on first sentence before final `LLMResponseFrame` arrives (early synthesis)
- [ ] Test: `CancelFrame` → in-flight synthesis stops, no further `TTSAudioFrame`s emitted, frame propagates
- [ ] Test: `EndFrame` propagates through the TTS processor
- [ ] `make test` passes with no `CARTESIA_API_KEY`, no speaker, and no network

## Blocked by

- #04 — LLM stage — streaming response + conversation context
