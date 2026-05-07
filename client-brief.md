I want to build a minimal voice agent in pure Python using asyncio to deeply understand the architecture behind frameworks like Pipecat and LiveKit Agents.Goal: A working real-time voice conversation loop that does:
Audio input (microphone)
Speech-to-Text (STT)
LLM reasoning / conversation logic
Text-to-Speech (TTS)
Audio output (speaker)
Constraints:
Pure Python + asyncio (no heavy frameworks at first)
Use popular libraries (e.g. sounddevice, faster-whisper or Deepgram, OpenAI/Anthropic/Groq for LLM, ElevenLabs/Cartesia or Piper for TTS)
Focus on understanding the pipeline / frame / event-driven architecture
Keep it modular and testable
Ask me lots of questions about requirements, trade-offs, tech choices, project structure, testing strategy, etc.