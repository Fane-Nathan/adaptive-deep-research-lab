import asyncio

from deep_research_lab.controller import ControllerConfig
from deep_research_lab.experiment import compare_policies


def test_compare_policies_returns_same_budgeted_system() -> None:
    results = asyncio.run(
        compare_policies(
            "Are hyperbolic embeddings useful for hierarchical classification?",
            ControllerConfig(max_cost=6.0, target_coverage=0.99, min_marginal_gain=0.0, max_steps=6),
        )
    )

    assert [result.policy for result in results] == ["fixed", "adaptive"]
    assert all(result.spent_cost <= 6.0 for result in results)
    assert all(result.steps <= 6 for result in results)


def test_adaptive_policy_is_not_worse_on_mock_backend() -> None:
    fixed, adaptive = asyncio.run(
        compare_policies(
            "Compare two research methods",
            ControllerConfig(max_cost=8.0, target_coverage=0.99, min_marginal_gain=0.0, max_steps=8),
        )
    )

    assert adaptive.weighted_coverage >= fixed.weighted_coverage
    assert adaptive.coverage_per_cost >= fixed.coverage_per_cost
