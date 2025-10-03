#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:02:30 2024

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
    energy=0
    cons=0
    
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
    new_y = []
    
    for i in range(len(y)):
        if y[i] == 1:
            if result.x[i] < (t-toff)/t:
                new_y.append(0)
                energy += toff*Poff + result.x[i]*t*Pa + (t-toff-result.x[i]*t)*Ps
                cons += result.x[i]*t*c
            else:
                new_y.append(1)
                energy += t*Pa
                cons += t*c
                
        elif y[i] == 0:
            if result.x[i] == 0:
                new_y.append(0)
            elif result.x[i] < (t-ton)/t:
                new_y.append(1)
                energy += Ps*(t-ton-result.x[i]*t) + ton*Pon + Pa*result.x[i]*t
                cons += result.x[i]*t*c
            else:
                new_y.append(0)
                energy += t*Ps
                cons += 0
                
                
    print("new optimal x:", new_y)

    
    
    
    return new_y, energy, cons

eSimplexobj = []
eSimplexcons = []
eSimplexactiveservers = []
eSimplexhistory = []

n=5
ALPHA = np.arange(0,1,.01)
y = [1]*n

for i in range(len(ALPHA)):
    run = LP(n=n,alpha=ALPHA[i], y=y)
    
    
    y = run[0]
    
    eSimplexhistory.append(y)
    eSimplexactiveservers.append(np.sum(y))
    
    eSimplexobj.append(run[1])
    eSimplexcons.append(run[2] - n*c*t*ALPHA[i])

    