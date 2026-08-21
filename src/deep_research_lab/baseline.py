from __future__ import annotations

from .controller import ControllerConfig, ResearchBackend, RunResult
from .coverage import evaluate_coverage
from .evidence import deduplicate_evidence
from .models import InformationRequirement, ResearchState


async def run_fixed_research(
    query: str,
    requirements: list[InformationRequirement],
    backend: ResearchBackend,
    config: ControllerConfig = ControllerConfig(),
) -> RunResult:
    """Run a deterministic round-robin research policy.

    This baseline intentionally shares the same backend, evidence model,
    budget, target coverage, and stopping rules as the adaptive controller.
    The only policy difference is requirement selection: fixed research cycles
    through requirements in their original order instead of targeting the
    currently weakest requirement.
    """
    state = ResearchState(query=query, requirements=requirements)
    previous_coverage = 0.0
    requirement_index = 0

    while state.steps < config.max_steps and state.spent_cost < config.max_cost:
        report = evaluate_coverage(state.requirements, state.evidence)
        if report.weighted_coverage >= config.target_coverage:
            return RunResult(state, report, "target_coverage")

        requirement = requirements[requirement_index % len(requirements)]
        requirement_index += 1
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
