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

## Blocked by

- #03 — STT stage — live transcription
