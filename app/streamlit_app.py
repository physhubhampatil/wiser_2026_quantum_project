import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd, plotly.express as px, streamlit as st
from src.pipeline import run
from src.utils.explain import explain
st.set_page_config(page_title='Quantum Workforce Planner',layout='wide')
st.title('📞 Quantum Call Center Workforce Planner')
st.caption('Forecast → QUBO → Qiskit QAOA → queue validation')
with st.sidebar:
    target=st.slider('Target SLA',.80,.99,.90,.01); cost=st.slider('Cost priority',0,100,70); service=st.slider('Service priority',0,100,90); preference=st.slider('Employee preference',0,100,50); resilience=st.slider('Resilience',0,100,60); n=st.slider('Available employees',8,16,8); solver=st.selectbox('Backend',['qaoa','classical']); go=st.button('Optimize schedule',type='primary')
if go or 'r' not in st.session_state: st.session_state.r=run(solver,30,n,target)
r=st.session_state.r; m=r['metrics']; c=st.columns(6)
for col,label,val in zip(c,['SLA','ASA','Abandonment','Utilization','Total cost','Breaches'],[f"{m['sla']:.1%}",f"{m['asa_seconds']:.1f}s",f"{m['abandonment_rate']:.1%}",f"{m['utilization']:.1%}",f"{m['total_cost']:,.0f}",str(r['validation']['hard_constraint_breaches'])]):col.metric(label,val)
st.subheader('Recommended staffing vs requirement')
d=r['staffing'].merge(r['requirements'][['interval','required_agents']],on='interval').melt('interval',value_vars=['agents','required_agents'],var_name='series',value_name='agents_count'); st.plotly_chart(px.line(d,x='interval',y='agents_count',color='series',markers=True),use_container_width=True)
st.subheader('Selected shifts'); st.dataframe(pd.DataFrame(r['selected'],columns=['employee','shift']),use_container_width=True)
st.subheader('Understaffed intervals'); st.warning(str(r['understaffed_intervals']) if r['understaffed_intervals'] else 'None')
st.subheader('Service-versus-cost explanation')
for x in explain(m,target,m['staffing_cost'],r['understaffed_intervals'],len(r['selected']),{'cost':cost,'service':service,'preference':preference,'resilience':resilience}):st.write('•',x)
