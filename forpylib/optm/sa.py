# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)

"""
Simulated Annealing discrete optimization
"""

from numpy import exp, abs, array, isnan, where,reshape,dot,  roll, ones, eye, zeros,arange,int8
from numpy.random import uniform
from random import randrange, randint

class Sa(object):
    '''
    Simulated Annealing discrete optimization.

    '''
    def __init__(self, f, n, ranges=None,temp=1000., r=0.95, imax=1000):
        '''
        Initializes the optimizer.

        :Parameters:
          f
            A function to be optimized.

          n
            Number of variables

          ranges
            A range of values might be passed to the algorithm..

          temp
            Initial temperature. 

          r
            Temperature decreasing rate.

          imax
            Maximum number of iterations..
        '''
        self.ranges = array(ranges)
        self.f = f
        self.n = n
        self.x = self.x0()
        self.fx = f(self.x)     
        self.temp = float(temp)
        self.r = float(r)
        self.imax = int(imax)
        
    def x0(self):
        '''
        First estimate of the minimum. 
        '''
        n = self.n
        x0 = zeros(n)        
        for index in range(n):
            x0[index] = randint(self.ranges[index, 0],self.ranges[index, 1])        
        return x0   
    
    def new(self, x):
            '''
            Generate neighbor
            '''
            x = x.copy()          
            n = self.n           
            rn =[-1,1]
            index2= randint(0,1)
            index=randrange(0,n,1)
            x[index] = x[index] + rn[index2]                                
            r0 = (x[index]<self.ranges[index, 0])
            r1 = (x[index]>self.ranges[index, 1])
            r2 = (uniform()<0.25)         
            if r0 or  r1 or r2:
                x[index] = randint(self.ranges[index, 0],self.ranges[index, 1])                         
            return x
    
    def step(self):
        '''
        One step of the search.
        '''
        f = self.f
        x = self.x
        fx = self.fx
        xn = self.new(x)
        delta = f(xn) - fx
        if delta < 0 or exp(-delta/self.temp) > uniform():
            xr = xn         
            self.x = xr
            self.fx = f(xr)       
        self.temp = self.temp * self.r              
        return

    def __call__(self):
        '''
          This method returns the best estimate of the minimum.
        '''
        i = 0
        while  i < self.imax:
            self.step()
            i = i + 1
        return self.x
