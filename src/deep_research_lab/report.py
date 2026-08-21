from __future__ import annotations

from .coverage import evaluate_coverage
from .models import ResearchState


def render_markdown_report(state: ResearchState) -> str:
    coverage = evaluate_coverage(state.requirements, state.evidence)
    lines = [
        f"# Research report: {state.query}",
        "",
        f"Weighted coverage: **{coverage.weighted_coverage:.1%}**",
        f"Research cost: **{state.spent_cost:.1f}**",
        f"Steps: **{state.steps}**",
        "",
        "## Requirement coverage",
        "",
    ]
    for req in state.requirements:
        lines.append(f"- {req.description}: {coverage.by_requirement[req.id]:.1%}")

    lines.extend(["", "## Evidence", ""])
    for item in state.evidence:
        lines.append(
            f"- **{item.confidence:.0%}** — {item.claim}  \n  Source: `{item.source_id}`"
        )
    return "\n".join(lines)
