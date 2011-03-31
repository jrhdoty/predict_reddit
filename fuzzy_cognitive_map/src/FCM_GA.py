'''
Created on Mar 9, 2011

@author: johndoty
'''
import FCM
import math
import numpy as np
import networkx as nx
import pyevolve
from pyevolve import GSimpleGA
'''
This module is designed to discover the edges and weights for arbitrary Fuzzy Cognitive Maps given a time series 
of some systems state data.  It is loosely is based on the work presented in 
[Stach, Kurgan, Pedrycz, Reformat, "Genetic Learning of Fuzzy Cognitive Maps" Fuzzy Sets and Systems 153 (2005) 371-401]
It inherits from pyevolve, an open source genetic algorithm library and uses internally a custom FCM simulation class
'''

'''////////////////////////////////////////
///
///    LEARN FCM CLASS
///
////////////////////////////////////////'''

class LearnFCM(GSimpleGA.GSimpleGA):
    
    myFCM = None
    processed_data = None
    
    def __init__(self, input_data, concept_list, myFCM, genome):
        '''input data is dictionary, keys: concept names, value: concept values over time
        an FCM that specifies the details of processing and normalizing the data from FCM iterations, 
        the initial digraph in this FCM will be replaced so it can be any arbitrary digraph
        takes in a genome of type pyevolve.D2List.D2List, and a list of concepts whose order corresponds to the genome matrix
        e.g.
                                concept_list[0]        concept_list[1]           concept_list[2]
                            
        concept_list[0]        genome[0][0]            genome[0][1]            genome[0][2]
        
        concept_list[1]        genome[1][0]            genome[1][1]            genome[1][2]
        
        concept_list[2]        genome[2][0]            genome[2][1]            genome[2][2]
        
        '''
        self.genome = genome
        genome.evaluator.set(self.eval_func_matrix)
        self.concept_list = concept_list
        self.num_concepts = len(concept_list)
        self.input_data = input_data
        self.processed_data = self.process_input_data(input_data)   #process input_data into pair format for eval_function
        
        #create completely connected digraph for nodes and insert it into the FCM simulator
        self.digraph = nx.DiGraph()
        self.digraph.add_nodes_from(self.concept_list)
        for concept1 in self.concept_list:
            for concept2 in self.concept_list:
                self.digraph.add_edge(concept1, concept2, {'weight': 0})
        self.myFCM = myFCM
        self.myFCM.set_digraph(self.digraph)
        pyevolve.GSimpleGA.GSimpleGA.__init__(self, self.genome)
        
    
    '''////////////////////////////////////////
    ///
    ///    EVALUATION FUNCTIONS
    ///
    ////////////////////////////////////////'''
    def eval_func_digraph(self, chromosome):
        '''implementation of the evaluation function suggested in the paper cited above:
        given input data of length k, we group each two adjacent state vectors, producing k-1 different pairs
        for each data pair, (t, t+1), define t to be the initial vector and t+1 to be the system response
        fitness function is calculated by taking the difference between the known system response for each initial vector 
        and the candidate FCM response after one iteration starting with the initial vector
        The L2-norm is taken of the vector of differences for each concept for each k-1 pairs summed and normalized
        '''
        #set edges to the chromosome's values
        edge_weight_list = []
        
        for i in range(self.num_concepts):
            for k in range(self.num_concepts):
                edge_weight_list.append((self.concept_list[i], self.concept_list[k], {'weight': chromosome[i][k]}))
        self.myFCM.set_edges(edge_weight_list)
        
        error_vectors = []
        error_t = []
        
        #for each k-1 pairs of state vectors
        for i in range(len(self.processed_data)-1):
            #initialize the FCM initial state
            node_value_list = {}
            for concept in self.concept_list:
                node_value_list[concept] = self.input_data[concept][i]
            self.myFCM.set_nodes(node_value_list)
            #perform one iteration of network
            self.myFCM.calculate_next_states(1)
            #calculate dif from candidate FCM output and actual output
            for item in self.myFCM.get_nodes():
                error_t.append(abs(item[1]['value'] - node_value_list[item[0]]))
            error_vectors.append(error_t)
            error_t = []
        
        #sum and normalize the Lp-norm
        coef = 1.0/((len(self.processed_data)-1)*self.num_concepts)
        total = 0
        for vector in error_vectors:
            total += self.calculate_L_2_norm(vector)
    
        return coef*total
        
        
    def eval_func_matrix(self, chromosome):
        '''
        in this representation the causal weights b/w concepts is expressed as such:
        (1,1)(2,1)(3,1)
        (1,2)(2,2)(3,2)
        (1,3)(2,3)(3,3)
        the state vector is multiplied by the weight matrix, then each row is summed to get the new 
        concept value
        '''
        error_vectors = []
        weight_matrix = np.array(chromosome[:])
        #print "WEIGHT MATRIX"
        #print weight_matrix
        
        for i in range(len(self.processed_data)-1):
            initial_vector = np.array(self.processed_data[i])
            #print "INITIAL VECTOR"
            #print initial_vector
            result_vector = self.processed_data[i+1]
            #print "RESULT VECTOR"
            #print result_vector
            next_step = initial_vector*weight_matrix
            #print "NEXT STEP"
            #print next_step
            error_t = []
            for k in range(self.num_concepts):
                #sum the value of incoming edges*weight, then normalize value with given function
                error_t.append(abs(result_vector[k]- self.myFCM.normalize_value(sum(next_step[k])))) 
            #print "ERROR_T"
            #print error_t
            #print "EXITING"
            error_vectors.append(error_t)
            
        #sum and normalize the Lp-norm
        coef = 1.0/((len(self.processed_data)-1)*self.num_concepts)
        total = 0
        for vector in error_vectors:
            total += self.calculate_L_2_norm(vector)
        #print "FITNESS VAL: %f" % (coef*total)
        return coef*total
    
    '''////////////////////////////////////////
    ///
    ///    EVALUATION FUNCTION HELPERS
    ///
    ////////////////////////////////////////'''
        
    def calculate_L_2_norm(self, vector):
        total = 0
        for item in vector:
            total += item**2
        return math.sqrt(total)
        
    '''////////////////////////////////////////////////////////////////////////////////
    ///
    ///    FUNCTIONS THAT EVALUATE THE EFFECTIVENESS OF SOLUTIONS GENERATED BY GA
    ///
    ////////////////////////////////////////////////////////////////////////////////'''  
    def error_initial(self, input_data, candidate_data, num_concepts):
        '''order of concepts must be the same in input_data and candidate_data
        the initial state vector should not be included in the input parameters
        it should have been the same for both'''
        coef = 1.0/(len(input_data)*num_concepts)   
        error_total = 0.0
        for i in range(len(input_data)):
            for k in range(num_concepts):
                error_total += abs(input_data[i][k] - candidate_data[i][k])
        return coef*error_total
                
    
    '''////////////////////////////////////////
    ///
    ///    UTLITY FUNCTIONS 
    ///
    ////////////////////////////////////////'''
    def process_input_data(self, input_data):
        '''turns the input data into a list of lists, each nested list corresponding to the FCM state at time t'''
        processed_list = []
        for i in range(len(self.concept_list)):
            t = []
            for concept in self.concept_list:
                t.append(input_data[concept][i])
            processed_list.append(t)
        return processed_list

    
    

    
    
    
    
    
    
    
    
    
    
    