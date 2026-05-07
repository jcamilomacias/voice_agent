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

## Blocked by

- #04 — LLM stage — streaming response + conversation context
