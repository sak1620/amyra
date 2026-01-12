# AMYRA

**AMYRA** — **Adaptive Multimodal Yielding Real-time Architecture**

Amyra is a local-first, real-time conversational AI system designed to feel **present**, **interruptible**, and **human** — without depending on the cloud.

It is not a chatbot.
It is not a single model.
It is a stable, extensible **conversation pipeline**.

---

## Why AMYRA?

Most conversational AI systems optimize for:
- Model size
- Cloud scale
- Perfect answers

Amyra optimizes for something else:

> **Presence.**

Amyra listens first, responds quickly, yields when interrupted, and runs locally by default.  
Accuracy improves over time — but **real-time interaction comes first**.

---

## What AMYRA Stands For

**A**daptive  
**M**ultimodal  
**Y**ielding  
**R**eal-time  
**A**rchitecture  

Each word is intentional:

- **Adaptive** — Responds to user intent, emotion, and timing
- **Multimodal** — Voice today, video and avatars tomorrow
- **Yielding** — Stops speaking when the user speaks (barge-in by design)
- **Real-time** — Low latency is a core feature, not an optimization
- **Architecture** — A system, not a demo or a single model

---

## Core Design Principles

### 1. Presence Over Performance
Fast enough beats perfect.
Natural pauses beat instant replies.

### 2. Local-First by Default
Amyra runs on your machine:
- No mandatory cloud calls
- No surprise billing
- Works offline

Cloud integration is optional and replaceable.

### 3. Interruptibility Is a Feature
If the user speaks, Amyra stops.
No monologues. No talking over people.

### 4. Stable Pipeline, Replaceable Parts
The architecture does not change.
Only the engines do.

---

## Canonical Pipeline (Never Changes)
Audio In
↓
Speech-to-Text (STT)
↓
Intent + Emotion
↓
LLM (Reasoning)
↓
Response Planning
↓
Text-to-Speech (TTS)
↓
Audio / Video Out


This same pipeline supports:
- Local MVP
- WebRTC calls
- AI phone agents
- Human ↔ AI video
- AI avatars

---

## Current Scope (Local MVP)

- Runs entirely on `localhost`
- No cloud dependency
- Single-user, single-session
- Acceptable (not perfect) latency
- CLI or simple browser UI

### Typical Stack
- STT: Whisper.cpp
- LLM: Local models via Ollama
- TTS: Piper / Coqui
- Orchestration: Python
- UI: CLI → Browser → WebRTC (later)

---

## What AMYRA Is Not

- ❌ A chatbot wrapper
- ❌ A cloud-only service
- ❌ A personality simulator
- ❌ A demo glued to one model

Amyra is a **conversation system**.

---

## Project Structure (Simplified)

amyra/
├── orchestrator/ # Core control logic (stable)
├── stt/ # Speech-to-text engines
├── llm/ # Reasoning engines
├── tts/ # Text-to-speech engines
├── emotion/ # Intent & emotion detection
├── audio/ # Mic / speaker I/O
└── ui/ # CLI / Web UI


The **orchestrator** is the heart of the system and is designed to survive into production unchanged.

---

## Guiding Motto

> **Presence first. Real-time over perfect. Interruptible by design.**

---

## Status

🚧 Active development — Local MVP phase  
📍 Architecture locked, components evolving

---

## License

MIT

---

## Vision

Amyra is built to become:
- A real-time AI caller
- A human-AI video presence
- A creator-driven AI persona platform
- An enterprise conversational system

All without rewriting the core.

---

**Amyra listens first.**

