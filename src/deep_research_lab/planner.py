from __future__ import annotations

from .models import InformationRequirement


def default_plan(query: str) -> list[InformationRequirement]:
    """Create a generic research decomposition for the MVP.

    This is deliberately deterministic. Later, replace this function with an
    LLM-backed planner that emits the same InformationRequirement schema.
    """
    return [
        InformationRequirement("background", f"Background and definitions for: {query}", 0.8),
        InformationRequirement("support", "Best supporting empirical or primary evidence", 1.0),
        InformationRequirement("comparison", "Relevant alternatives or direct comparisons", 1.0),
        InformationRequirement("limitations", "Limitations, failures, and counter-evidence", 1.0),
        InformationRequirement("recent", "Recent developments and current state of the field", 0.9),
    ]
