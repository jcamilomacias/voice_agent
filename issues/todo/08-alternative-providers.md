# 08 — Alternative providers — faster-whisper + Piper

## What to build

Add local fallback implementations for STT (faster-whisper) and TTS (Piper), enabling fully offline operation. Provider selection is driven by `config.py` so switching requires no code changes. This validates that the `STTProvider` and `TTSProvider` Protocol abstractions work correctly with a second, structurally different implementation.

Includes: `processors/stt/faster_whisper.py` (faster-whisper implementation of `STTProvider`), `processors/tts/piper.py` (Piper implementation of `TTSProvider`), `config.py` additions for provider selection (`stt_provider`, `tts_provider`).

## Acceptance criteria

- [ ] Setting `STT_PROVIDER=faster_whisper` in `.env` switches to local transcription with no code changes
- [ ] Setting `TTS_PROVIDER=piper` in `.env` switches to local synthesis with no code changes
- [ ] Full voice loop works end-to-end with faster-whisper + Piper (no internet required)
- [ ] Both implementations correctly handle `CancelFrame` and `EndFrame`
- [ ] `.env.example` documents the `STT_PROVIDER` and `TTS_PROVIDER` options

## Blocked by

- #05 — TTS stage — full end-to-end voice loop
