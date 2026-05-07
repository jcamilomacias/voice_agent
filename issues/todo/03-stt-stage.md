# 03 — STT stage — live transcription

## What to build

Add a Speech-to-Text stage that consumes `AudioRawFrame`s (gated by VAD state) and emits `TranscriptionFrame`s. Default implementation uses Deepgram streaming, which sends partial transcripts (`is_final: False`) as you speak and a final transcript (`is_final: True`) on silence detection. The `STTProvider` Protocol is defined so Deepgram can be swapped for faster-whisper via a single config change.

Includes: `frames.py` additions (`TranscriptionFrame` with `text: str`, `is_final: bool`), `processors/stt/base.py` (`STTProvider` Protocol), `processors/stt/deepgram.py` (Deepgram streaming implementation), pipeline updated to include STT stage, `DEEPGRAM_API_KEY` added to `.env.example`.

## Acceptance criteria

- [ ] Speaking into the microphone produces a printed transcript within ~500ms of stopping speech
- [ ] Partial transcripts (`is_final: False`) are emitted while speaking
- [ ] Final transcript (`is_final: True`) is emitted after VAD detects silence
- [ ] `STTProvider` Protocol is defined in `base.py` with a clear interface
- [ ] Swapping the STT implementation requires only changing the injected provider object
- [ ] `DEEPGRAM_API_KEY` is loaded from `.env` via `config.py`
- [ ] `EndFrame` and `CancelFrame` propagate cleanly through the STT stage

## Blocked by

- #02 — VAD stage — detect speaking state
