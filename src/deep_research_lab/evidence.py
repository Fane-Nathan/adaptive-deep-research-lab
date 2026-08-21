from __future__ import annotations

from .models import Evidence


def deduplicate_evidence(items: list[Evidence]) -> list[Evidence]:
    """Deduplicate exact claim/source pairs, retaining strongest confidence."""
    best: dict[tuple[str, str], Evidence] = {}
    for item in items:
        key = (item.source_id, item.claim.strip().lower())
        current = best.get(key)
        if current is None or item.confidence > current.confidence:
            best[key] = item
    return list(best.values())
