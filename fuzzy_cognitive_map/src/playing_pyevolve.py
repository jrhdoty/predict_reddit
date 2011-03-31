'''
Created on Mar 10, 2011

@author: johndoty
'''

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Initializators, Mutators
import math
import matplotlib.pyplot as plt
import random

'''////////////////////////////////////////
///
///    PYEVOLVE TUTORIAL
///
////////////////////////////////////////'''
#eval function from tutorial on pyevolve site (trying to evolve string of all 0's)
def tutorial_eval_func(chromosome):
    score = 0.0
    for val in chromosome:
        if val ==0:
            score +=1.0
    return score
    
def pyevolve_tutorial():
    #define the genome
    genome = G1DList.G1DList(20)            #length of genome
    genome.evaluator.set(tutorial_eval_func)#eval function for genome
    genome.setParams(rangemin = 0, rangmax = 10)
    
    #create GA engine
    ga = GSimpleGA.GSimpleGA(genome)
    '''with this instantiation we use default params for:
    num generations, pop size
    crossover rate, muation rate, selector  
    '''
    
    #run the ga
    ga.evolve(freq_stats=10)
    
    print "\n PRINTING BEST INDIVIDUAL DATA\N"
    print ga.bestIndividual()


'''////////////////////////////////////////
///
///    POLYNOMIAL EXAMPLE
///
////////////////////////////////////////'''
def polynomial_eval_func(chromosome):
    '''goal is to evolve the correct coef to the given polynomial'''
    #formula is: 4a + 6b + 3c +10d
    coef = [4, 6, 3, 10]
    num_test_cases = 10
    #generate some test cases inputs
    inputs = []
    random.seed()
    for i in range(num_test_cases):
        case = []
        for i in range(4):
            case.append(random.randint(0, 25))
        inputs.append(case)
    
    #for each test input find the correct value
    #and the value of the candidate solution
    correct_vals = []
    candidate_vals = []
    for case in inputs:
        val_correct = 0
        val_candidate = 0
        for i in range(4):
            val_correct += coef[i]*case[i]
            val_candidate += chromosome[i]*case[i]
        correct_vals.append(val_correct)
        candidate_vals.append(val_candidate)
        
    total_dif = 0
    for i in range(num_test_cases):
        total_dif += abs(correct_vals[i] - candidate_vals[i])
    return total_dif

    
def pyevolve_simple_polynomial():
    '''the running of the polynomial discovering GA'''
    #define genome
    genome = G1DList.G1DList(4)            #length of genome
    genome.evaluator.set(polynomial_eval_func)#eval function for genome
    genome.setParams(rangemin = 0, rangemax = 20)
    
     #create GA engine
    ga = GSimpleGA.GSimpleGA(genome)
    '''with this instantiation we use default params for:
    num generations, pop size
    crossover rate, muation rate, selector  
    '''
    ga.setPopulationSize(1000)
    ga.setMutationRate(0.1)
    ga.setGenerations(200)
    ga.setMinimax(Consts.minimaxType["minimize"])
    
    
    #run the ga
    ga.evolve(freq_stats=10)
    print "\n PRINTING BEST INDIVIDUAL DATA\n"
    print ga.bestIndividual()
    
    # This is the Rastringin Function, a deception function
def rastringin(xlist):
    n = len(xlist)
    total = 0
    for i in range(n):
        total += xlist[i]**2 - 10*math.cos(2*math.pi*xlist[i])
    return (10*n) + total
 
if __name__ == "__main__":
     # Genome instance
    genome = G1DList.G1DList(20)
    genome.setParams(rangemin=-5.2, rangemax=5.30)
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
    # The evaluator function (objective function)
    genome.evaluator.set(rastringin)
    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.minimax = Consts.minimaxType["minimize"]
    ga.setGenerations(800)
    ga.setMutationRate(0.05)
    # Create DB Adapter and set as adapter
    #sqlite_adapter = DBAdapters.DBSQLite(identify="rastringin")
    #ga.setDBAdapter(sqlite_adapter)
    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=50)
    # Best individual
    best = ga.bestIndividual()
    print "\nBest individual score: %.2f" % (best.getRawScore(),)
    print best

    
    
    
    
    
    