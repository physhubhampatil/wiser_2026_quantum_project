import numpy as np
import pandas as pd
QUEUES=['billing','technical','sales','retention']
CHANNELS=['voice','chat']

def generate_arrivals(days=90, intervals=48, seed=42):
    rng=np.random.default_rng(seed); rows=[]
    for day in range(days):
        dow=day%7
        for t in range(intervals):
            h=t*24/intervals
            shape=.30+.80*np.exp(-.5*((h-10.5)/2.8)**2)+1.10*np.exp(-.5*((h-16)/3)**2)+.35*np.exp(-.5*((h-19)/2.5)**2)
            if dow>=5: shape*=.65
            shock=rng.uniform(1.25,1.7) if rng.random()<.025 else 1
            for qi,q in enumerate(QUEUES):
                for c in CHANNELS:
                    lam=28*shape*[1,.82,.68,.45][qi]*(1 if c=='voice' else .52)*shock*rng.lognormal(0,.1)
                    base={'billing':360,'technical':520,'sales':410,'retention':600}[q]*(.8 if c=='chat' else 1)
                    rows.append(dict(day=day,dow=dow,interval=t,hour=h,queue=q,channel=c,arrivals=int(rng.poisson(max(lam,.1))),aht_seconds=max(90,rng.normal(base,.12*base))))
    return pd.DataFrame(rows)

def generate_employees(n=16, seed=42):
    rng=np.random.default_rng(seed); rows=[]
    for i in range(n):
        skills=rng.choice(QUEUES,size=int(rng.integers(1,4)),replace=False)
        hourly=float(rng.uniform(18,32))
        rows.append(dict(employee=f'E{i+1:03d}',skills=','.join(skills),preferred_start=int(rng.choice(range(6,15))),hourly_cost=hourly,overtime_cost=hourly*rng.uniform(1.5,2),preference=float(rng.uniform(.5,1)),max_overtime_hours=2.0))
    return pd.DataFrame(rows)

def generate_shifts():
    return pd.DataFrame([dict(shift=f'S{i:02d}',start_hour=h,end_hour=h+8,regular_hours=8.0,break_hours=.5) for i,h in enumerate(range(6,15),1)])
