# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)


"""
Multidimensional direct search. This class can be used in discrete
optimization problems.
"""

################################################################################

from numpy import exp, abs, array,reshape,dot, ones,where, roll, eye, zeros,arange,int8
from numpy.random import uniform
from random import randrange, randint




class Ds(object):
    '''
    Multidimensional direct search

    This optimization method  using variable swap as search direction.
    This results in a very simplistic and inefficient method that should be 
    used only when any other method fails.
    
    '''
    def __init__(self, f, n, ranges=None, imax=1000):
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

          imax
            Maximum number of iterations, the algorithm stops as soon this
            number of iterations are executed, no matter what the error is at
            the moment.
        '''
        self.ranges = array(ranges)        
        self.__f = f
        self.__n = n
        self.__x = self.x0()
        self.__h = arange(n)
        self.__dx =  ones(n)        
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

    def step(self):
        '''
        One step of the search.

        In this method, the result of the step is highly dependent of the steps
        executed before, as the search step is updated at each call to this
        method.

        '''
             
        f = self.__f
        x = self.__x.copy()
        dx = self.__dx
        fo = f(x)
        index = self.__h[0]
        # Next estimate
        x[index] = x[index] + dx[index]
        # Sanity check
        
        r0 = self.ranges[:, 0]
        r1 = self.ranges[:, 1]
        x = where(x < r0, r0, x)
        x = where(x > r1, r1, x)
        
        # Update state
        fn = f(x)
        if fn >= fo:
            
            self.__dx[index] = -1 * self.__dx[index]
            self.__h = roll( self.__h, -1)

        else:            
            self.__x = x
        return 


    def __call__(self):
        '''
        Transparently executes the search until the minimum is found. The stop
        the maximum number of iterations.. Note that this is a ``__call__`` method, so
        the object is called as a function. This method returns the best estimate of the minimum.

        :Returns:
          This method returns the best estimate of the minimum.
        '''
        i = 0
        while i < self.__imax:
         
            self.step()
            i = i + 1
        return self.__x
        

   


################################################################################
# Test
if __name__ == "__main__":
    pass