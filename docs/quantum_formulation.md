# Quantum formulation

Qiskit Optimization models the staffing problem as a `QuadraticProgram`. Its constraints are converted to penalty terms by `QuadraticProgramToQubo`.

For a coverage constraint, a penalty form is:

\[P(R_t-\sum_i a_{it}x_i)^2.\]

Expansion produces linear and quadratic binary terms because \(x_i^2=x_i\). The QUBO is mapped to an Ising Hamiltonian and supplied to QAOA.

The implementation uses modern Qiskit APIs:

```python
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.minimum_eigensolvers import QAOA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.optimizers import COBYLA
```

This avoids the deprecated `qiskit.algorithms` interface. The local statevector path is reproducible; an Aer SamplerV2 path is included for shot-based simulation.

## Overtime encoding

Each employee also has a binary `ot_e` variable. In the prototype, one overtime bit represents a two-hour overtime block and is constrained by:

\[
ot_e \leq \sum_s x_{e,s}.
\]

The objective charges the overtime rate for the block. Because the variable is binary, the model cannot exceed the configured two-hour block per employee.

## NISQ sizing

A full 48-interval workforce problem can contain many binary variables. For a near-term QAOA demonstration, reduce the employee and candidate-shift set so the QAOA circuit remains tractable on a local simulator. The full classical workforce planner can still use the complete candidate set. This is a modeling choice, not a claim of quantum advantage.
