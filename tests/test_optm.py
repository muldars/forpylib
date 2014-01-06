# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)

"""
test
"""



from numpy import *
from forpylib.optm.sa import Sa
from forpylib.optm.ds import Ds

import unittest


def f(xyz):
        x,y,z,v,w,r,s = xyz
        return  (((1.-x)**3. + (y-x*x)**3. - (z**3.-y*x*v) + (v**3.-y*x*z*v)- 
                (y**3.-x*z*w)+ (w**3.-v*y*w)- (r**3.-w*x*r)+  (s**3.-y*v*s))/
                1. +(x * y * z * v * w * r * s)** 2.)


class Test(unittest.TestCase):
    
    
    
    
    def test_sa(self):
        xrange=  [(-5, 5),(-10, 10),(-20, 20),(-30, 30),(-40, 40), (-50, 50), (-60, 60)]
        n = 7
        result= zeros(n)
        fx = f(result)
        for i in range(5):     
            csa = Sa(f, n,xrange, T0=600, imax =600)
            result0= csa()
            fx0 = f(result0)
            if (fx0<fx):
                result =result0
                fx = fx0
            self.assertTrue(len(result)==n)
            
            for j in range(len(result0)):
                self.assertTrue(xrange[j][0] <= result0[j] <=   xrange[j][1])
        
        print "Simulated annealing"
        print "Result:",result,"Min:", fx
    
 
    def test_ds_len(self):
        xrange=  [(-5, 5),(-10, 10),(-20, 20),(-30, 30),(-40, 40), (-50, 50), (-60, 60)]
        n = 7
        result= zeros(n)
        fx = f(result)
        for i in range(5):
            cds = Ds(f,n,xrange, imax =4000)
            result0= cds()
            fx0 = f(result0)
            if (fx0<fx):
                result =result0
                fx = fx0
            self.assertTrue(len(result)==n)
            
            for j in range(len(result0)):
                self.assertTrue(xrange[j][0] <= result0[j] <=   xrange[j][1])
        
        print "Direct search"
        print "Result:",result,"Min:", fx
        print "---------------------------------------------------"

if __name__ == '__main__':
    unittest.main()