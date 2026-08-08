def explain(metrics,target,cost,understaffed,selected_count,controls):
    out=[]
    out.append(f"Projected SLA is {metrics['sla']:.1%} versus the {target:.1%} target.")
    out.append(f"The recommended schedule uses {selected_count} employee-shifts and costs {cost:,.0f} in synthetic cost units.")
    out.append(f"{len(understaffed)} intervals are below the forecast requirement." if understaffed else 'No interval is below the modeled forecast requirement.')
    if metrics['utilization']>.9: out.append('Utilization is high; increasing resilience priority would add capacity around peaks.')
    elif metrics['utilization']<.65: out.append('Utilization is low; increasing cost priority could reduce excess capacity.')
    else: out.append('Utilization is moderate, balancing service and capacity.')
    if controls.get('preference',0)>70:out.append('High employee-preference priority trades some cost for preferred shifts.')
    if controls.get('resilience',0)>70:out.append('High resilience priority preserves additional capacity against forecast error.')
    return out
