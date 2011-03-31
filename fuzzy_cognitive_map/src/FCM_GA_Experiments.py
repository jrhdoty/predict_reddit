'''
Created on Mar 10, 2011

@author: johndoty
'''
import FCM
import FCM_GA
import math
import time
import numpy as np
import networkx as nx
import pyevolve
from pyevolve import G2DList
from pyevolve import GSimpleGA
from pyevolve import Consts

'''////////////////////////////////////////////////////////
///
///    GENERATE TEST CASE FOR INTEGER VALUE STATES/WEIGHTS
///
////////////////////////////////////////////////////////'''

def experiment1():
    #digraph, threshold_function, t_func_params = None, dep_coef=1, past_coef=0, normalize_initial_values = True
    myFCM = FCM.FCM(nx.DiGraph(), FCM.trivalent)  
    
    node_list = [1, 2, 3, 4, 5, 6]
    initial_state = [1, 1, 1, 1, 1, 1]
    density_percent = .4
    valid_input = False
    seed = 0
    while not valid_input:
        seed += time.time()
        print "seed is: "
        print seed
        input_FCM = FCM.generate_random_FCM_matrix(node_list, density_percent, seed, FCM.pos_neg_int, allow_self_edge = True)
        input_data = myFCM.calculate_next_states_matrix(input_FCM, initial_state, n = 30)
        print input_data
        if not myFCM.simple_pattern_recognition(input_data):
            valid_input = True
    print "\n\nINPUT FCM IS:"
    print input_FCM
    print "INPUT DATA IS:"
    for row in input_data:
        print row
    print "RUNNING GA TO ATTEMPT TO LEARN FCM"
    genome = G2DList.G2DList(len(node_list), len(node_list))
    genome.setParams(rangemin=-1, rangemax=1)
    myGA = FCM_GA.LearnFCM(input_data, node_list, myFCM, genome)
    myGA.setPopulationSize(1000)
    myGA.setGenerations(100)
    myGA.setMutationRate(0.3)
    myGA.setMinimax(Consts.minimaxType["minimize"])
    myGA.evolve(10)
    print myGA.bestIndividual()
    print "THE ERROR FOR THE BEST INDIVIDUAL IS:"
    print myGA.eval_func_matrix(myGA.bestIndividual())
    print "ACTUAL FCM"
    print input_FCM
    
    
if __name__=="__main__":
    experiment1()
    
    
    