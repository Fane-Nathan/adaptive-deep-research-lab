import asyncio

from deep_research_lab.controller import ControllerConfig, run_adaptive_research
from deep_research_lab.mock_backend import MockResearchBackend
from deep_research_lab.planner import default_plan


def test_adaptive_controller_improves_coverage() -> None:
    async def run():
        query = "test query"
        result = await run_adaptive_research(
            query,
            default_plan(query),
            MockResearchBackend(),
            ControllerConfig(max_cost=8.0, target_coverage=0.70, min_marginal_gain=0.0),
        )
        return result

    result = asyncio.run(run())
    assert result.coverage.weighted_coverage > 0.0
    assert result.state.steps > 0
    assert result.state.spent_cost <= 8.0
