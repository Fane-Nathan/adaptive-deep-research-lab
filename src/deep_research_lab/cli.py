from __future__ import annotations

import argparse
import asyncio

from .controller import ControllerConfig, run_adaptive_research
from .mock_backend import MockResearchBackend
from .planner import default_plan
from .report import render_markdown_report


async def _run(query: str) -> None:
    requirements = default_plan(query)
    result = await run_adaptive_research(
        query,
        requirements,
        MockResearchBackend(),
        ControllerConfig(max_cost=10.0, target_coverage=0.75),
    )
    print(render_markdown_report(result.state))
    print(f"\nStop reason: {result.stop_reason}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Adaptive Deep Research Lab MVP")
    parser.add_argument("query", help="Research question")
    args = parser.parse_args()
    asyncio.run(_run(args.query))


if __name__ == "__main__":
    main()
