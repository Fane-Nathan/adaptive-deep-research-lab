# Experiments

Planned comparison:

| Variant | Planner | Search allocation | Coverage-aware | Stop policy |
|---|---|---|---|---|
| A | fixed | fixed | no | fixed steps |
| B | fixed | weakest-gap | yes | coverage/budget |
| C | LLM | weakest-gap | yes | coverage/budget |
| D | LLM | expected utility | yes | marginal utility |

Keep the LLM, search provider, query set, and budget fixed when comparing controller policies.
