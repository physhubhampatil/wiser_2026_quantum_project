from src.data.synthetic import generate_arrivals,generate_employees,generate_shifts
from src.forecasting.demand import forecast_next_day,build_staffing_requirements
from src.optimization.problem import ProblemData,build_quadratic_program
from src.optimization.qubo import to_qubo

def test_qubo():
    h=generate_arrivals(10,4); E=generate_employees(4); S=generate_shifts(); R=build_staffing_requirements(forecast_next_day(h,4)); qp=build_quadratic_program(ProblemData(E,S,R)); q=to_qubo(qp); assert q.qubo_problem.get_num_linear_constraints()==0
