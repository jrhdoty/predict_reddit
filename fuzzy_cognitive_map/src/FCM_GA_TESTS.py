'''
Created on Mar 15, 2011

@author: johndoty
'''
import unittest
import FCM
import FCM_GA
import pyevolve
from pyevolve import G1DList
from pyevolve import G2DList
import numpy as np
import networkx

test_data = {1:[1, 2, 3], 2:[4, 5, 6], 3:[7, 8, 9]}

input_data1 = [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]]

input_data2 = [[5, 5, 5],
               [5, 5, 5],
               [5, 5, 5]]

input_data3 = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]]


class FCM_GA_TESTER(unittest.TestCase):
    #digraph, threshold_function, t_func_params = None, dep_coef=1, past_coef=0, normalize_initial_values = True
    myFCM = FCM.FCM(networkx.DiGraph(), FCM.no_func)
    genome = G2DList.G2DList(3, 3)
    genome.setParams(rangemin=0, rangemax=10)
    myGA = FCM_GA.LearnFCM(test_data, [1, 2, 3], myFCM, genome )    #input_data, concept_list, myFCM, genome

    def test_error_initial_(self):
        '''testing the error_initial function'''
        result = self.myGA.error_initial(input_data1, input_data2, 3)
        self.assertEqual(result, 4)
        
    def test_GA(self):
        self.myGA.setGenerations(100)
        self.myGA.evolve(10)
        print (self.myGA.bestIndividual())
        
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()