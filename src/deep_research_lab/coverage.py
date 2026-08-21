from __future__ import annotations

from dataclasses import dataclass

from .models import Evidence, InformationRequirement


@dataclass(frozen=True)
class CoverageReport:
    by_requirement: dict[str, float]
    weighted_coverage: float

    @property
    def weakest_requirement(self) -> str:
        return min(self.by_requirement, key=self.by_requirement.get)


def _requirement_score(requirement_id: str, evidence: list[Evidence]) -> float:
    """Simple noisy-OR evidence aggregation.

    Multiple independent pieces of evidence increase confidence while the
    score remains bounded by 1.0. Evidence from duplicate source IDs counts
    once, using the strongest item from that source.
    """
    best_by_source: dict[str, float] = {}
    for item in evidence:
        if requirement_id in item.requirement_ids:
            best_by_source[item.source_id] = max(
                item.confidence, best_by_source.get(item.source_id, 0.0)
            )

    probability_uncovered = 1.0
    for confidence in best_by_source.values():
        probability_uncovered *= 1.0 - confidence
    return 1.0 - probability_uncovered


def evaluate_coverage(
    requirements: list[InformationRequirement], evidence: list[Evidence]
) -> CoverageReport:
    scores = {req.id: _requirement_score(req.id, evidence) for req in requirements}
    total_weight = sum(req.weight for req in requirements)
    weighted = (
        sum(scores[req.id] * req.weight for req in requirements) / total_weight
        if total_weight
        else 0.0
    )
    return CoverageReport(scores, weighted)
