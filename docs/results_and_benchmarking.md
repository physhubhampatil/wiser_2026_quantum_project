# Results and benchmarking

Run:

```bash
python -m src.evaluation.benchmark
```

The script writes `results/benchmark.csv`.

The final competition comparison must prioritize feasibility:

1. SLA >= target.
2. Lowest staffing + overtime cost among feasible schedules.
3. Report ASA, abandonment, utilization, understaffing and runtime as supporting metrics.

Do not claim quantum advantage unless the benchmark supports it.
