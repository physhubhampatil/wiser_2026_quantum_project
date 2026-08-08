def solve_cpsat(data):
    from ortools.sat.python import cp_model
    M=cp_model.CpModel(); E=data.employees; S=data.shifts; R=data.requirements.set_index('interval')
    x={(e,s):M.NewBoolVar(f'x_{e}_{s}') for e in E.employee for s in S.shift}
    ot={e:M.NewBoolVar(f'ot_{e}') for e in E.employee}
    for e in E.employee:
        M.Add(sum(x[e,s] for s in S.shift)<=1)
        M.Add(ot[e] <= sum(x[e,s] for s in S.shift))
    for t,row in R.iterrows():
        cov=[]
        for e in E.employee:
            for s in S.itertuples():
                hour=float(t)*.5; br=int((s.start_hour+4)*2)
                if s.start_hour<=hour<s.end_hour and int(t)!=br: cov.append(x[e,s.shift])
                if s.end_hour<=hour<s.end_hour+data.max_overtime_hours: cov.append(ot[e])
        M.Add(sum(cov)>=int(row.required_agents))
    Ei=E.set_index('employee'); obj=[]
    for e in E.employee:
        for s in S.itertuples(): obj.append(int(round(Ei.loc[e,'hourly_cost']*s.regular_hours*100))*x[e,s.shift])
        obj.append(int(round(Ei.loc[e,'overtime_cost']*data.max_overtime_hours*100))*ot[e])
    M.Minimize(sum(obj)); solver=cp_model.CpSolver(); solver.parameters.max_time_in_seconds=30; status=solver.Solve(M)
    selected=[k for k,v in x.items() if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) and solver.Value(v)]
    overtime=[e for e,v in ot.items() if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) and solver.Value(v)]
    return {'selected':selected,'overtime':overtime,'objective':solver.ObjectiveValue()/100,'status':solver.StatusName(status)}
