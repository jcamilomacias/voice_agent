# 10 — Test coverage audit + audio hardware mocking

## What to build

By this point, each issue from 01-09 has its own test file. This issue has two goals: (1) audit for gaps and fill them, and (2) solve the one testing problem that could not be solved earlier — mocking `sounddevice` so that `audio_input.py` and `audio_output.py` can be tested without real hardware.

Covers: `audio_input.py` (sounddevice callback → queue bridge, tested via mock), `audio_output.py` (queue → playback, tested via mock), full-pipeline smoke test with all-mock providers confirming `make test` is a complete fast suite.

## Acceptance criteria

- [ ] `audio_input.py` has a unit test that patches sounddevice and asserts `AudioRawFrame`s arrive in the queue
- [ ] `audio_output.py` has a unit test that puts `TTSAudioFrame`s in its input queue and asserts playback is triggered (via mock)
- [ ] Coverage report shows ≥ 90% line coverage across all non-provider modules
- [ ] Any gap identified in Issues 01-09 test coverage is filled
- [ ] `make test` runs in under 10 seconds with no API keys, no microphone, no speaker
- [ ] No test imports real sounddevice, makes network calls, or touches the filesystem
- [ ] All tests in `tests/` are separated from integration tests by `@pytest.mark.integration`

## Blocked by

- #06 — Interruption handling via CancelFrame
- #07 — Error handling via ErrorFrame
