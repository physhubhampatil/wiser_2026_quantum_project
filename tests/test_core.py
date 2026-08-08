from src.data.synthetic import generate_arrivals,generate_employees,generate_shifts
from src.forecasting.demand import forecast_next_day,build_staffing_requirements

def test_data():
    d=generate_arrivals(2,4); assert len(d)>0
    assert len(generate_employees(5))==5
    assert len(generate_shifts())==9

def test_forecast():
    h=generate_arrivals(14,8); f=forecast_next_day(h,8); r=build_staffing_requirements(f); assert len(r)==8
