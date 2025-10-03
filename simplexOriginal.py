#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:10:13 2024

@author: j-ponteil
"""

import numpy as np
from scipy.optimize import linprog
#import math

#define the numerical values of the system parameters
Pa=280
Ps=25
Poff=90
Pon=90
c=10
#c_vec=[10,12,10,12,10,12,10,12,10,12]
t=10
toff=3
ton=3
def consumed_energy(x,y):
    return sum([t*Pa*x[i]*y[i] + t*Ps*(1-x[i])*(1-y[i]) + toff*Poff*(1-x[i])*y[i] + (t-toff)*Ps*(1-x[i])*y[i] + 
                ton*Pon*(1-y[i])*x[i] + (t-ton)*Pa*(1-y[i])*x[i] for i in range(n)])

def LP(n,alpha,y):
    
    c_vec = [c]*n
    LOAD=n*c*t*alpha
    # Problem data
    weights_obj = [t*Pa*y[i] - t*Ps*(1-y[i]) - toff*Poff*y[i] - (t-toff)*Ps*y[i] + ton*Pon*(1-y[i]) + (t-ton)*Pa*(1-y[i]) for i in range(n)]#Coefficients for the objective function
    weights_cons = [[(ton-t)*10*(1-y[i]) - t*10*y[i] for i in range(n)]]#Coefficient vector for a single constraint
    Clim = [-LOAD]            # Right-hand side of the inequality
    
    
    # Bounds for each variable (non-negative constraints)
    x_bounds = x_bounds = [(0, 1)] * n
    
    # Solve the problem using the simplex method
    result = linprog(weights_obj, A_ub=weights_cons, b_ub=Clim, bounds=x_bounds, method='simplex')
    
    print(f"Optimal x: {result.x}")
    new_y = result.x
    
    print("New activation profile:",new_y)
    
    # Output the results
    print(f"Optimal value: {result.fun}")
    res = consumed_energy(x=new_y, y=y)
    print("New-y optimal value:", res)
    print(f"Optimal value: {result.fun}")

    
    constraint_value = np.sum([t * c_vec[i] * new_y[i] * y[i] +
    (t - ton) * c_vec[i] * (1 - y[i]) * new_y[i] for i in range(n)])
    print("Constraint value:", constraint_value)
    
    
    
    return new_y, res, constraint_value,

OSimplexobj = []
OSimplexcons = []
OSimplexactiveservers = []
OSimplexhistory = []

n=5
ALPHA = np.arange(0,1,.01)
y = [1]*n

for i in range(len(ALPHA)):
    run = LP(n=n,alpha=ALPHA[i], y=y)
    
    
    y = run[0]
    
    OSimplexhistory.append(y)
    OSimplexactiveservers.append(np.sum(y))
    
    OSimplexobj.append(run[1])
    OSimplexcons.append(run[2] - n*c*t*ALPHA[i])

    