from dataclasses import dataclass
import pandas as pd

@dataclass
class ProblemData:
    employees: pd.DataFrame
    shifts: pd.DataFrame
    requirements: pd.DataFrame
    target_sla: float = .90
    max_overtime_hours: float = 2.0

def build_quadratic_program(data, preference_weight=10.0, resilience_weight=0.0, overtime_block_hours=2.0):
    """Build the binary workforce QuadraticProgram.

    x[e,s] = 1 when employee e works shift s.
    ot[e]  = 1 when employee e uses one overtime block (default 2 hours).

    The overtime variable is linked to a selected shift and is capped to one block,
    so the explicit maximum overtime is `max_overtime_hours`.
    """
    from qiskit_optimization import QuadraticProgram
    qp=QuadraticProgram('call_center_staffing'); E=data.employees; S=data.shifts
    for e in E.employee:
        for s in S.shift: qp.binary_var(f'x_{e}_{s}')
        qp.binary_var(f'ot_{e}')

    lin={}
    for e in E.itertuples():
        for s in S.itertuples():
            pref=e.preference-.03*abs(e.preferred_start-s.start_hour)
            lin[f'x_{e.employee}_{s.shift}']=e.hourly_cost*s.regular_hours-preference_weight*pref
        lin[f'ot_{e.employee}']=e.overtime_cost*overtime_block_hours
    qp.minimize(linear=lin)

    for e in E.employee:
        qp.linear_constraint({f'x_{e}_{s}':1 for s in S.shift},'<=',1,f'one_shift_{e}')
        qp.linear_constraint({f'ot_{e}':1, **{f'x_{e}_{s}':-1 for s in S.shift}}, '<=', 0, f'overtime_requires_shift_{e}')

    # Coverage. Overtime extends the selected shift by the configured overtime block.
    for t,row in data.requirements.set_index('interval').iterrows():
        coeff={}
        for e in E.itertuples():
            for s in S.itertuples():
                start=s.start_hour; end=s.end_hour
                break_t=int((start+4)*2)
                if start<=float(t)*.5<end and int(t)!=break_t:
                    coeff[f'x_{e.employee}_{s.shift}']=1
                # Overtime adds coverage after the regular shift, subject to no break.
                ot_start=end
                ot_end=end+data.max_overtime_hours
                if ot_start<=float(t)*.5<ot_end:
                    coeff[f'ot_{e.employee}']=coeff.get(f'ot_{e.employee}',0)+1
        qp.linear_constraint(coeff,'>=',int(row.required_agents),f'coverage_{int(t)}')
    return qp

def selected_pairs(qp_result):
    out=[]
    for v,x in zip(qp_result.variables,qp_result.x):
        if x>.5 and v.name.startswith('x_'):
            _,e,s=v.name.split('_',2); out.append((e,s))
    return out

def selected_overtime(qp_result):
    return [v.name.replace('ot_','') for v,x in zip(qp_result.variables,qp_result.x) if x>.5 and v.name.startswith('ot_')]
