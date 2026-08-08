from dataclasses import dataclass
@dataclass
class QuantumResult:
    result:object
    backend:str
    qubits:int

def solve_qaoa(problem,reps=1,maxiter=50,seed=42):
    from qiskit.primitives import StatevectorSampler
    from qiskit_optimization.minimum_eigensolvers import QAOA
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    from qiskit_optimization.optimizers import COBYLA
    sampler=StatevectorSampler(seed=seed)
    qaoa=QAOA(sampler=sampler,optimizer=COBYLA(maxiter=maxiter),reps=reps)
    result=MinimumEigenOptimizer(qaoa).solve(problem)
    return QuantumResult(result,'QAOA + StatevectorSampler',problem.get_num_vars())

def solve_qaoa_aer(problem,reps=1,maxiter=50,seed=42,shots=1024):
    from qiskit_aer.primitives import SamplerV2
    from qiskit_optimization.minimum_eigensolvers import QAOA
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    from qiskit_optimization.optimizers import COBYLA
    sampler=SamplerV2(options={'run_options':{'shots':shots,'seed':seed}})
    qaoa=QAOA(sampler=sampler,optimizer=COBYLA(maxiter=maxiter),reps=reps)
    result=MinimumEigenOptimizer(qaoa).solve(problem)
    return QuantumResult(result,'QAOA + Aer SamplerV2',problem.get_num_vars())
