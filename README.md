# Adaptive Deep Research Lab

A small experimental framework for testing **coverage-aware deep research** without requiring large-model training or expensive infrastructure.

The initial research question is:

> Can an adaptive controller improve evidence coverage per unit cost compared with a fixed research plan?

## MVP architecture

```text
User query
   ↓
Planner
   ↓
Information requirements
   ↓
Research workers
   ↓
Evidence store
   ↓
Coverage evaluator
   ↓
Adaptive controller ──→ research weakest gap
   ↓
Stop when utility < threshold or budget exhausted
   ↓
Report synthesis
```

The repository starts in **mock mode** so the orchestration and scoring logic can be tested deterministically before adding real LLM/search providers.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .[dev]
pytest
python -m deep_research_lab.cli "Are hyperbolic embeddings useful for hierarchical classification?"
```

## What we will test

Baseline A: fixed one-pass research.

Baseline B: coverage-aware adaptive research.

Primary metrics:

- weighted requirement coverage
- evidence confidence
- source diversity
- research cost / tool calls
- marginal coverage gain per research step

Later integrations can add:

- Exa / Brave / Tavily for web search
- OpenAlex / Semantic Scholar / Crossref for scholarly search
- GROBID + Docling for papers
- a reranker such as BGE
- OpenAI / Anthropic / Gemini / local Qwen models
- PostgreSQL/pgvector for persistent evidence storage

## Scope

This is intentionally a bachelor-scale experimental harness, not an attempt to reproduce Parallel, Anthropic Research, or Kimi infrastructure.
