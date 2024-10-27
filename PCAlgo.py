#Madeline Spawn
#PC Algorithm
#Causation, Prediction, and Search by Spirtes, Glymour, Scheines (pg. 116)

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
        self.sepset = dict()

        self.dag = None

        logging.getLogger().setLevel(logging.INFO)

    def getcomplete(self):
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

    def getskeleton(self):
        ''' 
        Input: None
        Output: skeleton graph in self.skeleton
        Purpose: Output graph with edges that are not significant
        '''

        self.skeletongraph = self.completegraph.copy()
        depth = 0
        Z = None

        # until for each ordered pair of adjacent vertices X, Y, Adjacencies(C,X)\{Y} is
        # of cardinality less than n.
        while depth <1:    #adj(X, G)\{Y }| > d for every pair of adjacent vertices in G;
            for edge in self.skeletongraph.edges:
                X, Y = edge
                #if (|adj(X, G)\{Y }| >= d) then
                    #for each subset Z ⊆ adj(X, G)\{Y } and
                if  self.testindependence(X, Y, Z) > self.alpha:
                    self.skeletongraph.remove_edge(X, Y)
                    if Z:
                        self.sepset[(X,Y)] = Z
                        self.sepset[(Y,X)] = Z
            depth +=1

        print(self.skeletongraph.edges)
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

        self.getcomplete()
        self.getskeleton()
        self.orienttriples()
        self.finalorientation()

        return self.dag
    
    #----------------Helper Functions----------------#   

    def testindependence(self, X, Y, Z):
        ''' 
        Input: X, Y, Z
        Output: p-value
        Purpose: handle different tests + return p-value
        '''

        if str(self.indtest.__name__) == 'pearsonr' or 'spearmanr':
            if Z:
                return self.indtest(self.data[X], self.data[Y], self.data[Z])[1]     
            return self.indtest(self.data[X], self.data[Y])[1]
    


        logging.error('Independence test not recognized')

        return 0