import argparse,json,os
from src.data.synthetic import generate_arrivals,generate_employees,generate_shifts
from src.forecasting.demand import forecast_next_day,build_staffing_requirements
from src.optimization.problem import ProblemData,build_quadratic_program,selected_pairs,selected_overtime
from src.optimization.qiskit_qaoa import solve_qaoa
from src.optimization.classical import solve_cpsat
from src.simulation.queue import staffing_series,simulate
from src.evaluation.metrics import summarize,validate

def run(solver='qaoa',days=30,employees_n=8,target=.9,seed=42):
    H=generate_arrivals(days,48,seed); E=generate_employees(employees_n,seed); S=generate_shifts(); F=forecast_next_day(H); R=build_staffing_requirements(F,target); D=ProblemData(E,S,R,target)
    if solver=='classical': cr=solve_cpsat(D); selected=cr['selected']; overtime=cr.get('overtime',[]); backend='OR-Tools CP-SAT'; qenergy=None
    else:
        qp=build_quadratic_program(D); qr=solve_qaoa(qp,reps=1,maxiter=25,seed=seed); selected=selected_pairs(qr.result); overtime=selected_overtime(qr.result); backend=qr.backend; qenergy=float(qr.result.fval)
    staff=staffing_series(selected,S); metrics=simulate(F,staff,seed); req=R.set_index('interval').required_agents; under=[int(r.interval) for r in staff.itertuples() if r.agents<req.get(r.interval,0)]
    Ei=E.set_index('employee'); Si=S.set_index('shift'); cost=sum(float(Ei.loc[e,'hourly_cost'])*float(Si.loc[s,'regular_hours']) for e,s in selected)
    overtime_cost=sum(float(Ei.loc[e,'overtime_cost'])*float(D.max_overtime_hours) for e in overtime)
    metrics=summarize(metrics,cost,overtime_cost)
    return {'solver':backend,'selected':selected,'overtime_employees':overtime,'selected_count':len(selected),'staffing':staff,'requirements':R,'forecast':F,'metrics':metrics,'validation':validate(metrics,target),'understaffed_intervals':under,'qubo_energy':qenergy}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--solver',choices=['qaoa','classical'],default='qaoa'); p.add_argument('--days',type=int,default=30); p.add_argument('--employees',type=int,default=8); p.add_argument('--target-sla',type=float,default=.9); a=p.parse_args(); r=run(a.solver,a.days,a.employees,a.target_sla)
    os.makedirs('results',exist_ok=True); r['staffing'].to_csv('results/staffing_schedule.csv',index=False); r['requirements'].to_csv('results/staffing_requirements.csv',index=False); print(json.dumps({k:v for k,v in r.items() if k not in ['staffing','requirements','forecast']},default=str,indent=2))
if __name__=='__main__':main()
