# AgentForge Proof of Concept

> Proof of Concept for **AgentForge**, an AI-driven multi-agent software engineering system.

This repository contains the proof of concept developed to validate the core workflow of AgentForge. It demonstrates how multiple specialized AI agents can collaboratively generate a simple full-stack application from a natural language description through coordinated task execution, validation, and human approval.

---

## Features

- Generate software requirements
- Human approval checkpoints
- Generate system architecture
- Generate frontend and backend implementations
- Integration validation
- QA review
- Automatic regeneration when issues are detected
- Final human approval

---

## Workflow

```text
User
  │
  ▼
Requirements Agent
  │
Human Approval
  │
  ▼
Architecture Agent
  │
Human Approval
  │
 ┌─────────────┐
 ▼             ▼
Frontend    Backend
  │             │
  └──────┬──────┘
         ▼
 Integration
         │
         ▼
      QA Review
         │
         ▼
 Final Approval
```

---

## Project Structure

```text
AgentForge-PoC/
│
├── agents/
├── models/
├── prompts/
├── orchestrator.py
├── app.py
├── human_approval.py
├── prompt_loader.py
└── README.md
```

---

## How to Use

Clone the repository.

```bash
git clone https://github.com/Ali-00Q/AgentForge-PoC.git

cd AgentForge-PoC
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

```bash
venv\Scripts\activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```
1. Open this url: https://ai.google.dev/gemini-api/docs/api-key
2. Create your API key
3. Paste the key in the .env file
---

## Usage

```bash
python app.py
```

---

---

## Current Limitations

This repository is a proof of concept and focuses on validating the orchestration workflow.

Current limitations include:

- Prompt-based agents
- Sequential execution
- Single LLM provider
- No persistent agent memory
- Basic QA review
- Console-based human approval
- No automatic deployment

---
