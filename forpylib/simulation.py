# !/usr/bin/env python
# -*- coding: utf-8 -*-
# forpylib - A Python library for forest simulation & optimization
# Licensed under GNU GPL, version 3
# UXFS Statistics & Operations Research Team (UXFSort)

"""
simulation
==========
Contains two classes, one to specify forest management prescriptions
(a itemized time schedule for operations, such as harvesting, planting, thinning)
and other to simulate stand tables based on dynamic growth models for
single-species, eveng-aged stands

    Example:
    
        >>> from growth_models.galicia import Betula_pendula
        >>> from simulation import PrescriptionWriter, Simulator
        >>> my_stand = Betula_pendula(stand_name="12A", t=10.0, H0=16.0, N=1000.0)
        >>> my_prescription = PrescriptionWriter(interval=3, periods=10)
        >>> my_prescription.add_thin(period=3, ti=50, rr=1)
        True
        >>> my_prescription.add_thin(period=6, ti=50, rr=0.6)
        True
        >>> my_prescription.add_final_harvest(period=10)
        True
        >>> my_simulation = Simulator(prescription=my_prescription, stand=my_stand)
        >>> my_simulation._to_string()
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from tools.tabulate import *
import time

class PrescriptionWriter(object):
    """ A class to specify forest management prescriptions (sequence of 
        operations) at stand level  

    :Parameters:

        periods : int,
                  number of projection periods

        interval : int,
                   period length in years

    :Example:
    
        Creates a new stand forest management prescription object for 10 periods 
        of 5 years length

        >>> my_prescription = PrescriptionWriter(stand=my_stand, periods=10, interval=5)
    """
    def __init__(self,  periods=1, interval=1):
        self.interval = float(interval)
        self.periods = float (periods)
        self.p = np.arange(1, self.periods + 1, dtype=np.int)
        self.actions = pandas.DataFrame({'p': self.p, 'ti': 0., 'rr': 0.},
                                        index=pandas.Index(self.p, name='period'))

    def add_final_harvest(self, period):
        """Adds a final harvest to the prescription

        :Parameters:
        
            period : int, in the range [1..self.periods] 
                     final harvest period
        
        :Returns:
        
            Bool, True if the action has been succesfully added to the presciption,
                  False otherwise

        :Examples:
        
            Final harvest at period 9 
    
            >>> my_prescription.add_final_harvest(period=9)
            True
        """
        return self.add_thin(period=period, ti=100.0, rr=1.0)

    def add_thin(self, period, ti=0.0, rr=1.0):
        """Adds a thinning to the prescription

        :Parameters:
        
            period :  int, in the range [1..self.periods] 
                      thinning period
    
            ti : float, in the range [0..100]
                 thinning intensity (the percentage of trees to remove)
    
            rr : float, in the range [0.5..1.5]
                 stand basal area removal ratio (the ratio of stand basal area
                 to remove to stand basal area before thinning times the ratio of
                 number of trees before thinning to number of trees to remove)

        :Returns:
        
            bool, True if the action has been succesfully added to the presciption,
                  False otherwise

        :Examples:

            Thinning at period 4 in which 30% of trees are removed
            with a stand basal area removal ratio of 1.0 (sistematic thinning)

            >>> my_prescription.add_thin(period=4, ti=30, rr=1.0)
            True
        """

        if (0 < period <= self.periods) and (0 < ti <= 100) and (0.5 <= rr <= 1.5):
            self.actions.ti[period] = ti
            self.actions.rr[period] = rr
            return True
        else:
            return False

    def delete_prescription(self):
        """
        Deletes all previously defined actions in the current prescription
        """
        self.actions.ti = 0.0
        self.actions.re = 0.0

    def get_actions(self, columns= ['p', 'ti', 'rr']):
        """
        Generates a list of the specified actions in the current prescription

        :Returns:
                pandas.dataset, actions in the current prescription
        """
        return self.actions.reindex(columns=columns)




class Simulator(object):
    """
    A class to generate stand tables on the basis of the initial state of
    the stands and the specified management prescriptions

    :Parameters:
    

        prescription : simulation.PrescriptionWriter
                       a instance of class to specify forest management 
                       prescriptions (sequence of operations) at stand leve
        
            
        stand : growth_models.generic,
                the initial state of a stand of a given species for which
                there exists a dynamic stand growth modell
        
        relative : bool
                   if True, the prescription is applied from the year: stand.t
                   if False, the prescription is applied from the year: zero
            
            
    :Example:

        Creates a new stand table on the basis of the initital state of the
        stand and the specified prescription

        >>> my_simulation = Simulator(prescription=my_prescription, stand=my_stand)
    """
    def __init__(self, prescription,stand, relative = False):
        self.prescription = prescription
        self.stand = stand
        if relative:
            self.inc = 0
            self.p = np.arange(1, 1 + self.prescription.periods - self.inc , dtype=np.int)
            self.t = (self.p - 1) * self.prescription.interval + self.stand.t  + \
                                                self.prescription.interval / 2
            self.prescription.actions['t'] = ((self.p - 1) * self.prescription.interval 
                                        + self.stand.t + self.prescription.interval / 2)
        else:
            self.inc = (np.floor(((self.prescription.interval / 2.0) +
                            self.stand.t) / self.prescription.interval))
            self.p = np.arange(1, 1 + self.prescription.periods - self.inc , dtype=np.int)
            self.t = (self.inc * self.prescription.interval ) +  ((self.p-1)
                      * self.prescription.interval + self.prescription.interval / 2)
            self.prescription.actions['t'] = ((self.prescription.actions.p - 1) * 
                                               self.prescription.interval  + 
                                               self.prescription.interval / 2)
        self.t2 = self.t + self.prescription.interval
        self.simulation = self.get_simulation()

    def get_simulation(self, columns = (['t', 'H0', 'Dg', 'Dm', 'HBIb',
                                        'Nb', 'Gb', 'Vb', 'Nr', 'Gr', 'Vr', 'Na',
                                        'Ga', 'Va', 'HBIa', 'MAI', 'PAI'])):
        """Generates a dataset with the simulated stand table

        :Parameters:
   
            colums : array,
                name of stand variables to include in the dataset

        :Returns:

            ds : pandas.dataset,
        """

        ds = pandas.DataFrame({'p': self.p,
                               't': self.t,
                               't2': self.t2,
                               'mortality':True,
                               'Nb': 0., 'Gb': 0., 'Vb': 0., 'H0': 0., 'Dg': 0.,
                               'Dm': 0., 'HBIb': 0., 'tst': -1.0, 'Nr': 0.,
                               'Gr': 0., 'Vr': 0., 'Na': 0., 'Ga': 0.,
                               'Va': 0., 'HBIa': 0.,'Vra': 0.,'PAI': 0.,'MAI': 0.,
                                'interval':self.prescription.interval},
                              index=pandas.Index(self.p,
                                                 name='period'))


        ds0 = {'t': self.stand.t,'tst': self.stand.t-self.prescription.interval/2.0,
               't2': self.stand.t + self.prescription.interval/2.0,
               'mortality':self.stand.mortality,'Va': self.stand.V, 'Vra': 0.0,
               'H0': self.stand.H0, 'Na': self.stand.N, 'Ga': self.stand.G,
               'interval':self.prescription.interval/2.0}

        for i in ds.index:
            ds.H0[i] = self.stand.fH0(**ds0)
            ds.Gb[i] = self.stand.fGp(**ds0)
            ds.tst[i] =  ds0['tst'] + self.prescription.interval
            ds.mortality[i]= (ds0['tst'] > 0 and ds0['Na'] > 100
                              and self.stand.mortality)
            ds.Nb[i] = self.stand.fN(**ds0)
            ds.Dg[i] = self.stand.fDg(ds.Nb[i], ds.Gb[i])
            ds.Dm[i] = self.stand.fDm(**ds.loc[i])
            ds.HBIb[i] = (100 * np.sqrt(10000 / ds.Nb[i]) / ds.H0[i])
            ds.Vb[i] = self.stand.fV(**ds.loc[i])
            ds.Nr[i] = ds.Nb[i] * self.prescription.actions.ti[i+self.inc]/100
            if (ds.Nr[i] > 0): ds.tst[i] = 0
            ds.Gr[i] = (self.prescription.actions.rr[i+self.inc] * ds.Gb[i]
                        * ds.Nr[i] / ds.Nb[i])
            ds.Na[i] = ds.Nb[i] - ds.Nr[i]
            ds.Ga[i] = ds.Gb[i] - ds.Gr[i]
            if ds.Na[i] > 0:
                ds.Va[i] = self.stand.fV(after=ds.Nr[i] > 0, **ds.loc[i])                
            ds.Vr[i] = ds.Vb[i] - ds.Va[i]
            ds.HBIa[i] = (100 * np.sqrt(10000 / ds.Na[i]) / ds.H0[i])
            ds.Vra[i] += ds.Vr[i] + ds0['Vra']
            ds.PAI[i] = (((ds.Vra[i] + ds.Va[i])-(ds0['Vra'] + ds0['Va'])) /
                                 ds0['interval'])
            ds.MAI[i] = (ds.Vra[i] + ds.Va[i]) / ds.t[i]
            if (ds.Na[i] < 25): break
            ds0 = ds.loc[i]
        return ds.reindex(columns=columns)

    def _to_string(self):

        summary = [('Generated by:', "forpylib"),
                   ('Date:', time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())),
                   ("Growth Model:", self.stand.model_specie + " - " +
                                     self.stand.model_region + " - " +
                                     self.stand.model_autor + " - " +
                                     self.stand.model_year)]
        prescription = self.prescription.get_actions(columns= ['p', 't','ti', 'rr'])
        txt = (
               "\n"
            +   "SUMMARY:\n"
            +  "========\n"
            +  tabulate(summary, tablefmt="grid")
            +  "\n"
            +  "\nSTAND:\n"
            +  "======\n"
            +  tabulate(self.stand.get_parametres(), headers="firstrow", tablefmt="orgtbl")
            +  "\n"
            +  "\nPRESCRIPTION:\n"
            +  "=============\n"
            +  tabulate(prescription[prescription.ti>0], headers="keys", tablefmt="orgtbl")
            +  "\n"
            +  "\nSIMULATION:\n"
            +  "===========\n"
            +  tabulate(self.simulation[self.simulation.H0>0], headers="keys", tablefmt="orgtbl"))

        return txt

    def plot(self,vars=['N','G','V','HBI']):        
        
        ds = self.simulation      
        columns =  ['t','N','G','V','H0','HBI', 'Nr', 'Gr']     
        d1=ds[['t','Nb','Gb','Vb','H0','HBIb','Nr', 'Gr']]
        d1.columns = columns
        d2=ds[['t','Na','Ga','Va','H0','HBIa','Nr', 'Gr']]
        d2.columns = columns
        dt = pandas.concat([d1,d2], ignore_index=True).sort(['t','N'], ascending=[1, 0])

        dr = ds[ds.Nr>0] 
        de=dr[['t','Nb','Gb','Vb','H0','HBIb','Nr', 'Gr']]
        de.columns = columns
        
        pos = len(vars)* 100 + 10       
        plt.figure(figsize=(10,10))
        plt.rcParams.update({'font.size': 10})
        n = 0        
        for var in vars:
            n += 1            
            pos += 1
            ax = plt.subplot(pos)
            plt.plot(dt.t,dt[var],lw=2,color="black") 
            plt.subplots_adjust(hspace =0)
            plt.grid(True)  
            ax.set_xticklabels(())
            ax.margins(0.1,0.2)
            ax.set_ylabel(var,fontsize=13)
            ax.yaxis.set_label_position("right")                  
            if n == 1: plt.title("stand: " + self.stand.stand_name,fontsize=13 )  
            y_min,y_max = ax.get_ylim()          
            for i in de.index:
                plt.text(de.t[i], y_min,"thin(%.0f;%.2f)"% ((100*de.Nr[i]/ 
                         de.N[i]),(de.Gr[i]*de.N[i] /(de.G[i]* de.Nr[i] ))),
                         verticalalignment='top', horizontalalignment='center', 
                         fontsize=9,backgroundcolor='0.95')
                plt.plot([de.t[i],de.t[i]],[y_min,de[var][i]],":",color="red")               
            plt.plot(dt.t,dt[var],lw=2,color="black")
            plt.plot(de.t,de[var],'o',color="red")
        
        ax.set_xticklabels(ax.get_xticks())    
        ax.set_xlabel(u"Time (years)")
        #plt.savefig("grafica.png",dpi=300)
        return plt
        


