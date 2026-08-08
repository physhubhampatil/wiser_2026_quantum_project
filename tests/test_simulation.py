from src.data.synthetic import generate_arrivals,generate_shifts
from src.forecasting.demand import forecast_next_day
from src.simulation.queue import staffing_series,simulate

def test_sim():
    h=generate_arrivals(10,4); f=forecast_next_day(h,4); m=simulate(f,staffing_series([('E001','S03')],generate_shifts(),4)); assert 0<=m['sla']<=1
