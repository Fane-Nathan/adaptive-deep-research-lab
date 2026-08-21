from deep_research_lab.coverage import evaluate_coverage
from deep_research_lab.models import Evidence, InformationRequirement


def test_duplicate_source_does_not_double_count() -> None:
    reqs = [InformationRequirement("a", "A")]
    evidence = [
        Evidence("1", "claim 1", "source-x", ("a",), 0.5),
        Evidence("2", "claim 2", "source-x", ("a",), 0.8),
    ]
    report = evaluate_coverage(reqs, evidence)
    assert report.by_requirement["a"] == 0.8


def test_independent_sources_accumulate() -> None:
    reqs = [InformationRequirement("a", "A")]
    evidence = [
        Evidence("1", "claim 1", "source-x", ("a",), 0.5),
        Evidence("2", "claim 2", "source-y", ("a",), 0.5),
    ]
    report = evaluate_coverage(reqs, evidence)
    assert report.by_requirement["a"] == 0.75
