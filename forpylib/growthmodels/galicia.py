# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest optimization & simulation.
# Licensed under GNU GPL, version 3.
# UXFS Statistics & Operational Research Team (UXFSort)

"""
stand-level growth model 
growth_models_galicia:


Pinus sylvestris:
.. [1] http://ftp.forestaluchile.cl/dasometria/Lectura%2015%20Dynamic%20growth%20model%20for%20Scots%20pine%20(Pinus%20sylves.pdf

"""


from math import log, sqrt, exp, pi, gamma
import numpy as np
import base as gm

class Betula_pendula(gm.GrowthModelGeneric):
    def __init__(self, **kwargs):
        self.tref = 20
        gm.GrowthModelGeneric.__init__(self, **kwargs)
        self.model_specie = "Betula pendula"
        self.model_region = "Galicia"
        self.model_autor  = "Diéguez-Aranda et al."
        self.model_year = "2012"


    def fH0(self, **kwargs):
        """Initializes the gcs.Gcs client.

        Clients are available per module. To switch the client, update the import
        statement above.

        Parameters
    ----------
            auth_http: An authorized httplib2.Http instance.
            project_id: A string Cloud Storage project id, ex: '123456'.

        Returns:
            An instance of gcs.Gcs.
        """

        t2 = kwargs["t2"]
        X0 = 0.5 * (self.H0 - 19.8 + sqrt((19.8 - self.H0) ** 2 + 4 * 758 *
             self.H0 * self.t ** -1.398))
        return (19.8 + X0) / (1 + 758 / X0 * t2 ** -1.398)


    def fN(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        N1 = kwargs["Na"]
        mortality = kwargs["mortality"]
        if mortality:
            return ((N1 ** (-1 / 1.581) + 0.004637 * log(self.S) * ((t2 / 100)
                ** 1.581 - (self.t / 100) ** 1.581)) ** -1.581)
        else:
            return N1

    def fGi(self, **kwargs):
        t = kwargs["t"]
        N = kwargs["N"]
        return 1.512 * N ** 0.3799 * exp(-27.01 / t + 0.07972 * self.S)

    def fGp(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        G1 = kwargs["Ga"]
        X0 = (0.5 * t1 ** -0.9385 * (-136.4 + t1 ** 0.9385 * log(G1) +
             sqrt(4 * 642.8 * t1 ** 0.9385 + (136.4 - t1 ** 0.9385 * log(G1)) ** 2)))
        return exp(X0) * exp((136.4 - 642.8 / X0) * t2 ** -0.9385)

    def fDm(self, **kwargs):
        Dg = kwargs["Dg"]
        H0 = kwargs["H0"]
        return Dg - exp(-1.31 + 0.08459 * H0 - 0.04192 * self.S)

    def fV(self, after=False, **kwargs):
        H = kwargs["H0"]
        if after:
            G = kwargs["Ga"]
        else:
            G = kwargs["Gb"]
        return 0.8003 * G ** 0.971 * H ** 0.7971


class Pinus_pinaster_interior(gm.GrowthModelGeneric):
    def __init__(self, **kwargs):
        if not hasattr(self, 'I'): self.I = 0.0
        self.tref = 20
        gm.GrowthModelGeneric.__init__(self, **kwargs)
        self.model_specie = "Pinus pinaster"
        self.model_region = "Galicia interior"
        self.model_autor  = "Diéguez-Aranda et al."
        self.model_year = "2009"

    def fH0(self, **kwargs):
        """Initializes the gcs.Gcs client.

        Clients are available per module. To switch the client, update the import
        statement above.

        Parameters
    ----------
            auth_http: An authorized httplib2.Http instance.
            project_id: A string Cloud Storage project id, ex: '123456'.

        Returns:
            An instance of gcs.Gcs.
        """
        t2 = kwargs["t2"]
        X0 = (self.H0 - 72.69 + 27.86 * self.I) / (1 + (2.993 + 5.084 * self.I)
                * self.H0 * self.t ** -1.486)
        return (72.69 - 27.86 * self.I + X0) / (1 - (2.993+ 5.084 * self.I) *
                X0 * t2 ** -1.486)

    def fN(self, **kwargs):
        N1 = kwargs["Na"]
        return self.N1

    def fGi(self, **kwargs):
        t = kwargs["t"]
        X0 = (4.363 - 0.1489 * self.I) * self.S ** 0.07383
        return exp(X0) * exp(-(-167.5 + (999.1 - 50.34 * self.I) / X0) * t ** -0.8936)

    def fGp(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        G1 = kwargs["Ga"]
        X0 = (t1 ** -0.8936 / 2) * (-167.5 + t1 ** 0.8936 * log(G1) + sqrt(
             4 * (999.1 - 50.34 * self.I) * t1 ** 0.8936 + (167.5 - t1 ** 0.8936 * log(G1)) ** 2))
        return exp(X0) * exp(-(-167.5 + (999.1 - 50.34 * self.I) / X0) * t2 ** -0.8936)

    def fDm(self, **kwargs):
        t = kwargs["t"]
        Dg = kwargs["Dg"]
        H0 = kwargs["H0"]
        return Dg - exp(-0.4456 - 10.99 / t + 0.02221 * H0)

    def fV(self, after=False, **kwargs):
        H = kwargs["H0"]
        if after:
            N = kwargs["Na"]
            Dg = self.fDg(N, kwargs["Ga"])
        else:
            N = kwargs["Nb"]
            Dg = kwargs["Dg"]
        return 0.000548 * Dg ** (1.43 - 0.07553 * self.I) * H ** 1.22 * N ** (0.7681 + 0.02974 * self.I)


class Pinus_pinaster_costa(Pinus_pinaster_interior):
    def __init__(self, **kwargs):
        self.tref = 20
        self.I = 1.0
        Pinus_pinaster_interior.__init__(self, **kwargs)
        self.model_specie = "Pinus pinaster"
        self.model_region = "Galicia costa"
        self.model_autor  = "Diéguez-Aranda et al."
        self.model_year = "2009"


class Pinus_radiata(gm.GrowthModelGeneric):
    def __init__(self, **kwargs):
        self.tref = 20
        gm.GrowthModelGeneric.__init__(self, **kwargs)
        self.model_specie = "Pinus radiata"
        self.model_region = "Galicia"
        self.model_autor  = "Castedo-Dorado et al."
        self.model_year = "2006"


    def fH0(self, **kwargs):
        """Initializes the gcs.Gcs client.

        Clients are available per module. To switch the client, update the import
        statement above.

        Parameters
    ----------
            auth_http: An authorized httplib2.Http instance.
            project_id: A string Cloud Storage project id, ex: '123456'.

        Returns:
            An instance of gcs.Gcs.
        """
        t2 = kwargs["t2"]
        L0 = log(1 - exp(-0.06738 * self.t))
        X0 = 0.5 * (log(self.H0) + 1.755 * L0 + sqrt((log(self.H0) + 1.755 * L0)
             ** 2 - 4 * 12.44 * L0))
        return self.H0 * ((1 - exp(-0.06738 * t2)) / (1 - exp(-0.06738 *
               self.t))) ** (-1.755 + 12.44 / X0)

    def fN(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        N1 = kwargs["Na"]
        mortality = kwargs["mortality"]
        if mortality:
            return ((N1 ** -0.3161 + 1.053 ** (t2 - 100) - 1.053 ** (t1 - 100))
                    ** (-1 / 0.3161))
        else:
            return N1


    def fGi(self, **kwargs):
        t = kwargs["t"]
        N = kwargs["N"]
        return -52.23 + 2.676 * t + 1.306 * self.S + 0.01008 * N

    def fGp(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        G1 = kwargs["Ga"]
        X0 = t1 ** -0.9233 / 2 * (-276.1 + t1 ** 0.9233 * log(G1) +
             sqrt(4 * 1391 * t1 ** 0.9233 + (276.1 - t1 ** 0.9233 * log(G1)) ** 2))
        return exp(X0) * exp(-(-276.1 + 1391 / X0) * t2 ** -0.9233)

    def fDm(self, **kwargs):
        t = kwargs["t"]
        Dg = kwargs["Dg"]
        N = kwargs["N"]
        return Dg - exp(0.1449 - 19.76 / t + 0.0001345 * N + 0.03264 * self.S)

    def fV(self, after=False, **kwargs):
        H = kwargs["H0"]
        t = kwargs["t"]
        if after:
            G = kwargs["Ga"]
        else:
            G = kwargs["Gb"]
        return (G * H) ** (0.9987 - 0.002232 * t) * exp(-0.9635 + 0.01703 * t)

class Pinus_sylvestris(gm.GrowthModelGeneric):
    def __init__(self, **kwargs):
        self.tref = 40
        gm.GrowthModelGeneric.__init__(self, **kwargs)
        self.model_specie = "Pinus sylvestris"
        self.model_region = "Galicia"
        self.model_autor  = "Diéguez-Aranda et al."
        self.model_year = "2005"


    def fH0(self, **kwargs):
        """Initializes the gcs.Gcs client.

        Clients are available per module. To switch the client, update the import
        statement above.

        Parameters
    ----------
            auth_http: An authorized httplib2.Http instance.
            project_id: A string Cloud Storage project id, ex: '123456'.

        Returns:
            An instance of gcs.Gcs.
        """

        t2 = kwargs["t2"]
        return 51.39 / (1 - (1 - (51.39 / self.H0)) * (self.t / t2) ** 1.277)


    def fN(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        N1 = kwargs["Na"]
        mortality = kwargs["mortality"]
        if mortality:
            return (N1 ** -1.59 + 1.138 * 10 ** -12 * self.S * (t2 ** 3.308 - t1 ** -3.308)) ** (-1 / 1.59)
        else:
            return N1

    def fGi(self, **kwargs):
        t = kwargs["t"]
        return 92.4 * exp(-(1593 / self.S) * t ** (-1.369))

    def fGp(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        G1 = kwargs["Ga"]
        return 92.4 * (G1 / 92.4) ** ((t1 / t2) ** 1.369)

    def fDm(self, **kwargs):
        Dg = kwargs["Dg"]
        N = kwargs["N"]
        H0 = kwargs["H0"]
        return Dg - exp(-1.294 + 0.0001867 * N + 0.03625 * H0)

    def fV(self, after=False, **kwargs):
        H = kwargs["H0"]
        if after:
            G = kwargs["Ga"]
        else:
            G = kwargs["Gb"]
        return  0.5908 * G ** 0.9981 * H ** 0.8844

class Quercus_Robur(gm.GrowthModelGeneric):
    def __init__(self, **kwargs):
        self.tref = 60
        gm.GrowthModelGeneric.__init__(self, **kwargs)
        self.model_specie = "Quercus robur"
        self.model_region = "Galicia"
        self.model_autor  = "Diéguez-Aranda et al."
        self.model_year = "2012"


    def fH0(self, **kwargs):
        """Initializes the gcs.Gcs client.

        Clients are available per module. To switch the client, update the import
        statement above.

        Parameters
        ----------
            auth_http: An authorized httplib2.Http instance.
            project_id: A string Cloud Storage project id, ex: '123456'.

        Returns:
            An instance of gcs.Gcs.
        """

        t2 = kwargs["t2"]
        L0 = log(1 - exp(-0.0144 * self.t))
        X0 = (0.5 * (log(self.H0) + 1.049 * L0 +
              sqrt((log(self.H0) + 1.049 * L0) ** 2 - 29.92 * L0)))
        return (self.H0 * ((1 - exp(-0.0144 * t2)) /
               (1 - exp(- 0.0144 * self.t))) ** (-1.049 + 7.479 / X0))

    def fN(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        N1 = kwargs["Na"]
        mortality = kwargs["mortality"]
        if mortality:
            return N1 * np.exp(-0.01533 * (t2 - t1))
        else:
            return N1

    def fGi(self, **kwargs):
        t = kwargs["t"]
        N = kwargs["N"]
        return 104.8 * (1 - exp(-0.006031 * t)) ** (14.62 / self.S + 167.1 / N)

    def fGp(self, **kwargs):
        t1 = kwargs["t"]
        t2 = kwargs["t2"]
        G1 = kwargs["Ga"]
        H1 = kwargs["H0"]
        N1 = kwargs["Na"]
        return (G1 ** (t1 / t2) * exp(0.8579 * log(H1)
                * (1 - t1 / t2) + 0.3060 * log(N1) * (1 - t1 / t2)))

    def fDm(self, **kwargs):
        Dg = kwargs["Dg"]
        N = kwargs["N"]
        G = kwargs["Gb"]
        return Dg - exp(-0.0001691 * N + 0.01334 * G)

    def fV(self, after=False, **kwargs):
        H = kwargs["H0"]
        if after:
            N = kwargs["Na"]
            Dg = self.fDg(N, kwargs["Ga"])
        else:
            N = kwargs["Nb"]
            Dg = kwargs["Dg"]
        return 0.0000503 * Dg ** 1.974 * H ** 0.9243 * N ** 0.9752

