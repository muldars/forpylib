# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)

"""
GrowthModelGeneric:
stand-level growth model  generic
"""


from math import log, sqrt, exp,pi, gamma
import numpy as np

class GrowthModelGeneric(object):

    def __init__(self, **kwargs):
        self.stand_name = str(kwargs["stand_name"])
        self.t = float(kwargs["t"])
        self.N = float(kwargs["N"])
        self.mortality = False
        if 'mortality' in kwargs:
            self.mortality = float(kwargs["mortality"])
        else:
            self.mortality =  True
        if 'H0' in kwargs and 'S' in kwargs:
            self.H0 = float(kwargs["H0"])
            self.S = float(kwargs["S"])
        if 'H0' in kwargs and not 'S' in kwargs:
            self.H0 = float(kwargs["H0"])
            self.S = self.fH0(t2=self.tref)
        if 'S' in kwargs and not 'H0' in kwargs:
            self.S, self.H0 = float(kwargs["S"])
            self.t = self.tref
            self.H0 = self.fH0(t2=kwargs["t"])
            self.t = float(kwargs["t"])
        if 'N' in kwargs:
            self.G = self.fGi(t=self.t, H0=self.H0, N=self.N)
            self.V = self.fV(t=self.t, H0=self.H0, Nb=self.N, Gb=self.G)

    def get_parametres(self):
        return [('Stand','t','H0',  'S', 'N','G','V'),(self.stand_name, self.t, self.H0, self.S, self.N, self.G,self.V)]

    def fH0(self, **kwargs):
        pass

    def fGi(self, **kwargs):
        pass

    def fGp(self, **kwargs):
        pass

    def fV(self, **kwargs):
        pass

    def fDg(self, N, G):
        return sqrt(G * 4 / (N * pi)) * 100

    def fN_diametric_class(self, N, k_upper, k_lower, c, b):
        up = (1 - exp(- ((k_upper / b) ** c)))
        down = (1 - exp(- ((k_lower / b) ** c)))
        return N * (up - down)

    def fWeibull(self, Dg, Dm):

        def fWeibullC(Dg, Dm, c):
            S2 = Dg ** 2 - Dm ** 2
            return (-S2 + (Dm * Dm / (gamma(1 + 1 / c) *
                    gamma(1 + 1 / c))) * ((gamma(1 + 2 / c)) -
                   (gamma(1 + 1 / c) * gamma(1 + 1 / c))))

      # biseccion start
        tolerance = 0.005
        lower_limit = 0.1
        upper_limit = 100
        max_iterations = 15
        c = (lower_limit + upper_limit) / 2.0
        i = 0
        while (upper_limit - lower_limit) / 2.0 > tolerance:
            if (fWeibullC(Dg, Dm, c) == 0 or i >= max_iterations):
                break
            elif fWeibullC(Dg, Dm, lower_limit) * fWeibullC(Dg, Dm, c) < 0:
                upper_limit = c
            else:
                lower_limit = c
            c = (lower_limit + upper_limit) / 2.0
            i += 1
        # biseccion end
        if c == 0:
            return 0, 0
        else:
            return c, (Dm / gamma(1 + 1 / c)), i