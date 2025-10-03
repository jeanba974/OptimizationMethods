#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:54:56 2024

@author: j-ponteil
"""

import numpy as np
n=5

C=10
T=140
Toff=25
Ton=25
Pa=280
Ps=1
Poff=90
Pon=90



def cap(x,y):
    cap = sum([T*C*x[i]*y[i]+(T-Ton)*C*(1-y[i])*x[i] for i in range(n)])
    return cap

def consumed_energy(x,y):
    return sum([T*Pa*x[i]*y[i] + T*Ps*(1-x[i])*(1-y[i]) + Toff*Poff*(1-x[i])*y[i] + (T-Toff)*Ps*(1-x[i])*y[i] + 
                Ton*Pon*(1-y[i])*x[i] + (T-Ton)*Pa*(1-y[i])*x[i] for i in range(n)])


def heuristic_add(input,L):
    x=[]
    x[:]=input
    pos=int(sum(input))

    if L==0:
        x = np.zeros(n)

    
    else:
        while cap(x,input)<L:
            x[pos]=1
            pos+=1

    return x


def heuristic_remove(input,L):
    x=[]
    x[:]=input
    pos=int(sum(input))

    if L==0:
        x = np.zeros(n)
        
    else:
        while cap(x,input)>=L:
            pos-=1
            x[pos]=0
        x[pos]=1
        
    return x

energy = []
margin = []
Hactiveservers = []
Hhistory = []

#ALPHA = np.append(np.arange(0,.11,.01),.6)
ALPHA = np.arange(0,1,.01)
x_prev = [1]*n

for i in range(len(ALPHA)):
    L=n*C*T*ALPHA[i]
    
    if cap(x=x_prev,y=x_prev)<L:
        
        run = heuristic_add(input=x_prev,L=L)
        
        e = consumed_energy(x=run, y=x_prev)
        energy.append(e)
        
        margin.append(cap(run,x_prev)-L)
        
        x_prev = run
        
        Hhistory.append(x_prev)
        Hactiveservers.append(sum(x_prev))
    
    else:
        run = heuristic_remove(input=x_prev, L=L)
        
        e = consumed_energy(x=run, y=x_prev)
        energy.append(e)
        
        margin.append(cap(run,x_prev)-L)
        
        x_prev = run
        
        Hhistory.append(x_prev)
        Hactiveservers.append(sum(x_prev))

        
        