# 04 — LLM stage — streaming response + conversation context

## What to build

Add an LLM stage that receives final `TranscriptionFrame`s and emits streaming `LLMResponseFrame`s token-by-token. Implements `ConversationContext` with a sliding window for multi-turn memory. Implements `SentenceAggregator` to batch LLM tokens into sentence-sized chunks before passing downstream. Default LLM provider is Groq.

Includes: `frames.py` additions (`LLMResponseFrame` with `text: str`, `is_final: bool`), `processors/llm/base.py` (`LLMProvider` Protocol), `processors/llm/groq.py` (Groq streaming implementation), `conversation.py` (`ConversationContext` with sliding window), `utils/sentence_aggregator.py` (`SentenceAggregator`), pipeline updated to include LLM stage, `GROQ_API_KEY` added to `.env.example`.

## Acceptance criteria

- [ ] Speaking produces a streamed LLM response printed to stdout sentence-by-sentence
- [ ] `LLMResponseFrame` tokens arrive with `is_final: False`; final frame has `is_final: True`
- [ ] `ConversationContext` retains history across turns up to `max_turns` (default 10)
- [ ] `get_messages()` applies the sliding window and prepends the system prompt
- [ ] `SentenceAggregator` buffers tokens and yields on sentence-ending punctuation
- [ ] `LLMProvider` Protocol is defined in `base.py` with a clear interface
- [ ] `GROQ_API_KEY` is loaded from `.env` via `config.py`
- [ ] `max_turns` and `system_prompt` are configurable via `config.py`
- [ ] `CancelFrame` flushes `SentenceAggregator` buffer without emitting

## Tests to write

### Sub-task A — Pure utilities first (tests/test_conversation.py, tests/test_sentence_aggregator.py)

`ConversationContext` and `SentenceAggregator` are pure Python with no external dependencies. Write and run their tests before touching the LLM processor. This is intentional: verify the building blocks are correct before stacking things on top.

- [ ] `ConversationContext.add_user_turn()` and `add_assistant_turn()` append correctly
- [ ] `get_messages()` prepends the system prompt in position 0
- [ ] `get_messages()` returns all turns when count is below `max_turns`
- [ ] `get_messages()` applies the sliding window when count exceeds `max_turns` (boundary: exactly `max_turns`, and `max_turns + 1`)
- [ ] `SentenceAggregator.push()` returns `[]` when no sentence boundary reached yet
- [ ] `SentenceAggregator.push()` yields a complete sentence on `.` `!` `?`
- [ ] `SentenceAggregator.push()` yields multiple sentences when a token contains two boundaries
- [ ] `SentenceAggregator.flush()` returns partial buffer and clears it
- [ ] `SentenceAggregator.flush()` on empty buffer returns `[]`

### Sub-task B — LLM processor (tests/test_llm_processor.py)

Define `MockLLMProvider` implementing `LLMProvider`. It takes a list of tokens and yields them one by one.

- [ ] `MockLLMProvider` satisfies the `LLMProvider` Protocol
- [ ] Test: `TranscriptionFrame(is_final=True)` → `LLMResponseFrame`s emitted, last has `is_final=True`
- [ ] Test: `TranscriptionFrame(is_final=False)` → no `LLMResponseFrame` emitted (partials are ignored)
- [ ] Test: `ConversationContext` is updated with the user turn before calling the provider
- [ ] Test: `CancelFrame` → `SentenceAggregator` buffer flushed without emitting, frame propagates
- [ ] Test: `EndFrame` propagates through the LLM processor
- [ ] `make test` passes with no `GROQ_API_KEY` and no network

## Blocked by

- #03 — STT stage — live transcription
