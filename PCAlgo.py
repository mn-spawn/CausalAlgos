#Madeline Spawn
#PC Algorithm
#https://arxiv.org/pdf/1502.02454

import networkx as nx
import logging

class PC:
    def __init__(self, data, alpha, indtest=callable):
        self.data = data;
        self.V = data.columns
        self.alpha = alpha
        self.indtest = indtest

        self.completegraph = None
        self.skeletongraph = None
        self.sepset = {}

        self.dag = None

        logging.getLogger().setLevel(logging.INFO)


    def complete(self):
        ''' 
        Input: None
        Output: complete graph, G
        Purpose: obtain and store complete graph
        '''
        G = nx.Graph()

        for i, node in enumerate(self.V):
            G.add_node(node)
            for j in range(i + 1, len(self.V)):
                G.add_edge(node, self.V[j])

        logging.info('Complete graph created with %d nodes and %d edges', len(G.nodes), len(G.edges))
                   
        self.completegraph = G
        return 0;

    def skeleton(self):
        ''' 
        Input: None
        Output: skeleton graph in self.skeleton
        Purpose: Output graph with edges that are not significant
        '''
        depth = 0
        self.skeletongraph = self.completegraph.copy()

        for edge in self.skeletongraph.edges:
            print(edge)
            for i in range(1):
                print(depth)
                #check adjacenies and ind test
            #check cardinality

            depth +=1

        logging.info('Skeleton graph created with %d nodes and %d edges', len(self.skeletongraph.nodes), len(self.skeletongraph.edges))
        return 0;

    def orienttriples(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''
        return 0;

    def finalorientation(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''
        return 0;


    def runPC(self):
        ''' 
        Input: None 
        Output: DAG
        Purpose: run the steps of the PC algorithm
        '''

        self.complete()
        self.skeleton()
        self.orienttriples()
        self.finalorientation()

        return self.dag
    


     