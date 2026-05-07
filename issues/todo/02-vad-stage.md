# 02 — VAD stage — detect speaking state

## What to build

Add a Voice Activity Detection stage between audio input and the rest of the pipeline. The VAD processor reads `AudioRawFrame`s and emits `UserStartedSpeakingFrame` and `UserStoppedSpeakingFrame` at the correct boundaries. Default implementation uses silero-vad. The `VADProvider` Protocol is defined so alternative implementations can be swapped in via a single config change.

Includes: `frames.py` additions (`UserStartedSpeakingFrame`, `UserStoppedSpeakingFrame`), `processors/vad/base.py` (`VADProvider` Protocol), `processors/vad/silero.py` (silero-vad implementation), pipeline updated to include VAD stage.

## Acceptance criteria

- [ ] Speaking and silence transitions are logged to stdout during a live session
- [ ] `UserStartedSpeakingFrame` is emitted within ~32ms of speech onset
- [ ] `UserStoppedSpeakingFrame` is emitted reliably after a short silence
- [ ] `VADProvider` Protocol is defined in `base.py` with a clear interface
- [ ] Swapping the VAD implementation requires only changing the injected provider object
- [ ] `AudioRawFrame`s are forwarded downstream unchanged (VAD is non-destructive)
- [ ] `EndFrame` still propagates cleanly through the VAD stage

## Blocked by

- #01 — Project scaffold + silent echo loop
