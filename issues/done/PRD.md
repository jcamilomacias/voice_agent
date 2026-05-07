# PRD: Minimal Real-Time Voice Agent in Pure Python

## Problem Statement

Developers who want to understand how production voice agent frameworks like Pipecat and LiveKit Agents work internally have no minimal, readable reference implementation to study. Existing frameworks are powerful but opaque — their abstractions (frames, processors, pipelines) are difficult to understand without first building the concepts from scratch. A developer learning this space needs a working, end-to-end voice conversation loop that exposes the architecture explicitly, without hiding it behind framework magic.

## Solution

A minimal, fully functional real-time voice agent written in pure Python using asyncio. The agent implements a complete voice conversation loop: microphone input → voice activity detection → speech-to-text → LLM reasoning → text-to-speech → speaker output. Every component is built around the same frame-based, queue-driven pipeline architecture that underpins Pipecat and LiveKit Agents, making the design patterns directly transferable. All providers (VAD, STT, LLM, TTS) are swappable via Protocol interfaces, and the entire pipeline is unit-testable without real hardware or API calls.

## User Stories

1. As a developer, I want a working voice conversation loop, so that I can speak to the agent and hear a response without any framework boilerplate.
2. As a developer, I want all pipeline messages to be typed Frame objects, so that I understand how Pipecat's frame model works by reading the code.
3. As a developer, I want each pipeline stage to communicate via asyncio queues, so that I understand the producer/consumer pattern used in real-time agent frameworks.
4. As a developer, I want voice activity detection to emit `UserStartedSpeakingFrame` and `UserStoppedSpeakingFrame`, so that I understand how the pipeline knows when to begin and end transcription.
5. As a developer, I want silero-vad as the default VAD, so that speech boundaries are detected accurately even in noisy environments.
6. As a developer, I want to swap the VAD provider via a single config change, so that I can experiment with alternative VAD implementations without modifying pipeline logic.
7. As a developer, I want Deepgram streaming STT as the default, so that I get partial transcripts in real time and understand streaming frame flow.
8. As a developer, I want faster-whisper as a local STT fallback, so that I can develop offline without incurring API costs.
9. As a developer, I want to swap the STT provider via a single config change, so that I understand how provider abstraction works in practice.
10. As a developer, I want Groq as the default LLM, so that end-to-end latency stays under 1.5 seconds and the pipeline's streaming behavior is clearly observable.
11. As a developer, I want the LLM to stream tokens rather than returning a full response, so that I understand how streaming enables early TTS synthesis.
12. As a developer, I want to swap the LLM provider via a single config change, so that I can switch between Groq, OpenAI, and Anthropic without touching pipeline code.
13. As a developer, I want Cartesia as the default TTS, so that audio synthesis begins quickly (~150ms first chunk) while the LLM is still generating.
14. As a developer, I want Piper as a local TTS fallback, so that the pipeline runs fully offline when needed.
15. As a developer, I want to swap the TTS provider via a single config change, so that provider abstraction is consistent across all pipeline stages.
16. As a developer, I want LLM tokens to be aggregated into sentence chunks before being sent to TTS, so that synthesized speech sounds natural rather than word-by-word.
17. As a developer, I want TTS synthesis to begin as soon as the first sentence is available, so that perceived latency is minimized while the LLM finishes generating.
18. As a developer, I want interruption handling via `CancelFrame`, so that if I speak while the agent is talking, playback stops immediately and the pipeline resets.
19. As a developer, I want `CancelFrame` to propagate through all processors, so that every stage clears its buffer and returns to a clean listening state.
20. As a developer, I want conversation history to persist across turns, so that the agent maintains context throughout a session.
21. As a developer, I want conversation history to use a sliding window, so that the context never exceeds the LLM's token limit.
22. As a developer, I want the sliding window size to be configurable, so that I can tune memory vs. token cost trade-offs without code changes.
23. As a developer, I want microphone capture to bridge sounddevice callbacks into the asyncio event loop, so that audio input integrates cleanly with the async pipeline.
24. As a developer, I want audio captured at 16000 Hz with 512-sample chunks, so that VAD, STT, and the audio pipeline all operate at the same native sample rate without resampling.
25. As a developer, I want all API keys and configuration to load from a `.env` file via pydantic BaseSettings, so that secrets are never hardcoded.
26. As a developer, I want provider errors to emit `ErrorFrame` rather than crash the pipeline, so that I can observe and handle failures gracefully.
27. As a developer, I want fatal vs. non-fatal errors to be distinguished in `ErrorFrame`, so that the pipeline can decide whether to shut down or continue.
28. As a developer, I want per-stage latency tracked via `LatencyTracker`, so that I can measure STT latency, LLM time-to-first-token, TTS time-to-first-audio, and end-to-end latency.
29. As a developer, I want unit tests that inject frames directly into processor queues using mock providers, so that I can test pipeline behavior without real hardware or API calls.
30. As a developer, I want integration tests tagged separately from unit tests, so that `make test` runs fast by default and integration tests are opt-in.
31. As a developer, I want a `Makefile` with `make install`, `make test`, and `make run` targets, so that setup and execution are reproducible in one command.
32. As a developer, I want a `.env.example` file listing all required API keys, so that project setup is self-documenting.

## Implementation Decisions

### Frame Model
- All pipeline messages are instances of a `Frame` base dataclass.
- Data frames: `AudioRawFrame` (raw PCM bytes, sample rate, channels), `TranscriptionFrame` (text, is_final), `LLMResponseFrame` (text, is_final), `TTSAudioFrame` (audio bytes).
- VAD state frames: `UserStartedSpeakingFrame`, `UserStoppedSpeakingFrame`.
- System frames: `StartFrame`, `EndFrame`, `CancelFrame`, `ErrorFrame` (processor name, exception, fatal flag).
- `is_final: bool` on `TranscriptionFrame` and `LLMResponseFrame` enables streaming — consumers act on final frames and can preview partials.

### Pipeline Architecture
- Stages communicate exclusively via `asyncio.Queue`. No shared mutable state between processors except `ConversationContext` (injected into the LLM processor).
- Each stage is an async function with signature `(input_queue, output_queue, provider, ...)`.
- `pipeline.py` creates all queues, instantiates all processors with injected providers, launches each as an `asyncio.create_task()`, and returns the task list.
- System frames (`CancelFrame`, `EndFrame`) propagate immediately through all processors without buffering.

### Provider Abstraction
- Each component type (VAD, STT, LLM, TTS) defines a `Protocol` interface in its `base.py`.
- Default implementations: silero-vad, Deepgram, Groq, Cartesia.
- Fallback implementations: faster-whisper (STT), Piper (TTS).
- Swapping providers requires only changing the injected object in `main.py` or `config.py` — no pipeline code changes.

### Audio I/O
- Microphone capture uses `sounddevice` with a C-thread callback bridged to the asyncio event loop via `loop.call_soon_threadsafe(queue.put_nowait, frame)`.
- Sample rate: 16000 Hz. Chunk size: 512 samples (~32ms). Both configurable via `config.py`.
- Speaker output reads `TTSAudioFrame`s from a queue and plays them via sounddevice.

### Sentence Aggregation
- A `SentenceAggregator` utility accumulates LLM tokens and yields complete sentences on sentence-ending punctuation.
- Lives in `utils/` as a pure, stateful text utility with no queue logic.
- On `CancelFrame`, the aggregator's internal buffer is flushed without emitting.

### Conversation Management
- `ConversationContext` holds `messages: list[dict]` in OpenAI/Anthropic message format.
- Exposes `add_user_turn(text)`, `add_assistant_turn(text)`, and `get_messages() -> list[dict]`.
- `get_messages()` applies the sliding window: returns the system prompt plus the last `max_turns * 2` messages.
- `max_turns` is configurable via `config.py`, default 10.

### Configuration
- All settings loaded from `.env` via pydantic `BaseSettings`.
- Includes: API keys (Deepgram, Groq, Cartesia), audio settings (sample rate, chunk size), conversation settings (max_turns, system_prompt), provider selection flags.

### Interruption Handling
- When VAD emits `UserStartedSpeakingFrame` while TTS is playing, the audio output processor emits a `CancelFrame` upstream.
- All processors handle `CancelFrame` by clearing internal buffers and forwarding the frame downstream.
- The pipeline returns to the listening state immediately.

### Error Handling
- Each processor wraps provider calls in try/except and emits `ErrorFrame` on failure.
- `pipeline.py` handles `ErrorFrame` centrally: logs all errors, sends `EndFrame` for fatal ones.

### Tooling
- Package manager: `uv`.
- Python: 3.11+.
- Makefile targets: `make install`, `make test`, `make test-integration`, `make run`.

## Testing Decisions

### What makes a good test
Tests should verify observable external behavior — what frames come out of a processor given specific frames as input — not internal implementation details like method call counts or buffer state. A processor test creates real `asyncio.Queue` instances, puts frames in, runs the processor with a mock provider, and asserts on the frames that come out.

### Modules with unit tests
- `frames.py` — frame instantiation, dataclass field validation.
- `conversation.py` — sliding window behavior, turn accumulation, system prompt inclusion.
- `utils/sentence_aggregator.py` — sentence boundary detection, partial accumulation, flush-on-cancel behavior.
- `processors/vad/` — correct emission of `UserStartedSpeakingFrame` / `UserStoppedSpeakingFrame` given mock VAD output.
- `processors/stt/` — correct emission of `TranscriptionFrame` (partial and final) given mock STT output.
- `processors/llm/` — correct emission of `LLMResponseFrame` tokens, correct `ConversationContext` updates, `CancelFrame` passthrough.
- `processors/tts/` — correct emission of `TTSAudioFrame` chunks, `CancelFrame` buffer flush.
- `pipeline.py` — end-to-end frame flow using all-mock providers; `CancelFrame` propagation across the full pipeline.

### Integration tests
- Tagged `@pytest.mark.integration`, excluded from default `make test`, run via `make test-integration`.
- Cover: real Deepgram transcription round-trip, real Groq completion, real Cartesia synthesis, end-to-end latency assertions using `LatencyTracker`.

## Out of Scope

- Web or mobile interface — this is a CLI/terminal tool only.
- Multi-speaker or diarization support.
- Wake word detection.
- Conversation summarization for long-context management (sliding window only for v1).
- Token-based context truncation (configurable turn count is sufficient for v1).
- Deployment, containerization, or cloud hosting.
- Custom fine-tuned models.
- Retry logic for failed provider calls (log and emit `ErrorFrame` only).
- Audio format conversion or resampling (all components use 16000 Hz natively).

## Further Notes

- The primary goal is educational: the code should be readable enough that a developer can trace a single utterance through the entire pipeline by reading `main.py` and following function calls.
- The frame model, queue-based stages, and Protocol-based providers are the three concepts that directly transfer to Pipecat and LiveKit Agents. These should be the most polished parts of the implementation.
- `LatencyTracker` measurements should be printed to stdout during a live session so latency characteristics are immediately visible during development.
- The `SentenceAggregator` + streaming TTS interaction is the most subtle part of the pipeline and deserves the most thorough unit test coverage.
