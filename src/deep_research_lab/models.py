from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InformationRequirement:
    id: str
    description: str
    weight: float = 1.0


@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    source_id: str
    requirement_ids: tuple[str, ...]
    confidence: float
    cost: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be within [0, 1]")
        if self.cost < 0:
            raise ValueError("cost must be non-negative")


@dataclass
class ResearchState:
    query: str
    requirements: list[InformationRequirement]
    evidence: list[Evidence] = field(default_factory=list)
    spent_cost: float = 0.0
    steps: int = 0
