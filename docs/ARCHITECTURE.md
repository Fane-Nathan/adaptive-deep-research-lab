# Architecture Notes

## Research hypothesis

A research controller that explicitly models information requirements and evidence coverage should allocate additional searches more efficiently than a fixed-depth loop.

## Canonical objects

- `InformationRequirement`: one dimension of information needed for a satisfactory answer.
- `Evidence`: one claim/source observation mapped to one or more requirements.
- `ResearchState`: accumulated evidence, cost, and steps.
- `CoverageReport`: per-requirement and weighted aggregate coverage.

## Initial controller policy

1. Evaluate current coverage.
2. Pick the weakest requirement.
3. Spend one research action on that requirement.
4. Recompute coverage.
5. Stop on target coverage, budget exhaustion, max steps, or low marginal gain.

This policy is intentionally simple so it can serve as an interpretable baseline. Later experiments can replace step 2 with an expected-utility policy such as:

`U(action) = expected_coverage_gain / expected_cost`

and then add confidence, source diversity, contradiction resolution, and latency terms.

## Experiment roadmap

1. Mock deterministic backend — validate mechanics.
2. Real web search backend — compare fixed vs adaptive policies.
3. Academic backend — OpenAlex/Semantic Scholar plus PDF parsing.
4. Evidence verifier — claim/source entailment and contradiction labels.
5. Learned controller — contextual bandit or RL only after strong non-learned baselines exist.
