
# Quantum Call Center Workforce Planner


### Team Name :- Quantum Maniac


### Team member :- Shubham Gajanan Patil



A complete hybrid Python + Qiskit workforce optimization prototype for the Call Center Staffing Optimization challenge.

## Challenge coverage

- Mathematical formulation with binary employee-shift variables, linear constraints and quadratic objective.
- QUBO conversion using Qiskit Optimization.
- Synthetic 90-day arrivals by time, queue and channel.
- Demand forecasting and Erlang-C staffing requirements.
- Shift rules, skills, breaks and maximum overtime representation.
- Queue simulation: ASA, abandonment, SLA and utilization.
- Manager controls for cost, service, employee preference and resilience.
- Classical OR-Tools CP-SAT baseline.
- Qiskit QAOA implementation using modern primitive-based APIs.
- Benchmarking and hard-constraint validation.
- Streamlit workforce planner with explanations.
- Presentation and demo script.

## Architecture

```text
Synthetic arrivals
      ↓
Demand forecast
      ↓
Erlang-C staffing requirement
      ↓
Binary workforce model
      ↓
Qiskit QuadraticProgram
      ↓
QUBO / Ising conversion
      ↓
Qiskit QAOA
      ↓
Recommended schedule
      ↓
Queue simulation
      ↓
SLA / ASA / abandonment / utilization
      ↓
Classical CP-SAT validation + benchmark
      ↓
Workforce co-pilot
```

## Competition objective

The scoring rule is modeled lexicographically:

1. Achieve `SLA >= target`.
2. Among feasible schedules, minimize regular staffing + overtime cost.
3. Use employee preference and resilience as secondary manager controls.

## Install

Python 3.11 is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Qiskit QAOA:

```bash
python -m src.pipeline --solver qaoa
```

Classical CP-SAT:

```bash
python -m src.pipeline --solver classical
```

Benchmark both:

```bash
python -m src.evaluation.benchmark
```

Launch prototype:

```bash
streamlit run app/streamlit_app.py
```

Tests:

```bash
pytest -q
```

## Qiskit design

The repository targets Qiskit 2.x and Qiskit Optimization 0.7.x. QAOA is implemented through `qiskit_optimization.minimum_eigensolvers.QAOA`, `MinimumEigenOptimizer`, `COBYLA`, and the V2 `StatevectorSampler` primitive.

Official references:
- Qiskit Optimization: https://qiskit-community.github.io/qiskit-optimization/
- QAOA API: https://qiskit-community.github.io/qiskit-optimization/stubs/qiskit_optimization.minimum_eigensolvers.QAOA.html
- MinimumEigenOptimizer: https://qiskit-community.github.io/qiskit-optimization/stubs/qiskit_optimization.algorithms.MinimumEigenOptimizer.html

## Important scientific claim

This project does not assume quantum advantage. QAOA is benchmarked against a classical CP-SAT solution and the final schedule is validated by queue simulation. The quantum layer demonstrates a genuine QUBO/QAOA workflow while the classical layers handle forecasting and stochastic operational validation.

## Quantum demonstration sizing

For a live QAOA demonstration, use a reduced candidate workforce (for example 4–8 employees and a small candidate-shift set) because QAOA on a local statevector simulator scales exponentially with qubit count. The complete workforce formulation remains available to the classical baseline. This mirrors the NISQ-era hybrid strategy: classical preprocessing and validation, quantum optimization on a compact discrete core.
