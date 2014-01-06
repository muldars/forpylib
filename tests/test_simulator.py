# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:36:52 2014

@author: forostm
"""


from forpylib.simulation import PrescriptionWriter, Simulator
import forpylib.growthmodels.galicia as gm
import unittest


class Test(unittest.TestCase):
    def test_simulator(self):
        
        my_stand = gm.Betula_pendula(stand_name="12A", t=11.0,
                                     H0=16.0, N=1000.0, mortality=False)
        my_prescription = PrescriptionWriter(interval=1,periods=50)
        self.assertTrue(my_prescription.add_thin(period=15, ti=50, rr=1))
        self.assertTrue(my_prescription.add_thin(period=25, ti=50, rr=0.6))
        self.assertTrue(my_prescription.add_thin(period=35, ti=50, rr=0.6))
        self.assertTrue(my_prescription.add_final_harvest(period=50))
        self.assertFalse(my_prescription.add_thin(period=0))
        self.assertFalse(my_prescription.add_thin(period=51))               
        my_simulation = Simulator(prescription=my_prescription,
                                        stand=my_stand,relative=False)

        self.assertTrue(my_simulation.simulation['Nr'].sum() == my_stand.N)
        print (my_simulation._to_string())
        
        

if __name__ == '__main__':
    unittest.main()