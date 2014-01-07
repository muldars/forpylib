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
        return  -((((1.-x)**3. + cos(y-x*x)**3. - cos(z**3.-y*x*v) + sin(v**3.-y*x*z*v)- 
                sin(y**3.-x*z*w)+ cos(w**3.-v*y*w)- (r**3.-w*x*r)+  sin(s**3.-y*v*s))/
                1. +cos(x * y * z * v * w * r * s)** 2.))


class Test(unittest.TestCase):
     
    
    def test_sa(self):
        xrange = [(-5, 5),(-10, 10),(-20, 20),(-30, 30),(-40, 40), (-50, 50), (-60, 60)]
        n = 7
        result = zeros(n)
        fx = f(result)
        for i in range(5):     
            csa = Sa(f, n,xrange,temp=600, imax=600)
            result0= csa()
            fx0 = f(result0)
            if (fx0<fx):
                result =result0
                fx = fx0
            self.assertTrue(len(result)==n)
            
            for j in range(len(result0)):
                self.assertTrue(xrange[j][0] <= result0[j] <= xrange[j][1])
        
        print "Simulated annealing"
        print "Result:",result,"Min:", fx 
 
    def test_ds(self):
        xrange = [(-5, 5),(-10, 10),(-20, 20),(-30, 30),(-40, 40), (-50, 50), (-60, 60)]
        n = 7
        result= zeros(n)
        fx = f(result)
        for i in range(10):
            cds = Ds(f,n,xrange, imax=5000)
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