#Madeline Spawn
#PC Algorithm
#Causation, Prediction, and Search by Spirtes, Glymour, Scheines (pg. 116)

import networkx as nx
import logging
import itertools
import pingouin as pg

class PC:
    def __init__(self, data, alpha, indtest=callable, condindtest=callable, debug=False):
        self.data = data;
        self.V = data.columns
        self.alpha = alpha
        self.indtest = indtest
        self.condindtest = condindtest

        self.completegraph = None
        self.skeletongraph = None
        self.sepset = dict()

        self.dag = None

        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def getcomplete(self):
        ''' 
        Input: None
        Output: complete graph, G
        Purpose: obtain and store complete graph
        '''
        G = nx.DiGraph()

        for i, node in enumerate(self.V):
            G.add_node(node)
            for j in range(i + 1, len(self.V)):
                G.add_edge(node, self.V[j])
                G.add_edge(self.V[j], node)

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
        edges = list(self.skeletongraph.edges)
        depth = 0
        Z = None
        numnodes = len(self.skeletongraph.nodes)

        while self.adjgreaterthandepth(self.skeletongraph, depth) and depth < numnodes-1: 
            edges = list(self.skeletongraph.edges)
            for edge in edges:
                X, Y = edge
                neighbors = list(self.skeletongraph.neighbors(Y))

                if len(neighbors) > depth:
                    neighborsexcludeX = [node for node in neighbors if node != X]

                    for Z in itertools.combinations(neighborsexcludeX, depth):
                        Z = set(Z)
                        if  self.testindependence(X, Y, Z) > self.alpha:
                            if self.skeletongraph.has_edge(X, Y):
                                logging.debug(f"removing {X} - {Y}")
                                self.skeletongraph.remove_edge(X, Y)
                                self.skeletongraph.remove_edge(Y, X)

                            if Z:
                                logging.debug(f"adding {Z} to sep set for {X},{Y}")
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

        self.dag = self.skeletongraph.copy()
        edges = list(self.dag.edges)

        #find unshielded triples


        #orient triples



        return 0;

    def finalorientation(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''
        return 0;

        #meeks rules

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
        
        if Z:
            result = pg.partial_corr(self.data, X, Y, covar=Z)
            #result = self.condindtest(self.data, X, Y, Z)
            return result['p-val'].values[0]
        else:
            return self.indtest(self.data[X], self.data[Y])[1]

    def adjgreaterthandepth(self, graph, d):
        '''
        Input: graph, depth 
        Output: True/False
        Purpose: check if adajcent nodes have depth greater than d
        '''

        for edge in graph.edges:
            X, Y = edge
            if len(list(graph.neighbors(Y))) > d:
                return True
            
        return False