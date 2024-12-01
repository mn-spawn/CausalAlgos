#Madeline Spawn
#PC Algorithm
#Causation, Prediction, and Search by Spirtes, Glymour, Scheines (pg. 116)

import networkx as nx
import logging
import itertools
import pingouin as pg
import matplotlib.pyplot as plt

class PC:
    def __init__(self, data, alpha, indtest=callable, condindtest=callable, debug=False):
        self.data = data;
        self.V = data.columns
        self.alpha = alpha
        self.indtest = indtest
        self.condindtest = condindtest

        self.completegraph = None
        self.skeletongraph = None
        self.dag = None
        self.sepset = dict()
        self.unorientededges = []

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

                            if Z:
                                logging.debug(f"adding {Z} to sep set for {X},{Y}")
                                self.sepset[(X,Y)] = Z
                                self.sepset[(Y,X)] = Z
            depth +=1

        logging.info('Skeleton graph created with %d nodes and %d edges', len(self.skeletongraph.nodes), len(self.skeletongraph.edges))
        return 0;

    def orienttriples(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''

        self.dag = nx.DiGraph()

        #find unshielded triples
        unshieldedtriples = self.unshieldedtriples()

        for triple in unshieldedtriples:
            X, Z, Y = triple

            if (X,Z) in self.skeletongraph.edges and (Z,Y) in self.skeletongraph.edges and (X,Y) not in self.skeletongraph.edges:
                if self.testindependence(X, Z, Y) < self.alpha:          
                    self.dag.add_edge(X, Z)
                    self.dag.add_edge(Z, Y)
                else:
                    self.dag.add_edge(Z, X)
                    self.dag.add_edge(Z, Y)

        for edge in self.skeletongraph.edges:
            X, Y = edge
            if (X, Y) not in self.dag.edges and (Y, X) not in self.dag.edges:
                self.dag.add_edge(X, Y)  
                self.dag.add_edge(Y, X)
                self.unorientededges.append((X,Y))       

        return 0

    def finalorientation(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''

        #meeks rules
        logging.info('Number of unoriented edges: %d', len(self.unorientededges))
        self.visualizegraph(self.dag, directed=True)

        return 0
       
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
    
    def unshieldedtriples(self):
        ''' 
        Input: graph
        Output: set of unshielded triples
        Purpose: find and return unshielded triples in graph
        '''

        edges = self.skeletongraph.edges
        nodes = self.skeletongraph.nodes

        triples = list(itertools.combinations(nodes, 3))
        unshieldedtriples = set()
        
        for triple in triples:
            X, Y, Z = triple
            if (X,Y) in edges and (Y,Z) in edges and (X,Z) not in edges:
                unshieldedtriples.add(triple)

        return unshieldedtriples
    
    def visualizegraph(self, graph=None, directed=False):
        ''' 
        Input: graph
        Output: None
        Purpose: visualize graph
        '''
        logging.getLogger('matplotlib').setLevel(logging.ERROR)

        if graph is None:
            graph = nx.Graph(self.skeletongraph)

            nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=16, 
                font_weight="bold", edge_color='gray')

        else:
            pos = nx.spring_layout(graph, k=0.5, iterations=50) 
            plt.figure(figsize=(8, 8)) 

            if directed:
                graph = nx.DiGraph(graph)
                
                nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=16, 
                    font_weight="bold", edge_color='gray', arrowsize=20)
            else:    
                graph = nx.Graph(graph)
                nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=16, 
                    font_weight="bold", edge_color='gray')


        plt.title(str(graph))    
        plt.show()
  