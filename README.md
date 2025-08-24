# FFM-Style Web Navigation Agent — Starter Repo

A minimal, runnable scaffold for an FFM-style, risk‑aware web agent using Playwright (Python).

## Features (MVP)
- Instruction → Action loop with Playwright (sync API)
- Observation encoder (DOM + URL + optional a11y snapshot + screenshot)
- Safety shield (allowlist, selector blacklist, PII guard, rate‑limit)
- Simple policy stub (LLM-compatible interface, heuristic fallback)
- Replay logging of (state, action, outcome) to JSONL
- Tiny evaluation harness (success rate, steps, violations)
- Example tasks: form-filler + research-assistant

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
python -m src.agent.runner --start_url "https://example.com" --goal "example domain"
```

## Project Layout
```
.
├── README.md
├── requirements.txt
├── tasks/
│   ├── research_example.yaml
│   └── form_example.yaml
└── src/
    └── agent/
        ├── __init__.py
        ├── observe.py
        ├── policy_llm.py
        ├── safety.py
        ├── runner.py
        └── eval.py
```

## Notes
- Policy: `policy_llm.py` exposes `policy_fn(obs, goal_words)`; replace the heuristic with your LLM/planner.
- Safety: `safety.py` gates every action; tune `ALLOWED_DOMAINS`, `DANGEROUS_SELECTORS`, and PII regexes.
- Replays: JSONL files under `./replays/DATE/…` for later BC/RL training.
- Evaluation: `eval.py` contains a simple loop and metrics; extend with your own success heuristics.
- Next: Introduce a world‑model (ΔDOM + success + risk) and an MPC loop scoring candidate actions.
