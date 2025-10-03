# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import pulp
import numpy as np
import math

#define the numerical values of the system parameters
Pa=280
Ps=25
Pmicro=55
Poff=90
Pon=90
c=10
#c_vec=[10,12,10,12,10,12,10,12,10,12]
t=10
toff=3
ton=3

#n=10

#the load is defined as a fraction alpha of the total capacity of the system with all netfuncs active: n*c*t
#note that for very high load settings alpha can be greater than 1
#def load(n,alpha):
#    return n*c*t*alpha

def milp(n,alpha,x_prev):

    #this to address the case all network functions have the same capacity c,
    #note that we can construct c_vec in many different ways
    c_vec=[c]*n

#define and solve the milp problem P
    prob = pulp.LpProblem("Optimization_Problem", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(n)]

# Define the objective function
    obj_expr = pulp.lpSum(
        t * Pa * x[i] * x_prev[i] +
        t * Ps * (1 - x[i]) * (1 - x_prev[i]) +
        toff * Poff * (1 - x[i]) * x_prev[i] +
        (t - toff) * Ps * (1 - x[i]) * x_prev[i] +
        ton * Pon * (1 - x_prev[i]) * x[i] +
        (t - ton) * Pa * (1 - x_prev[i]) * x[i] for i in range(n)
    )

    prob += obj_expr

# define the constraint for the CU
    constraint_expr = pulp.lpSum(
        t * c_vec[i] * x[i] * x_prev[i] +
        (t - ton) * c_vec[i] * (1 - x_prev[i]) * x[i] for i in range(n)
    ) >= n*c*t*alpha
    
    prob += constraint_expr
    
#define the constraints for each DU
#    for l in range(k-1):
#        constraint_DU = pulp.lpSum(
#            t * c_vec[m-1] * x[m-1] * x_prev[m-1] +
#            (t - ton) * c_vec[m-1] * (1 - x_prev[m-1]) * x[m-1] for m in 
#            range(l*math.ceil(n/k)+1,(l+1)*math.ceil(n/k))
#            ) >= math.ceil(n/k)*c*t*alpha
#        prob += constraint_DU
    
#this to address the case when n is not multiple of k, the remainder/ remaining BBUs are added to the last 
#DU pool. E.g. we have n=11 BBUs in the CU and k=2 DUs, 5 in the first pool, and 6 in the second
#    last_constraint_DU = pulp.lpSum(
#        t * c_vec[m-1] * x[m-1] * x_prev[m-1] +
#        (t - ton) * c_vec[m-1] * (1 - x_prev[m-1]) * x[m-1] for m in range((k-1)*math.ceil(n/k)+1,n+1)
#        ) >= math.ceil(n/k)*c*t*alpha
#    prob += last_constraint_DU

    


#solve P

    prob.solve()

    # Print the solution
    print("Objective value:", pulp.value(prob.objective))
    obj = pulp.value(prob.objective)
    
    #print the constraints values to observe the margins
    constraint_value = np.sum([t * c_vec[i] * x[i].value() * x_prev[i] +
    (t - ton) * c_vec[i] * (1 - x_prev[i]) * x[i].value() for i in range(n)])
    print("Constraint value:", constraint_value)

    print("Lower limit:", n*c*t*alpha)
    lowerBound = n*c*t*alpha
    print("Margin:", constraint_value-lowerBound)
    
    #these are the constraints values at each DU (sub-group of BBUs)
    #constraints_DU = [np.sum([t * c_vec[m-1] * x[m-1].value() * x_prev[m-1] +
    #(t - ton) * c_vec[m-1] * (1 - x_prev[m-1]) * x[m-1].value() for m 
    #in range(l*math.ceil(n/k)+1,(l+1)*math.ceil(n/k))]) for l in range(k-1)]
    
    #constraints_DU += [np.sum(
    #    t * c_vec[m-1] * x[m-1].value() * x_prev[m-1] +
    #    (t - ton) * c_vec[m-1] * (1 - x_prev[m-1]) * x[m-1].value() 
    #    for m in range((k-1)*math.ceil(n/k)+1,n+1))]
    
    #print("DU constraints:",constraints_DU)
    #print("Margins:",[x-math.ceil(n/k)*c*t*alpha for x in constraints_DU])
    
    
    print("Optimal values for x:")
    for i in range(n):
        print(f"x_{i}:", x[i].value())
        x_prev[i] = x[i].value()
        
    return x_prev, obj, constraint_value#, constraints_DU



objmicro = []
consmicro = []
activeserversmicro = []
historymicro = []

n=5
ALPHA = np.arange(0,1,.01)
y = np.ones(n)

for i in range(len(ALPHA)):
    run = milp(n=n,alpha=ALPHA[i], x_prev=y)
    
    y = run[0]
    
    historymicro.append(y)
    
    
    
    waste = run[2] - n*c*t*ALPHA[i]
    
    savings = math.floor(waste/c)*(Pa-Pmicro)

    objmicro.append(run[1] - savings)
    
    consmicro.append(waste - c*math.floor(waste/c))
    
    activeserversmicro.append(np.sum(y) - math.floor(waste/c)/t)


