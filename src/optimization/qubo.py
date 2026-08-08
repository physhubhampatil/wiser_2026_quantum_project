from dataclasses import dataclass
@dataclass
class QUBOModel:
    original_problem:object
    qubo_problem:object
    penalty:float

def to_qubo(problem, penalty=1000.):
    from qiskit_optimization.converters import QuadraticProgramToQubo
    q=QuadraticProgramToQubo(penalty=penalty).convert(problem)
    return QUBOModel(problem,q,penalty)
