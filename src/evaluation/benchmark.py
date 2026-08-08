import os,time,pandas as pd
from src.data.synthetic import generate_arrivals,generate_employees,generate_shifts
from src.forecasting.demand import forecast_next_day,build_staffing_requirements
from src.optimization.problem import ProblemData,build_quadratic_program,selected_pairs
from src.optimization.classical import solve_cpsat
from src.optimization.qiskit_qaoa import solve_qaoa
from src.simulation.queue import staffing_series,simulate
from src.evaluation.metrics import summarize,validate

def run_benchmark(seed=42,target=.9):
    """Benchmark a compact quantum core against CP-SAT on exactly the same core.

    A compact instance is intentional: a local statevector QAOA demonstration cannot
    represent a full enterprise workforce model with hundreds of qubits. The full
    model is still available through `src.pipeline` and the classical baseline.
    """
    H=generate_arrivals(30,24,seed)
    E=generate_employees(4,seed)
    S=generate_shifts().iloc[[2,4,6]].reset_index(drop=True)
    F=forecast_next_day(H,24)
    R=build_staffing_requirements(F,target).copy()
    # Compact demonstrator requirement: 1–2 agents, preserving the temporal pattern.
    R['required_agents']=R['required_agents'].clip(1,2)
    D=ProblemData(E,S,R,target)
    rows=[]
    t=time.perf_counter(); c=solve_cpsat(D); ct=time.perf_counter()-t
    cm=simulate(F,staffing_series(c['selected'],S,24),seed)
    Ei=E.set_index('employee'); Si=S.set_index('shift')
    ccost=sum(Ei.loc[e,'hourly_cost']*Si.loc[s,'regular_hours'] for e,s in c['selected'])
    rows.append({'solver':'CP-SAT','runtime_seconds':ct,**summarize(cm,ccost),**validate(cm,target)})
    qp=build_quadratic_program(D); t=time.perf_counter(); q=solve_qaoa(qp,reps=1,maxiter=25,seed=seed); qt=time.perf_counter()-t
    qs=selected_pairs(q.result); qm=simulate(F,staffing_series(qs,S,24),seed)
    qcost=sum(Ei.loc[e,'hourly_cost']*Si.loc[s,'regular_hours'] for e,s in qs)
    rows.append({'solver':'QAOA','runtime_seconds':qt,'qubo_objective':q.result.fval,**summarize(qm,qcost),**validate(qm,target)})
    return pd.DataFrame(rows)

def main():
    os.makedirs('results',exist_ok=True); df=run_benchmark(); df.to_csv('results/benchmark.csv',index=False); print(df.to_string(index=False))
if __name__=='__main__':main()
