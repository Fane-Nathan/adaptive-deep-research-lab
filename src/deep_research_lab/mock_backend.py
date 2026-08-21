from __future__ import annotations

from itertools import count

from .models import Evidence, InformationRequirement


class MockResearchBackend:
    """Deterministic research backend used to test orchestration cheaply."""

    def __init__(self) -> None:
        self._counter = count(1)
        self._attempts: dict[str, int] = {}

    async def research(self, query: str, requirement: InformationRequirement) -> list[Evidence]:
        attempt = self._attempts.get(requirement.id, 0) + 1
        self._attempts[requirement.id] = attempt
        n = next(self._counter)
        base = {
            "background": 0.78,
            "support": 0.62,
            "comparison": 0.48,
            "limitations": 0.32,
            "recent": 0.52,
        }.get(requirement.id, 0.45)
        confidence = min(0.95, base + 0.12 * (attempt - 1))
        return [
            Evidence(
                id=f"ev-{n}",
                claim=f"Mock finding #{attempt} for {requirement.description}",
                source_id=f"mock://{requirement.id}/{attempt}",
                requirement_ids=(requirement.id,),
                confidence=confidence,
                cost=1.0,
            )
        ]
