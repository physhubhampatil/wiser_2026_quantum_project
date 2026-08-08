from collections import deque
import numpy as np
import pandas as pd

def staffing_series(selected,shifts,intervals=48):
    S=shifts.set_index('shift'); rows=[]
    for t in range(intervals):
        n=0
        for e,s in selected:
            start=int(S.loc[s,'start_hour']); end=int(S.loc[s,'end_hour']); br=int((start+4)*2)
            if start<=t*.5<end and t!=br:n+=1
        rows.append({'interval':t,'agents':n})
    return pd.DataFrame(rows)

def simulate(forecast,staffing,seed=42,service_seconds=20):
    rng=np.random.default_rng(seed); d=forecast.groupby('interval',as_index=False).agg(expected_arrivals=('forecast_arrivals','sum'),aht_seconds=('aht_seconds','mean')).merge(staffing,on='interval',how='left').fillna({'agents':0})
    q=deque(); waits=[]; answered=abandoned=arrivals=busy=0
    for r in d.itertuples():
        n=int(rng.poisson(max(r.expected_arrivals,0))); arrivals+=n
        q.extend([(r.interval,r.aht_seconds)]*n)
        cap=int(r.agents*1800/max(r.aht_seconds,1))
        for _ in range(min(cap,len(q))):
            at,aht=q.popleft(); waits.append(max(0,(r.interval-at)*1800)); answered+=1; busy+=aht
        rem=deque()
        while q:
            at,aht=q.popleft()
            if r.interval-at>=2:abandoned+=1
            else:rem.append((at,aht))
        q=rem
    w=np.asarray(waits,float); asa=float(w.mean()) if len(w) else 0.; sla=float((w<=service_seconds).mean()) if len(w) else 1.; util=min(busy/max(float(d.agents.sum()*1800),1),1)
    return {'arrivals':arrivals,'answered':answered,'abandoned':abandoned,'asa_seconds':asa,'sla':sla,'abandonment_rate':abandoned/max(arrivals,1),'utilization':util}
