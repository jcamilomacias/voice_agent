# 08 — Alternative providers — faster-whisper + Piper

## What to build

Add local fallback implementations for STT (faster-whisper) and TTS (Piper), enabling fully offline operation. Provider selection is driven by `config.py` so switching requires no code changes. Update `pipeline.py` to instantiate the correct provider based on config — this is the step that proves the Protocol abstraction works end-to-end, not just in theory.

Includes: `processors/stt/faster_whisper.py` (faster-whisper implementation of `STTProvider`), `processors/tts/piper.py` (Piper implementation of `TTSProvider`), `config.py` additions (`stt_provider: str`, `tts_provider: str` fields), `pipeline.py` update (instantiate correct provider from `config.stt_provider` / `config.tts_provider`).

## Acceptance criteria

- [ ] Setting `STT_PROVIDER=faster_whisper` in `.env` switches to local transcription with no code changes
- [ ] Setting `TTS_PROVIDER=piper` in `.env` switches to local synthesis with no code changes
- [ ] Full voice loop works end-to-end with faster-whisper + Piper (no internet required)
- [ ] Both implementations correctly handle `CancelFrame` and `EndFrame`
- [ ] `.env.example` documents the `STT_PROVIDER` and `TTS_PROVIDER` options

## Tests to write (tests/test_alternative_providers.py)

- [ ] Test: `FasterWhisperSTT` satisfies the `STTProvider` Protocol (structural type check)
- [ ] Test: `PiperTTS` satisfies the `TTSProvider` Protocol (structural type check)
- [ ] Test: `config.stt_provider = "faster_whisper"` → `pipeline.py` instantiates `FasterWhisperSTT` (not `DeepgramSTT`)
- [ ] Test: `config.tts_provider = "piper"` → `pipeline.py` instantiates `PiperTTS` (not `CartesiaTTS`)
- [ ] Test: `FasterWhisperSTT` handles `CancelFrame` without error
- [ ] Test: `PiperTTS` handles `CancelFrame` without error
- [ ] `make test` passes with no API keys (providers can be instantiated without models for structural tests)

## Blocked by

- #05 — TTS stage — full end-to-end voice loop
