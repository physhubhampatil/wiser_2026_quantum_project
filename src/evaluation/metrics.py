def validate(metrics,target):
    return {'sla_met':metrics['sla']>=target,'hard_constraint_breaches':0 if metrics['sla']>=target else 1}

def summarize(metrics,cost,overtime=0):
    return {**metrics,'staffing_cost':float(cost),'overtime_cost':float(overtime),'total_cost':float(cost+overtime)}
