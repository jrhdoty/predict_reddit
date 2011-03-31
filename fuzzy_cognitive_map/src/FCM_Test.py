'''
Created on Mar 9, 2011

@author: johndoty
'''
import unittest
import FCM
import matplotlib.pyplot as plt
import copy
import time
import networkx as nx

class FCM_Test(unittest.TestCase):
    
    node_list = [1, 2, 3, 4]
    #create simple adjacency list with no edges
    simple_matrix = {}
    for node in node_list:
        simple_matrix[node]={}
        for node1 in node_list:
            simple_matrix[node][node1] = 0
    
    #create simple digraph with no edges
    simple_digraph = nx.DiGraph()
    simple_digraph.add_nodes_from(node_list)
    
    def test_matrix_to_digraph(self):
        #add some edges to matrix
        matrix = copy.deepcopy(self.simple_matrix)
        matrix[1][2] = 1
        matrix[1][3] = 1
        matrix[1][4] = 1
        matrix[2][3] = 1
        #print out matrix with weighted edges
        '''for row in matrix.keys():
            print row, matrix[row]'''
        
        digraph = FCM.matrix_to_digraph(matrix)
        #nx.draw_circular(digraph)
        #plt.show()
        
    def test_digraph_to_matrix(self):
        #add some edges to digraph
        digraph = nx.DiGraph(self.simple_digraph)
        edges = [(1,2, {'weight': 1}), (2, 3, {"weight": 1}), (3, 4, {"weight": 1})]
        digraph.add_edges_from(edges)
        #nx.draw_circular(digraph)
        #plt.show()
        matrix = FCM.digraph_to_matrix(digraph)
        '''for row in matrix.keys():
            print row, matrix[row]'''
        
    def test_random_digraph_generator(self):
        '''tests the random FCM generator function'''
        print "Entering random FCM generator test"
        #generate_random_FCM(node_list, density_percent, seed, node_value_generator, edge_weight_generator)
        seed1 = 5
        seed2 = 7
        node_list = range(0,6)
        myFCM = FCM.generate_random_FCM(node_list, .5, seed2, FCM.pos_real, FCM.pos_neg_real)
        #print myFCM.nodes(data=True)
        #print myFCM.edges(data=True)
        
        
    def test_clear_functions(self):
        print "TEST CLEAR FUNCTIONS\n"
        digraph = nx.DiGraph(self.simple_digraph)
        edges = [(1,2, {'weight': 1}), (2, 3, {"weight": 1}), (3, 4, {"weight": 1})]
        digraph.add_edges_from(edges)
        for node in digraph.nodes():
            digraph.node[node]['value'] = 1
        
        n = {1: 5, 2: 5, 3: 5, 4: 5,}
        myFCM = FCM.FCM(digraph, FCM.bivalent_pos_zero)
        myFCM.clear_edges()
        myFCM.clear_nodes()
        print myFCM.get_edges()
        print myFCM.get_nodes()
        myFCM.set_nodes(n)
        myFCM.set_edges(edges)
        print myFCM.get_edges()
        print myFCM.get_nodes()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()