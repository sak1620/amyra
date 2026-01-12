# Product Requirements Document (PRD)

## Product Name

**AI Human Voice & Video Interaction Platform (Local‑First MVP)**

---

## 1. Purpose & Vision

The goal of this product is to build a **local‑first, real‑time AI human interaction system** that enables natural **speech‑to‑speech conversations** and later **video‑based AI human calls**.

The MVP must:

* Run entirely on a **local machine**
* Avoid cloud dependency and billing anxiety
* Preserve a **production‑grade pipeline architecture**
* Allow future replacement of components without rewrites

This system is the foundation for:

* AI human video calls
* Human ↔ human random calls
* AI personas / creators
* Monetized real‑time AI interactions

---

## 2. Non‑Goals (Explicitly Out of Scope for MVP)

The MVP will **not** attempt to:

* Support 24/7 uptime
* Handle multiple concurrent users
* Achieve perfect speech recognition
* Provide production‑grade security
* Train or fine‑tune any ML models
* Use cloud APIs by default

---

## 3. Target Users

### Primary (MVP)

* Internal developer (single user)
* AI system designer / founder

### Future

* General users (voice & video calls)
* Creators building AI personas
* Brands deploying conversational AI humans

---

## 4. Canonical System Pipeline (Invariant)

This pipeline **must never change** across phases:

```
Audio In
  → Speech‑to‑Text (STT)
  → Intent + Emotion Detection
  → Large Language Model (LLM)
  → Response Planner
  → Text‑to‑Speech (TTS)
  → Audio / Video Out
```

All future versions may only **replace implementations**, not the pipeline itself.

---

## 5. MVP Functional Requirements

### 5.1 Core Capabilities

* Capture microphone input (local / browser)
* Convert speech to text (offline)
* Detect basic intent and emotion (rule‑based)
* Generate AI response using local LLM
* Convert text response to speech (offline)
* Play audio response locally
* Allow user to interrupt AI at any time

---

### 5.2 Speech‑to‑Text (STT)

**Requirements**

* Fully offline
* Accept WAV audio input
* Reasonable latency (< 1s chunks acceptable)

**MVP Implementation**

* `whisper.cpp`
* Models: `small.en` or `medium.en`

---

### 5.3 Intent & Emotion Detection

**Requirements**

* Lightweight
* Deterministic
* Replaceable

**MVP Implementation**

* Rule‑based heuristics
* No ML training

Emotion output is **advisory metadata only**.

---

### 5.4 LLM (Conversation Brain)

**Requirements**

* Local execution
* Streaming‑capable
* Deterministic prompts

**MVP Implementation**

* Ollama
* Models:

  * `llama3.1:8b`
  * `mistral:7b`

---

### 5.5 Text‑to‑Speech (TTS)

**Requirements**

* Offline
* Low latency
* Interruptible

**MVP Implementation**

* Piper TTS
* Coqui TTS (optional upgrade)

---

### 5.6 Interrupt / Barge‑In

**Requirements**

* User speech must stop AI audio immediately
* No buffering that blocks interruption

**Baseline Logic**

```python
if mic_detects_speech:
    tts.stop()
```

---

### 5.7 User Interface (MVP)

**Supported Interfaces**

* CLI (press‑to‑talk)
* Browser UI (mic button)

**UI Responsibilities**

* Capture audio
* Display transcript (optional)
* Play AI audio

UI must contain **no business logic**.

---

## 6. Non‑Functional Requirements

### 6.1 Local‑First Constraint

* All components must run on `localhost`
* No paid APIs
* No required internet access

---

### 6.2 Latency Targets (MVP)

| Component  | Target     |
| ---------- | ---------- |
| STT        | 300–800 ms |
| LLM        | 1–2 sec    |
| TTS        | 200–400 ms |
| End‑to‑End | < 3 sec    |

Latency is prioritized over accuracy.

---

### 6.3 Observability

The system must log:

* Input timestamp
* Output timestamp
* Per‑component latency
* Errors (explicit, no silent failures)

Logs must be:

* Local
* Human‑readable
* Structured (JSON preferred)

---

### 6.4 Determinism & Reliability

* No hidden retries
* No silent fallbacks
* No background model switching

Failures must be explicit and local.

---

## 7. Architecture & Code Requirements

### 7.1 Interface‑Driven Design

Each core component must implement an interface:

* `STTEngine`
* `LLMEngine`
* `TTSEngine`

Implementations must be swappable without modifying the orchestrator.

---

### 7.2 Orchestrator Rules

The orchestrator:

* Coordinates data flow
* Contains no ML logic
* Contains no UI logic
* Is deterministic per turn

This file must survive into production unchanged.

---

## 8. Hardware Requirements

### Minimum Viable

* CPU: 6–8 cores
* RAM: 16 GB
* GPU: Not required
* Storage: SSD

### Comfortable Development

* RAM: 32 GB
* GPU: RTX 3060 / 4060 (12 GB VRAM)

---

## 9. Security & Privacy (MVP Level)

* No recording without explicit user action
* No background mic usage
* No cloud data transmission
* No hidden storage of audio or transcripts

---

## 10. Validation Criteria (MVP Exit)

The MVP is considered complete when:

* User can speak locally
* Speech is transcribed
* AI responds verbally
* AI can be interrupted
* System runs without internet
* Latency metrics are visible

---

## 11. Future Phases (High‑Level)

* Phase 1: WebRTC audio calls
* Phase 2: Human ↔ human calls + moderation
* Phase 3: AI human video avatar
* Phase 4: Hybrid cloud optimization
* Phase 5: Monetization & scale

---

## 12. Success Metric (Early)

The MVP is successful if:

> A local user can have a **natural, interruptible voice conversation** with an AI that feels like a call, not a chatbot.

---

## 13. Final Constraint

> If a feature cannot be explained on a whiteboard, it must not be added.
