'''
Created on Mar 7, 2011

@author: johndoty
'''
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font
import math
import time
import random
from copy import deepcopy


'''////////////////////////////////////////
///
///    FCM Class
///
////////////////////////////////////////'''
class FCM():
    '''
    This class is a Fuzzy Cognitive Map.  It takes as input a weighted networkx.DiGraph
    as well as parameters for how to calculate successive states, threshold functions
    and how to transform the the fuzzy concept values to the real value of the systems's variable for which it stands
    '''


    def __init__(self, digraph, threshold_function, t_func_params = None, dep_coef=1, past_coef=0, normalize_initial_values = True):
        '''
        Takes as input a weighted digraph, 
        a coefficient that determines how dep. a concept's value is on the interconnected concepts
        a coefficient that determines how dep. a concept's value is on its previous state
        a threshold function to normalize concept fuzzy values after each iteration
        extra parameters for threshold function
        '''
        self.digraph = digraph
        self.dep_coef = dep_coef
        self.past_coef = past_coef
        self.threshold_function = threshold_function
        self.t_func_params = t_func_params
        #iterate through digraph nodes to get list of concept names
        self.concept_names = []
        self.concept_names.extend(digraph.nodes_iter())
        
        #normalize the node values using threshold function?
        if normalize_initial_values:
            for concept in self.concept_names:
                digraph.node[concept]['value'] = self.normalize_value(digraph.node[concept]['value'])
                
        #place the initial state as first item in state time series list
        initial_state = {}
        for concept in self.concept_names:
            initial_state[concept] = digraph.node[concept]['value']
        self.state_time_series = [initial_state]
        
    def normalize_value(self, input):
        '''normalize the input value according to the threshold function that was passed in __init__'''
        if self.t_func_params != None:
            normalized_value = self.threshold_function(input, self.t_func_params)
        else:
            normalized_value = self.threshold_function(input)
            
        return normalized_value
        
        
    def __calculation_rule(self, concept):
        '''
        takes as input the name of one of the concept nodes in the FCM
        it then calculates the value of that concept at time (t+1)
        python implementation of the calculation rule presented in 
        'Modeling Complex Systems Using Fuzzy Cognitive Maps' Sylios and Groumpos IEEE Vol. 34 No. 1, Jan 2004
        '''
        concept_value = self.digraph.node[concept]['value']  #the current value of concept
        predecessors = self.digraph.predecessors(concept)     #get dict of incoming edges
        edge_value_weight_products = 0.0
        #multiply the predecessor's value by the weight of the edge and sum the values
        for neighbor in predecessors:
            edge_value_weight_products += self.digraph.node[neighbor]['value']*self.digraph[neighbor][concept]['weight']        
        next_value = (edge_value_weight_products * self.dep_coef) + (concept_value * self.past_coef)
        normalized_value = self.normalize_value(next_value)
        return normalized_value
    
    def calculate_next_states(self, n = 1):
        '''
        performs calculation function on all nodes
        then assigns each node its updated value
        and stores this state in state_time_series 
        '''
        while n > 0:
            next_state = {}
            for concept in self.digraph.nodes_iter():
                next_state[concept] = self.__calculation_rule(concept)
            #once all values at t+1 have been calculated update node values and time_series data
            self.state_time_series.append(next_state)
            for key, val in next_state.items():
                self.digraph.node[key]['value'] = val
            n -= 1
    
    def calculate_next_states_matrix(self, matrix, initial_state, n = 1):
        '''performs FCM simulation for a matrix representation of FCM and initial_state vector'''
        matrix = np.array(matrix)
        initial_state = np.array(initial_state)
        state_time_series = [initial_state]
        
        for i in range(n):
            weight_value_product = initial_state * matrix
            next_state = []
            for row in weight_value_product:
                next_state.append(self.normalize_value(sum(row)))
            state_time_series.append(next_state)
            initial_state = next_state
        return state_time_series
                
            
    '''////////////////////////////////////////
    ///
    ///    ACCESSOR AND MUTATOR FUNCTIONS 
    ///
    ////////////////////////////////////////'''
    def set_digraph(self, new_graph):
        self.digraph = new_graph
        self.concept_names = []
        self.concept_names.extend(self.digraph.nodes_iter())
        
    def set_nodes(self, values):
        '''takes a dict of node:value pairs to update node values with'''
        for key, val in values.items():
            self.digraph.node[key]['value'] = val
    
    def set_edges(self, values):
        '''takes a list of (node1, node2 {weight: value}) to update node values with'''
        self.digraph.add_edges_from(values)
        
    def get_nodes(self):
        '''get all of the concepts in the FCM'''
        return deepcopy(self.digraph.nodes(data=True))
        
    def get_edges(self):
        '''get all of the directed edges and weights from FCM'''
        return deepcopy(self.digraph.edges(data=True))
    
    def get_state_time_series(self):
        '''accessor function to get the state data'''
        return self.state_time_series
    
    def clear_nodes(self):
        '''set all node values to 0'''
        for node in self.digraph.nodes():
            self.digraph.node[node]['value'] = 0
            
    def clear_edges(self):
        '''set all edge weights to 0'''
        for edge in self.digraph.edges():
            self.digraph.edge[edge[0]][edge[1]]['weight'] = 0
            
    def clear_state_time_series(self):
        '''clear the state_time_series dictionary'''
        self.state_time_series = []
        
    '''////////////////////////////////////////
    ///
    ///    PATTERN RECOGNITION FUNCTIONS 
    ///
    ////////////////////////////////////////'''

    def simple_pattern_recognition(self, state_time_series):
        '''
        will generally only work if threshold function maps to a finite number of values (e.g. bivariate, trivariate)
        reports if a cycle has been reached and the length (number of iterations) of the cycle 
        a cycle length of 1 indicates equilibrium
        state_number parameter is 0 indexed
        '''
        if len(state_time_series) == 0:
            return 0
        length = range(len(state_time_series))
        #if the state is equal another state further in the series it indicates a cycle
        #return the cycle length
        for i in length:
            for k in length[i+1:]:
                comp = state_time_series[i] == state_time_series[k]
                if np.all(comp):
                    return k-i
        return 0

                
    
'''////////////////////////////////////////
///
///    GENERATE RANDOM FCM 
///
////////////////////////////////////////'''
def generate_random_FCM(node_list, density_percent, seed, node_value_generator, edge_weight_generator, allow_self_edge = True):
    '''creates a random FCM made up of concepts contained in node_list
    and with number of edges equal to len(node_list)*(len(node_list)-1)*density_percent
    the weights and node values are by default real numbers
    returns a digraph'''
    random.seed(seed)
    digraph = nx.DiGraph()
    N = len(node_list)
    for node in node_list:
        digraph.add_node(node, value=node_value_generator())
    total_edges = int(N*(N-1)*density_percent)
    current_edges = 0
    edge_list = []
    while current_edges < total_edges:
        #select two random nodes
        n1 = random.randint(0, N-1)
        n2 = random.randint(0, N-1)
        e = (node_list[n1], node_list[n2])
        #make sure edge doesn't already exist
        if e not in edge_list:
            #check to see if ok to do reflexive edges
            if allow_self_edge == True or n1 != n2:
                edge_list.append(e)
                current_edges += 1
    for edge in edge_list:
        digraph.edge[edge[0]][edge[1]] = {'weight': edge_weight_generator()}
        
    return digraph
    
def generate_random_FCM_matrix(node_list, density_percent, seed, edge_weight_generator, allow_self_edge = True):
    '''creates a random FCM made up of concepts contained in node_list
    and with number of edges equal to len(node_list)*(len(node_list)-1)*density_percent
    the weights and node values are by default real numbers
    returns a matrix'''
    num_concepts = len(node_list)
    matrix = np.zeros((num_concepts, num_concepts))
    if allow_self_edge:
        total_edges = int(num_concepts*(num_concepts)*density_percent)
    else:
        total_edges = int(num_concepts*(num_concepts-1)*density_percent)
    current_edges = 0
    edge_list = []
    while current_edges < total_edges:
        #select two random nodes
        n1 = random.randint(0, num_concepts-1)
        n2 = random.randint(0, num_concepts-1)
        #make sure edge doesn't already exist
        if matrix[n1][n2] == 0:
            #check to see if ok to do reflexive edges
            if allow_self_edge == True or n1 != n2:
                matrix[n1][n2] = edge_weight_generator()
                current_edges += 1
    return matrix
    
    

def pos_real():
    return random.random()

def pos_neg_real():
    return random.random()*2.0 - 1

def pos_int():
    return 1

def pos_neg_int():
    if random.randint(0, 1) == 0:
        return -1
    return 1
   

    
'''////////////////////////////////////////
///
///    THRESHOLD FUNCTIONS
///
////////////////////////////////////////'''
def bivalent_pos_zero(input):
    '''maps negative and positive values to 1 and 0 respectively'''
    if input >= 0:
        return 1
    else:
        return 0
    
def bivalent_pos_neg(input):
    '''maps negative and positive values to 1 and 0 respectively'''
    if input >= 0:
        return 1
    else:
        return -1
        
def trivalent(input):
    '''maps value of zero to zero, and positive and negative values to 1 and 0 respectively'''
    if input <= -0.5:
        return -1
    elif input >= 0.5:
        return 1
    return 0

def logistic_signal_funct_pos_zero(input, coef):
    ''' 
    a sigmoidal function that maps to [0, 1], coef determines steepness of curve and must be positive
    for large values of coef the return value will approach a discrete threshold functions
    '''
    if coef < 0:
        print ("Must input positive coef for logistic_signal_funct_pos_zero")
        return None
    exponent = (-1.0)*(coef*input)
    val = 1.0/(1.0 + pow(math.e, exponent))
    return val
    
def inverse_logistic_signal_funct_pos_zero(input, coef):
    if coef < 0:
        print ("Must input positive coef for inverse_logistic_signal_funct_pos_zero")
        return None
    numerator = math.log((1.0 - input)/input)
    val = numerator/(coef*-1)
    return val
    
def logistic_signal_funct_pos_neg(input, coef):
    ''' 
    a sigmoidal function that maps to [-1, 1], coef determines steepness of curve and must be positive
    for large values of coef the return value will approach a discrete threshold functions
    '''
    if coef < 0:
        print ("Must input positive coef for logistic_signal_funct")
        return None
    
    exponent = (-1)*(coef*input)
    val = 1.0/(1.0 + pow(math.e, exponent))
    return (val*2)-1

def no_func(input):
    return input

'''//////////////////////////////////////////////////
///
///    FCM REPRESENTATION SCHEMA MAP FUNCTIONS
///
//////////////////////////////////////////////////'''
def matrix_to_digraph(matrix):
        '''takes as input a dictionary of dictionaries 
        {key: concept, val: {key: neighbor, val: weight of link from concept --> neighbor}...}...} 
        representing the adjacency matrix for an fcm
        it returns the networkx.DiGraph representation'''
        
        digraph = nx.DiGraph()
        digraph.add_nodes_from(matrix.keys())
        for concept, val in matrix.items():
            for neighbor, weight in val.items():
                if weight != 0:
                    digraph.add_edge(concept, neighbor, {'weight': weight})
        return digraph
            
def digraph_to_matrix(digraph):
    '''takes as input a networkx.DiGraph representation of an FCM
    it returns the list of dictionaries representation of that fcm'''
    matrix = {}
    for concept in digraph.nodes_iter():
        matrix[concept] = {}
        for concept1 in digraph.nodes_iter():
            matrix[concept][concept1] = 0 

    for edge in digraph.edges_iter(data=True):
        matrix[edge[0]][edge[1]] = edge[2]['weight']
    return matrix
    


'''//////////////////////////////////////////////////
///
///    SOME FCM REPRESENTATIONS OF REDDIT DYNAMICS
///
//////////////////////////////////////////////////'''
def generate_reddit_digraph_1(initial_values = None):
    '''order of values of initial values must correspond to internal list "nodes" '''
    #nodes
    digraph = nx.DiGraph()
    nodes = ["Attention", "Time", "Score", "Ups", "Downs", 
             "Number_of_Comments", "Average_Branching_Factor", "Average_Max_Depth",  "Average_Comment_Length"]
    
    digraph.add_nodes_from(nodes)
    digraph.node["Attention"]['value']                  =    0
    digraph.node["Time"]['value']                       =   .1     #we want the effect of time to increase over course of simulation
    digraph.node["Score"]['value']                      =   .01
    digraph.node["Ups"]['value']                        =   .0
    digraph.node["Downs"]['value']                      =   .0
    digraph.node["Number_of_Comments"]['value']         =   .0
    digraph.node["Average_Branching_Factor"]['value']   =   .0
    digraph.node["Average_Max_Depth"]['value']          =   .0
    digraph.node["Average_Comment_Length"]['value']     =   .0
    
    if initial_values != None:
        for i in range(len(initial_values)):
            name = nodes[i]
            print name
            digraph.node[name]['value'] = initial_values[i]
    
    
    #edges
    
    edges = [("Attention",                  "Ups",                      {'weight': .66}),   #based upon ratio of ups/downs found in popular threads
             ("Attention",                  "Downs",                    {'weight': .33}),   #based upon ratio of ups/downs found in popular threads
             ("Ups",                        "Score",                    {'weight': 1}),     #Logical Correlation
             ("Downs",                      "Score",                    {'weight': -1}),    #Logical Correlation
             ("Score",                      "Attention",                {'weight': .25}),   #rough estimation based upon Reddit 'Hot' algorithm, should be less than time's effect on attention
             ("Attention",                  "Number_of_Comments",       {'weight': .2}),    #rough estimation
             
             ("Time",                       "Time",                     {'weight': .55}),   #as time progresses the number and rate of up votes that a post needs
             ("Time",                       "Attention",                {'weight': -.1}),     #in order to stay on the front page increases, the value of 55 was chosen to allow
                                                                                            #time to consistently increase over duration of simulation
             ("Number_of_Comments",         "Average_Max_Depth",        {'weight': .2}),    #Pearson-R
             ("Number_of_Comments",         "Average_Branching_Factor", {'weight': .15}),   #Pearson-R
             ("Number_of_Comments",         "Average_Comment_Length",   {'weight': .1}),    #Pearson-R
             ("Average_Max_Depth",          "Number_of_Comments",       {'weight': .2}),    #Pearson-R
             ("Average_Branching_Factor",   "Number_of_Comments",       {'weight': .15}),   #Pearson-R
             ("Average_Branching_Factor",   "Average_Max_Depth",        {'weight': .4}),    #Pearson-R
             ("Average_Max_Depth",          "Average_Branching_Factor", {'weight': .4}),    #Pearson-R
                
             #("Average_Max_Depth",          "Attention",                {'weight': .05}),   #Hypothesis 
             #("Average_Branching_Factor",   "Attention",                {'weight': .05}),   #Hypothesis
             ]
    #reflexive edges, give past value an affect on present value rather than just other concepts
    reflexive_weight = 0#1.0/len(nodes)
    for node in nodes:
        if node != "Time":
            edges.append((node, node, {'weight': reflexive_weight}))
    
    digraph.add_edges_from(edges)
    return digraph



if __name__ == "__main__":
    #if main is called the generate reddit digraph will run and a graph of the system will be printed
    print "RUNNING A SIMULATION OF THE PRE-PROGRAMMED REDDIT FCM"
    print "A LIST OF INITIAL CONCEPT VALUES AND EDGES SHOULD PRINT TO CONSOLE"
    print "A GRAPH MAPPING THE CHANGE OF THE SYSTEM OVER TIME SHOULD BE GENERATED"

    digraph = generate_reddit_digraph_1()
    
    #prepare parameters for saving graphics and data
    '''
    t = str(int(time.time()))
    experiment_name = "attention_negated%d" % exp_num
    path = "/Users/johndoty/Desktop/FCM_runs/%s" % experiment_name
    path_data = "/Users/johndoty/Desktop/FCM_runs/%s_data" % experiment_name
    f = open(path_data, 'a')
    '''
        
    #print initial values of nodes
    print "Initial value of system variables:\n"
    #f.write("Initial value of system variables:\n")
    for node in digraph.nodes_iter(data=True):
        s = node[0].ljust(30) + str(node[1]['value'])
        print s
        #f.write(s+'\n')
        
        
    print "\nValue of Causal Connections:"
    #f.write("\nValue of Causal Connections:")
    for edge in digraph.edges_iter(data=True):
        s = edge[0].ljust(30)
        s = s+(edge[1].ljust(30))
        r = round(edge[2]['weight'], 2)
        s = s + str(r)
        print s
        
            
    #digraph, threshold_function, t_func_params = None, dep_coef=1, past_coef=0, normalize_initial_values = True
    myFCM = FCM(digraph, logistic_signal_funct_pos_neg, 5, normalize_initial_values= False)
    myFCM.calculate_next_states(35)
    data = myFCM.get_state_time_series()
      
    #plot the time_series
    nodes = ["Attention", "Time", "Score", "Ups", "Downs", 
            "Number_of_Comments", "Average_Branching_Factor", "Average_Max_Depth",  "Average_Comment_Length"]
    x = range(len(data))
    y_vals = [[],[],[],[],[],[],[],[],[]]
    for item in data:
        for k in range(len(nodes)):
            y_vals[k].append(item[nodes[k]])
        
    myFont = font.FontProperties(size = 8)
    plt.figure(figsize = (14, 4))
    plt.hold(b=True)
    plt.plot(x, y_vals[0], 'ob-', label=nodes[0])
    plt.plot(x, y_vals[1], 'vg-', label=nodes[1])
    plt.plot(x, y_vals[2], '^r-', label=nodes[2])
    plt.plot(x, y_vals[3], 'sc-', label=nodes[3])
    plt.plot(x, y_vals[4], '*m-', label=nodes[4])
    plt.plot(x, y_vals[5], 'py-', label=nodes[5])
    plt.plot(x, y_vals[6], '+k-', label=nodes[6])
    plt.plot(x, y_vals[7], 'Db-', label=nodes[7])
    plt.plot(x, y_vals[8], '3r-', label=nodes[8])
    #plt.legend()
    plt.legend(bbox_to_anchor=(0, 0, 1, 1), prop=myFont)
    #plt.savefig(path)
    plt.show()
    #f.close()

    
    
    
    
    