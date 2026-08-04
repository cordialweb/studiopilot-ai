# StudioPilot AI Architecture

**Version:** 0.1.0

**Last Updated:** August 2026

---

# Overview

StudioPilot AI is an autonomous multi-agent production platform built using:

- FastAPI
- Google Agent Development Kit (ADK)
- Gemini
- PostgreSQL
- SQLAlchemy

The system is designed using Clean Architecture while leveraging Google ADK as the native AI execution engine.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| AI Framework | Google ADK |
| LLM | Gemini 2.5 Flash |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Configuration | python-dotenv |
| Deployment | Google Cloud Run (planned) |
| Agent Runtime | Google Agent Engine (planned) |

---

# High-Level Architecture

```
                    FastAPI
                       │
                       ▼
               StudioPilot API
                       │
                       ▼
              StudioPilotEngine
                       │
                       ▼
                  ADK Runner
                       │
                       ▼
               Session Service
                       │
                       ▼
               Studio Root Agent
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
Document Agent                  Future Agents
                                • Planner Agent
                                • Crew Agent
                                • Budget Agent
                                • Director Agent
```

---

# Backend Structure

```
backend/

app/
│
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
│
├── adk/
│   ├── config.py
│   ├── engine.py
│   │
│   ├── studio/
│   │     ├── __init__.py
│   │     └── agent.py
│   │
│   └── document/
│         ├── __init__.py
│         ├── agent.py
│         ├── prompts.py
│         └── tools.py
│
└── main.py
```

---

# AI Architecture

Google ADK is used as the native execution framework.

Current architecture:

```
StudioPilotEngine

↓

Runner

↓

SessionService

↓

Studio Root Agent

↓

Document Agent

↓

Gemini
```

---

# Engine

Location:

```
app/adk/engine.py
```

Responsibilities:

- Initialize Runner
- Initialize Session Service
- Register Root Agent
- Manage agent execution

---

# Runner

Provided by Google ADK.

Responsibilities:

- Execute agents
- Generate events
- Maintain execution workflow

Methods currently used:

- run()
- run_async()

---

# Session Service

Development:

```
InMemorySessionService
```

Future:

```
DatabaseSessionService
```

Possible Cloud deployment:

```
VertexAiSessionService
```

Session stores:

- Session ID
- User ID
- Events
- State

---

# Studio Root Agent

Location:

```
app/adk/studio/agent.py
```

Acts as the entry point for the complete AI system.

Future responsibility:

- Route tasks to specialized agents.

---

# Document Agent

Location:

```
app/adk/document/agent.py
```

Responsibilities:

- Analyze screenplay documents
- Extract structured information
- Return JSON responses
- Use Gemini

Future tools:

- PDF parser
- OCR
- Metadata extraction

---

# Data Flow

```
User

↓

FastAPI

↓

StudioPilotEngine

↓

Runner

↓

Session

↓

Root Agent

↓

Document Agent

↓

Gemini

↓

Events

↓

API Response
```

---

# Configuration

Environment variables:

```
DATABASE_URL

GEMINI_API_KEY

GEMINI_MODEL
```

Loaded through:

```
app/core/config.py
```

---

# Design Principles

- Clean Architecture
- Separation of Concerns
- Modular Agents
- Native Google ADK
- Native Gemini Integration
- Reusable Components
- Test-Driven Development

---

# Future Agents

- Document Agent
- Planner Agent
- Crew Agent
- Budget Agent
- Director Agent
- Scheduling Agent
- VFX Agent
- Audio Agent

---

# Current Status

## Completed

- Project Structure
- FastAPI Backend
- PostgreSQL Integration
- SQLAlchemy
- Alembic
- Google ADK Installation
- Gemini Configuration
- StudioPilotEngine
- Runner Initialization
- Session Service
- Studio Root Agent
- Document Agent Skeleton

## In Progress

- First Runner Execution
- First Gemini Response

## Planned

- Screenplay Analysis
- Multi-Agent Collaboration
- Agent Engine Deployment
- Cloud Run Deployment

---

# Architecture Philosophy

StudioPilot AI uses Google ADK as the execution engine rather than wrapping Gemini directly.

Business logic remains inside FastAPI services, while AI execution is delegated to ADK.

This separation allows the application to scale from a single document agent to a complete multi-agent production platform without changing the overall architecture.