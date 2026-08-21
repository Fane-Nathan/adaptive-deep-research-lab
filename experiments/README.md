# Experiments

The first experiment isolates **research allocation policy** while keeping the rest of the system fixed.

| Variant | Planner | Search allocation | Coverage-aware | Stop policy |
|---|---|---|---|---|
| A | deterministic | round-robin | no | coverage/budget/marginal gain |
| B | deterministic | weakest-gap | yes | coverage/budget/marginal gain |
| C | LLM | weakest-gap | yes | coverage/budget |
| D | LLM | expected utility | yes | marginal utility |

## Experiment 001 — fixed vs adaptive allocation

The controlled variables are:

- same query
- same information requirements
- same mock research backend
- same evidence schema
- same evidence aggregation
- same maximum cost
- same maximum steps
- same target coverage
- same marginal-gain stop threshold

The only independent variable is **which requirement is researched next**.

Primary metrics:

- weighted coverage
- total research cost
- number of steps
- evidence count
- coverage per unit cost
- stop reason

Run the comparison from Python:

```python
import asyncio

from deep_research_lab.controller import ControllerConfig
from deep_research_lab.experiment import compare_policies, write_csv, write_json

results = asyncio.run(
    compare_policies(
        "Are hyperbolic embeddings useful for hierarchical classification?",
        ControllerConfig(max_cost=10.0, min_marginal_gain=0.0),
    )
)

write_csv(results, "results/experiment_001.csv")
write_json(results, "results/experiment_001.json")
```

Do not introduce a real LLM or web provider until this baseline comparison is stable and reproducible. Later experiments should change one component at a time whenever practical.
