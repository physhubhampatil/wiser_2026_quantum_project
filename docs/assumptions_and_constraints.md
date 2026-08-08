# Assumptions and constraints

- Synthetic data only.
- 90-day historical dataset by default.
- 48 half-hour planning intervals.
- 8-hour candidate shifts.
- One 30-minute break per shift.
- One regular shift per employee.
- Employees have one or more queue skills.
- Maximum overtime is 2 hours in the extended model.
- Default SLA target is 90% within 20 seconds.
- Erlang-C converts workload to staffing requirement.
- Queue simulator is a transparent prototype, not a production WFM engine.
- SLA is hard-validated before comparing cost.
