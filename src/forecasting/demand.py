import numpy as np
import pandas as pd

def forecast_next_day(history, intervals=48):
    target=int((history.day.max()+1)%7); rows=[]
    for t in range(intervals):
        for q in history.queue.unique():
            for c in history.channel.unique():
                s=history[(history.interval==t)&(history.queue==q)&(history.channel==c)]
                same=s[s.dow==target].arrivals; recent=s.sort_values('day').tail(14).arrivals
                f1=float(same.mean()) if len(same) else (float(recent.mean()) if len(recent) else 0)
                f2=float(recent.mean()) if len(recent) else f1
                rows.append(dict(interval=t,queue=q,channel=c,forecast_arrivals=max(0,.7*f1+.3*f2),aht_seconds=float(s.aht_seconds.tail(30).mean())))
    return pd.DataFrame(rows)

def erlang_c(n, lam, aht):
    if n<=0:return 1.
    mu=3600/max(aht,1); a=lam/mu
    if a>=n:return 1.
    term=1.; total=1.
    for k in range(1,n+1): term*=a/k; total+=term
    return (term*n/(n-a))/total

def sla_for_agents(n, arrivals_30m, aht, target_seconds=20):
    if arrivals_30m<=0:return 1.
    lam=arrivals_30m*2; mu=3600/max(aht,1); a=lam/mu
    if a>=n:return 0.
    pw=erlang_c(n,lam,aht); rate=max(n*mu-lam,1e-9)
    return 1-pw*np.exp(-rate*target_seconds/3600)

def required_agents(arrivals_30m,aht,target=.9):
    return next((n for n in range(1,101) if sla_for_agents(n,arrivals_30m,aht)>=target),100)

def build_staffing_requirements(forecast,target=.9):
    g=(forecast.assign(workload_hours=lambda x:x.forecast_arrivals*x.aht_seconds/3600).groupby('interval',as_index=False).agg(arrivals=('forecast_arrivals','sum'),workload_hours=('workload_hours','sum'),aht_seconds=('aht_seconds','mean')))
    g['required_agents']=[required_agents(r.arrivals,r.aht_seconds,target) for r in g.itertuples()]
    return g
