# Mathematical formulation

Let E be employees, S candidate shifts, T half-hour intervals and G skill groups.

Binary decision:

\[x_{e,s}\in\{0,1\}\]

One shift per employee:

\[\sum_s x_{e,s}\le 1.\]

Coverage:

\[\sum_{e,s}a_{e,s,t,g}x_{e,s}\ge R_{t,g}.\]

Staffing cost:

\[C_{staff}=\sum_{e,s}c_{e,s}x_{e,s}.\]

Preference reward:

\[P=\sum_{e,s}p_{e,s}x_{e,s}.\]

The primary objective is:

\[\min(C_{staff}+C_{OT}-\lambda_P P+\lambda_R C_{resilience})\]

subject to shift, skill, break, overtime and service constraints.

The detailed queue is nonlinear, so Erlang-C translates forecast workload into required staffing before the discrete optimization. The selected schedule is then validated by stochastic queue simulation.
