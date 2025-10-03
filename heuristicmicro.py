#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:54:56 2024

@author: j-ponteil
"""
import math
import numpy as np
n=5

C=10
T=10
Toff=3
Ton=3
Pa=280
Ps=25
Pmicro=55
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

energymicro = []
marginmicro = []
Hactiveserversmicro = []
Hhistorymicro = []

ALPHA = np.arange(0,1,.01)
x_prev = [1]*n

for i in range(len(ALPHA)):
    L=n*C*T*ALPHA[i]
    
    if cap(x=x_prev,y=x_prev)<L:
        
        run = heuristic_add(input=x_prev,L=L)
        
        
        
        waste = cap(run,x_prev)-L
        savings = math.floor(waste/C)*(Pa-Pmicro)
        
        e = consumed_energy(x=run, y=x_prev) - savings
        energymicro.append(e)
        
        
        marginmicro.append(cap(run,x_prev)-L-C*math.floor(waste/C))
        
        x_prev = run
        
        Hhistorymicro.append(x_prev)
        
        Hactiveserversmicro.append(sum(x_prev)-math.floor(waste/C)/T)
    
    else:
        run = heuristic_remove(input=x_prev, L=L)
        
        waste = cap(run,x_prev)-L
        savings = math.floor(waste/C)*(Pa-Pmicro)
        
        e = consumed_energy(x=run, y=x_prev) - savings
        energymicro.append(e)
        
        marginmicro.append(cap(run,x_prev)-L-C*math.floor(waste/C))
        
        x_prev = run
        
        Hhistorymicro.append(x_prev)
        
        Hactiveserversmicro.append(sum(x_prev)-math.floor(waste/C)/T)
    
