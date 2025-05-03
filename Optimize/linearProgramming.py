""" 
- minimize a cost function c1x1 + c2x2 + ....+ cnxn
- with constrainst of form a1x1+a2x2+..+anxn <= b or of form a1x1+a2x2+...+anxn = b
- with bounds for each variable li <= xi <= ui

Example: 
Condition 1: Two machines x1 and x2
x1 = $50/hour
x2 = $80/hour
GOAL: minimize cost

Condition 2:
x1 requires 5 units of labor/hour
x2 requires 2 units of labor/hour

Total of 20 units of labor to spend

Condition 3: 
x1 produces 10 units of output/hour
x2 produces 12 units of output/hour

Company needs 90 units of output

Cost function: 50x1 + 80x2
Constraint1: 5x1 + 2x2 <= 20
Constraint2: 10x1 + 90x2 >= 90
(-10x1) + (-12x2) <= -90
"""
import scipy

result = scipy.optimize.linprog(
    [50,80],
    A_ub = [[5,2], [-10,-12]],
    b_ub = [20, -90],
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")

else:
    print("No solutions")