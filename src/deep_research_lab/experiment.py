from __future__ import annotations

import asyncio
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .baseline import run_fixed_research
from .controller import ControllerConfig, RunResult, run_adaptive_research
from .mock_backend import MockResearchBackend
from .planner import default_plan


@dataclass(frozen=True)
class ExperimentResult:
    query: str
    policy: str
    weighted_coverage: float
    spent_cost: float
    steps: int
    evidence_count: int
    stop_reason: str

    @property
    def coverage_per_cost(self) -> float:
        return self.weighted_coverage / self.spent_cost if self.spent_cost else 0.0


def _summarize(query: str, policy: str, result: RunResult) -> ExperimentResult:
    return ExperimentResult(
        query=query,
        policy=policy,
        weighted_coverage=result.coverage.weighted_coverage,
        spent_cost=result.state.spent_cost,
        steps=result.state.steps,
        evidence_count=len(result.state.evidence),
        stop_reason=result.stop_reason,
    )


async def compare_policies(
    query: str,
    config: ControllerConfig = ControllerConfig(),
) -> list[ExperimentResult]:
    requirements = default_plan(query)

    fixed = await run_fixed_research(
        query,
        requirements,
        MockResearchBackend(),
        config,
    )
    adaptive = await run_adaptive_research(
        query,
        requirements,
        MockResearchBackend(),
        config,
    )

    return [
        _summarize(query, "fixed", fixed),
        _summarize(query, "adaptive", adaptive),
    ]


async def run_suite(
    queries: list[str],
    config: ControllerConfig = ControllerConfig(),
) -> list[ExperimentResult]:
    nested = await asyncio.gather(*(compare_policies(query, config) for query in queries))
    return [result for pair in nested for result in pair]


def write_json(results: list[ExperimentResult], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            **asdict(result),
            "coverage_per_cost": result.coverage_per_cost,
        }
        for result in results
    ]
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(results: list[ExperimentResult], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "query",
        "policy",
        "weighted_coverage",
        "spent_cost",
        "steps",
        "evidence_count",
        "stop_reason",
        "coverage_per_cost",
    ]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    **asdict(result),
                    "coverage_per_cost": result.coverage_per_cost,
                }
            )
