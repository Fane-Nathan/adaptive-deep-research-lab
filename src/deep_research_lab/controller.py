from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .coverage import CoverageReport, evaluate_coverage
from .evidence import deduplicate_evidence
from .models import Evidence, InformationRequirement, ResearchState


class ResearchBackend(Protocol):
    async def research(self, query: str, requirement: InformationRequirement) -> list[Evidence]: ...


@dataclass(frozen=True)
class ControllerConfig:
    max_cost: float = 10.0
    target_coverage: float = 0.78
    min_marginal_gain: float = 0.015
    max_steps: int = 20


@dataclass(frozen=True)
class RunResult:
    state: ResearchState
    coverage: CoverageReport
    stop_reason: str


async def run_adaptive_research(
    query: str,
    requirements: list[InformationRequirement],
    backend: ResearchBackend,
    config: ControllerConfig = ControllerConfig(),
) -> RunResult:
    state = ResearchState(query=query, requirements=requirements)
    previous_coverage = 0.0

    while state.steps < config.max_steps and state.spent_cost < config.max_cost:
        report = evaluate_coverage(state.requirements, state.evidence)
        if report.weighted_coverage >= config.target_coverage:
            return RunResult(state, report, "target_coverage")

        weakest_id = report.weakest_requirement
        requirement = next(req for req in requirements if req.id == weakest_id)
        new_evidence = await backend.research(query, requirement)

        remaining_budget = config.max_cost - state.spent_cost
        affordable = []
        running_cost = 0.0
        for item in new_evidence:
            if running_cost + item.cost <= remaining_budget:
                affordable.append(item)
                running_cost += item.cost

        if not affordable:
            return RunResult(state, report, "budget_exhausted")

        state.evidence = deduplicate_evidence(state.evidence + affordable)
        state.spent_cost += running_cost
        state.steps += 1

        updated = evaluate_coverage(state.requirements, state.evidence)
        marginal_gain = updated.weighted_coverage - previous_coverage
        previous_coverage = updated.weighted_coverage

        if state.steps > 1 and marginal_gain < config.min_marginal_gain:
            return RunResult(state, updated, "low_marginal_gain")

    final = evaluate_coverage(state.requirements, state.evidence)
    reason = "budget_exhausted" if state.spent_cost >= config.max_cost else "max_steps"
    return RunResult(state, final, reason)
