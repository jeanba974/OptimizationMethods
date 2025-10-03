#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:14:53 2024

@author: j-ponteil
"""

import pulp
import numpy as np

n=5
n1 = n
n2 = n - n1

C=10
T=60
Ton = 3
Toff = 3


Pa=280
Ps=25
Poff=90
Pon=90

#the piecewise linear function E(x|y=1) is defined as max(a1x+b1,a2x+b2)
a1=Pa-Ps
a2=Pa-Poff

b1=Toff*Poff + (T-Toff)*Ps
b2=T*Poff

#the piecewise linear function E(x|y=0) is defined as max(c1x+d1,c2x+d2)
c1=Ps-Pa
c2=Ps-Pon

d1=Ton*Pon + Pa*(T-Ton)
d2=T*Pon

threshold = T-Toff



def realLP(L,n1,n2):
    
    #M is the big factor for the linearisation of the constraint
    #big_M=1000

    #OUTPUT
    new_n1 = n1
    new_n2 = n2
    #store the decision of time to sleep/awake for all servers
    adecision = np.zeros(n1)
    sdecision = np.zeros(n2)
    
    #values = np.zeros(n1)
    #store the state of each server
    #from 1 to new_n1, active servers, from new_n1+1 to new_n1+new_n2, asleep servers
    active_DUs = np.zeros(n)
    energy = 0
    cons = 0

    prob = pulp.LpProblem("Optimization_Problem", pulp.LpMinimize)
    
    x = [pulp.LpVariable(f"x_{i+1}", cat='Continuous') for i in range(n1)]
    y = [pulp.LpVariable(f"y_{i+1}", cat='Continuous') for i in range(n2)]
    t = [pulp.LpVariable(f"t_{i+1}", cat='Continuous') for i in range(n1)]
    u = [pulp.LpVariable(f"u_{i+1}", cat='Continuous') for i in range(n2)]
    
    #f = [pulp.LpVariable(f"f_{i}") for i in range(n1)]
    #delta = [pulp.LpVariable(f"delta_{i}", cat="Binary") for i in range(n1)]
    

    
    
    
    
    obj_expr = pulp.lpSum(
        t[i] for i in range(n1)
        ) + pulp.lpSum(
            u[i] for i in range(n2)
            )
    
    prob += obj_expr
    
    for i in range(n1):
        prob += x[i] >= 0
    for i in range(n1):
        prob += x[i] <= T-Toff
        
    for i in range(n2):
        prob += y[i] >= 0
    for i in range(n2):
        prob += y[i] <= T-Ton
    
    for i in range(n1):
        prob += a1*x[i] + b1 <= t[i]
    for i in range(n1):
        prob += a2*x[i] + b2 <= t[i]
    for i in range(n2):
        prob += c1*y[i] + d1 <= u[i]
    for i in range(n2):
        prob += c2*y[i] + d2 <= u[i]
     
        
     
        
    #linearisation of the discontinuous constraint function f(x_i)=x_i or T
    # Constraints to enforce f(x_i) = x_i for x_i < T-T' and f(x_i) = T for x_i = T-T'
    # for i in range(n1):
    #     #when delta_i = 0, f(x_i) = x_i
    #     prob += f[i] <= x[i] + big_M * delta[i], f"Constraint1_{i}"
    #     prob += f[i] >= x[i] - big_M * delta[i], f"Constraint2_{i}"
        
    #     #when delta_i = 1, f(x_i) = T
    #     prob += f[i] <= T + big_M * (1 - delta[i]), f"Constraint3_{i}"
    #     prob += f[i] >= T - big_M * (1 - delta[i]), f"Constraint4_{i}"
    
    #     # Ensure delta switches based on x_i value
    #     prob += x[i] <= threshold + big_M * delta[i], f"Constraint5_{i}"  # If delta_i = 0, x_i <= T - T'
    #     prob += x[i] >= threshold - big_M * (1 - delta[i]), f"Constraint6_{i}"  # If delta_i = 1, x_i = T - T'


    
    prob += pulp.lpSum(x[i]*T/(T-Toff) for i in range(n1)) + pulp.lpSum(T-Ton-y[i] for i in range(n2)) >= L/C
    
    
            
    glpk_solver = pulp.GLPK()
    prob.solve(glpk_solver)
    
    for i in range(n1):
        if x[i].value() < T - Toff:
            #binary_decision[i] = 0
            new_n1 -= 1
            new_n2 += 1
            energy += Toff*Poff + x[i].value()*Pa + (T-Toff-x[i].value())*Ps
            cons += x[i].value()*C
            
            active_DUs[i] = (x[i].value())/T
        else:
            #binary_decision[i] = 1
            energy += T*Pa
            cons += T*C
            
            active_DUs[i] = 1
    
    for i in range(n2):
        if y[i].value() < T - Ton:
            #binary_decision[n1+i] = 1
            new_n1 += 1
            new_n2 -= 1
            energy += Ps*y[i].value() + Ton*Pon + Pa*(T-Ton-y[i].value())
            cons += (T-Ton-y[i].value())*C
            
            active_DUs[n1+i] = (T-Ton-y[i].value())/T
        else:
            #binary_decision[n1+i] = 0
            energy += T*Ps
            cons += 0
            
            active_DUs[n1+i] = 0
        
    for i in range(n1):
        adecision[i] = x[i].value()
        #values[i] = f[i].value()
        print("the active server goes to sleep at ", x[i].value())
    for i in range(n2):
        sdecision[i] = y[i].value()
        print("the sleeping server wakes up at ", y[i].value())
        

            
    return new_n1, new_n2, adecision, sdecision, active_DUs, energy, cons

ALPHA = np.arange(0,1,.01)


realLPobj = []
realLPcons=[]
realLPsleepToactive=[]
realLPactiveTosleep=[]

realLPservers=[]



for i in range(len(ALPHA)):
    alpha = ALPHA[i]
    L = n*C*T*ALPHA[i]
    
    linear = realLP(L=L,n1=n1,n2=n2)
    
    n1=linear[0]
    n2=linear[1]
    
    realLPobj.append(linear[5])
    realLPcons.append(linear[6]-n*C*T*ALPHA[i])
    
    realLPservers.append(sum(linear[4]))
    
    realLPsleepToactive.append(linear[3])
    realLPactiveTosleep.append(linear[2])
    
