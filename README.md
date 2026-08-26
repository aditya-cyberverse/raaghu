# Raaghu: Production-Grade Modular AI Agent Harness

A composable framework for building scalable, production-ready AI agents with decoupled, reusable components.

## Architecture: Five Modular Lego Blocks

1. **Brain** (core) – Orchestration engine managing agent lifecycle and decision loops
2. **Memory** (state management) – Context, session, and knowledge persistence layer
3. **Tool** (tools registry) – Decoupled function registry with capability contracts
4. **Bouncer** (guardrails) – Safety, compliance, and policy enforcement middleware
5. **Conductor** (providers) – Model adapter abstraction for multi-LLM support

## Project Structure

```
raaghu/
├── src/
│   ├── core/        # Orchestration loop & agent runtime
│   ├── providers/   # Model adapters (OpenAI, Claude, etc.)
│   ├── tools/       # Tool registry & execution layer
│   └── guardrails/  # Safety, policy & compliance enforcement
├── README.md        # This file
├── package.json     # Node.js dependencies
└── requirements.md  # Engineering specifications
```

## Getting Started

See `requirements.md` for technical specifications and engineering guidelines.
