# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)

"""
Simulated annealing optimization. This class can be used in discrete
optimization problems.
"""

################################################################################

from numpy import exp, abs, array, isnan, where,reshape,dot,  roll, ones, eye, zeros,arange,int8
from numpy.random import uniform
from random import randrange, randint




class Sa(object):
    '''
    Simulated Annealing discrete optimization.

    This is a simulated annealing optimizer implemented to work with vectors of
    discrete variables (obviouslly, implemented as integers numbers). In
    general, simulated annealing methods searches for neighbors of one estimate,
    which makes a lot more sense in discrete problems. 
.
    '''
    def __init__(self, f, n, ranges=None,T0=1000., rt=0.95, imax=1000):
        '''
        Initializes the optimizer.

        To create an optimizer of this type, instantiate the class with the
        parameters given below:

        :Parameters:
          f
            A multivariable function to be optimized. The function should have
            only one parameter, a multidimensional line-vector, and return the
            function value, a scalar.

          n
            Number of variables

          ranges
            A range of values might be passed to the algorithm, but it is not
            necessary. If supplied, this parameter should be a list of ranges
            for each variable of the objective function. It is specified as a
            list of tuples of two values, ``(x0, x1)``, where ``x0`` is the
            start of the interval, and ``x1`` its end. Obviously, ``x0`` should
            be smaller than ``x1``. It can also be given as a list with a simple
            tuple in the same format. In that case, the same range will be
            applied for every variable in the optimization.

          T0
            Initial temperature of the system. The temperature is, of course, an
            analogy. Defaults to 1000.

          rt
            Temperature decreasing rate. The temperature must slowly decrease in
            simulated annealing algorithms. In this implementation, this is
            controlled by this parameter. At each step, the temperature is
            multiplied by this value, so it is necessary that ``0 < rt < 1``.
            Defaults to 0.95, smaller values make the temperature decay faster,
            while larger values make the temperature decay slower.

          imax
            Maximum number of iterations, the algorithm stops as soon this
            number of iterations are executed, no matter what the error is at
            the moment.
        '''
        self.ranges = array(ranges)
        self.__f = f
        self.__n = n
        self.__x = self.x0()
        self.__fx = f(self.__x)
        
        self.__t = float(T0)
        self.__r = float(rt)
        self.__imax = int(imax)
        

    def x0(self):
        '''
        First estimate of the minimum. 
        Estimates can be given in any format,but internally they are converted 
        to a one-dimension vector, where each component corresponds to the 
        estimate of that particular variable. 
        '''
        n = self.__n
        x0 = zeros(n)        
        for index in range(n):
            x0[index] = randint(self.ranges[index, 0],self.ranges[index, 1])        
        return x0
    
    
    def new(self, x):
            '''
            Generate neighbor
            
            In this method,  >>completar
            :Parameters:
              x
                The estimate to which the neighbor must be computed.
            '''

            x = x.copy()          
            n = self.__n
            
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

        It is accepted as a new estimate if it
        performs better in the cost function *or* if the temperature is high
        enough. In case it is not accepted, a gradient step is executed.

        :Returns:
          This method returns a tuple ``(x, e)``, where ``x`` is the updated
          estimate of the minimum, and ``e`` is the estimated error.
        '''
        f = self.__f
        x = self.__x
        fx = self.__fx

        # Next estimate
        xn = self.new(x)
        delta = f(xn) - fx
        if delta < 0 or exp(-delta/self.__t) > uniform():
            xr = xn         
            self.__x = xr
            self.__fx = f(xr)


        
        self.__t = self.__t * self.__r
        
        
        return

        
       

    def __call__(self):
        '''
        Transparently executes the search until the minimum is found. The stop
        criteria are the  maximum number of iterations. 

        :Returns:
          This method returns the best estimate of the minimum.
        '''
        i = 0
        while  i < self.__imax:
            self.step()
            i = i + 1
        return self.__x
