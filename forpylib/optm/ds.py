# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)


"""
Direct search algorithm
"""

from numpy import exp, abs, array,reshape,dot, ones,where, roll, eye, zeros,arange,int8
from numpy.random import uniform
from random import randrange, randint

class Ds(object):
    '''
    Direct search algorithm
    '''
    def __init__(self, f, n, ranges=None, imax=1000):
        '''
        Initializes the optimizer.

        :Parameters:
          f
            A function to be optimized..

          n
            Number of variables

          ranges
            A range of values might be passed to the algorithm..

          imax
            Maximum number of iterations.
        '''
        self.ranges = array(ranges)        
        self.f = f
        self.n = n
        self.x = self.x0()
        self.h = arange(n)
        self.dx =  ones(n)        
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

    def new(self, x,index):
        '''
        Generate neighbor
        '''
        x[index] = x[index] + self.dx[index]
        r0 = self.ranges[:, 0]
        r1 = self.ranges[:, 1]
        x = where(x < r0, r0, x)
        x = where(x > r1, r1, x)      
        return x
    
    
    def step(self):
        '''
        One step of the search.
        '''
        index = self.h[0]    
        f = self.f
        x = self.x.copy()    
        fo = f(x)      
        x = self.new(x,index)
        fn = f(x)       
        if fn >= fo:          
            self.dx[index] = -1 * self.dx[index]
            self.h = roll( self.h, -1)
        else:            
            self.x = x
        return 

    def __call__(self):
        '''
          This method returns the best estimate of the minimum.
        '''
        i = 0
        while i < self.imax:        
            self.step()
            i = i + 1
        return self.x
        

