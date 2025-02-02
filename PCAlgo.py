#Madeline Spawn
#PC Algorithm
#Causation, Prediction, and Search by Spirtes, Glymour, Scheines (pg. 116)
#Meeks Rules: https://proceedings.mlr.press/v89/katz19a/katz19a-supp.pdf

import networkx as nx
import logging
import itertools
import pingouin as pg
from pgmpy.estimators.CITests import g_sq
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
        self.sepset = dict()
        self.continueorienttation = True

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

        logging.info(f'Complete graph created with {len(G.nodes)} nodes and {len(G.edges)} edges')
              
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
                        Z = list(Z)
                        logging.debug(f"testing {Z} to sep set for {X},{Y}, p-value:{self.testindependence(X, Y, Z)}")

                        if self.testindependence(X, Y, Z) > self.alpha:
                            if self.skeletongraph.has_edge(X, Y):
                                logging.debug(f"removing {X} - {Y}")
                                self.skeletongraph.remove_edge(X, Y)

                            if Z:
                                logging.debug(f"adding {Z} to sep set for {X},{Y}")
                                self.sepset[(X,Y)] = Z
                                self.sepset[(Y,X)] = Z
                            else:
                                self.sepset[(X,Y)] = None
                                self.sepset[(Y,X)] = None
            depth +=1

        logging.info(f'Skeleton graph created with {len(self.skeletongraph.nodes)} nodes and {len(self.skeletongraph.edges)} edges')
        return 0;

    def orienttriples(self):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''

        self.dag = nx.DiGraph()

        for node in self.skeletongraph.nodes():
            self.dag.add_node(node)

        #find unshielded triples
        unshieldedtriples = self.unshieldedtriples()

        for (X, Y, Z) in unshieldedtriples:
            if (self.sepset[(X,Z)] != None and Y not in self.sepset[(X,Z)]) or self.sepset[(X,Z)] == None:
                #collider
                logging.debug(f"Add {X, Y} and {Z, Y}")#
                self.dag.add_edge(X, Y)
                self.dag.add_edge(Z, Y)
        
        logging.info(f"Triple orientation: DAG created with {len(self.dag.nodes)} nodes and {len(self.dag.edges)} edges")
        return 0

    def finalorientation(self, rule4="False"):
        ''' 
        Input: None
        Output: None
        Purpose: 
        '''
        
        undirectededges = {
            edges for edges in self.skeletongraph.edges
            if (edges[0], edges[1]) not in self.dag.edges and (edges[1], edges[0]) not in self.dag.edges
        }

        edges = undirectededges.copy()
        for edge in edges:
            undirectededges.add((edge[1], edge[0]))

        while self.continueorienttation:

            #Rule 1
            self.rule1(undirectededges)
                    
            #Rule 2
            self.rule2(undirectededges)

            #Rule 3
            self.rule3(undirectededges)

            if rule4:
                self.rule4(undirectededges)

        undirectededgescount = 0
        for (X,Y) in self.skeletongraph.edges:
            if (X,Y) not in self.dag.edges and (Y,X) not in self.dag.edges:
                self.dag.add_edge(X, Y)
                self.dag.add_edge(Y, X)
                undirectededgescount += 1
                        

        logging.info(f"Meeks Rules: DAG created with {len(self.dag.nodes)} nodes and {len(self.dag.edges)} edges (undirectable edges: {undirectededgescount} ... {len(self.dag.edges)-undirectededgescount} total edges)")
        return self.dag
       
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
        
        return  g_sq(X, Y, Z, self.data, boolean=False)[1]

        #if Z:
        #    result = pg.partial_corr(self.data, X, Y, covar=Z, method="spearman")
        #    #result = self.condindtest(self.data, X, Y, Z)
        #    return result['p-val'].values[0]
        #else:
        #    return self.indtest(self.data[X], self.data[Y])[1]

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

        unshieldedtriples = set()

        for X in self.skeletongraph.nodes():
            for Z in self.skeletongraph.nodes():
                if X != Z and not self.skeletongraph.has_edge(X, Z):  
                    Xneighbors = set(self.skeletongraph.neighbors(X))
                    Zneighbors = set(self.skeletongraph.neighbors(Z))

                    sharedneighbors = Xneighbors.intersection(Zneighbors)

                    # For each common neighbor, add the unshielded triple
                    for Y in sharedneighbors:
                        if Y != X and Y != Z: 
                            unshieldedtriples.add((X, Y, Z))

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
    
    def rule1(self, undirectededges):
        '''
        Input: None
        Output: None
        Purpose: Orient X - Y into  X -> Y when directed W -> X 
        '''

        self.continueorienttation = False
        oriented_edges_set = set()

        for (X,Y) in undirectededges:
            if (Y,X) not in self.dag.edges:
                if X not in self.dag.nodes:
                    logging.debug(f"X not in DAG: {X}")
                    continue
                else:
                    parentsX = list(self.dag.predecessors(X))
                    for W in parentsX:
                        if self.dag.has_edge(W, X):
                            self.dag.add_edge(X, Y)
                            oriented_edges_set.add((X,Y))
                            oriented_edges_set.add((Y,X))
                            logging.debug(f"orienting {X} -> {Y} because {W} -> {X}, logging rule 1")
                            self.continueorienttation = True
                            break

        undirectededges-=oriented_edges_set
        return 0
    
    def rule2(self, undirectededges):
        '''
        Input: None
        Output: None
        Purpose: X - Y is X -> Y when X -> Z and Z -> Y
        '''
        self.continueorienttation = False
        oriented_edges_set = set()
        
        for (X,Y) in undirectededges:
            if (Y,X) not in self.dag.edges:
                if X not in self.dag.nodes:
                    logging.debug(f"X not in DAG: {X}")
                    continue
                else:
                    childrenY = list(self.dag.successors(X))
                    for Z in childrenY:
                        if self.dag.has_edge(X, Z) and self.dag.has_edge(Z, Y):
                            self.dag.add_edge(X, Y)
                            oriented_edges_set.add((X,Y))
                            oriented_edges_set.add((Y,X))
                            logging.debug(f"orienting {X} -> {Y} because {X} -> {Z} and {Z} -> {Y} logging rule 2")
                            self.continueorienttation = True
                            break

        undirectededges-=oriented_edges_set
        return 0
    
    def rule3(self, undirectededges):
        '''
        Input: None
        Output: None
        Purpose: Orient X - Y into  X -> Y where W -> Y and Z -> Y
        '''
        self.continueorienttation = False
        oriented_edges_set = set()

        for (X,Y) in undirectededges:
            if (Y,X) not in self.dag.edges:
                if X not in self.dag.nodes:
                    logging.debug(f"X not in DAG: {X}")
                    continue
                else:
                    parents = list(self.dag.predecessors(X))
                    parentcombos = list(itertools.combinations(parents, 2))
                    for (W, Z) in parentcombos:
                        if self.dag.has_edge(W, X) and self.dag.has_edge(Z, X):
                            self.dag.add_edge(X, Y)
                            oriented_edges_set.add((X,Y))
                            oriented_edges_set.add((Y,X))
                            logging.debug(f"orienting {X} -> {Y} logging rule 3")
                            self.continueorienttation = True
                            break
        
        undirectededges-=oriented_edges_set
        return 0

    def rule4(self, undirectededges):
        '''
        Input: None
        Output: None
        Purpose: Orient X - Y into X -> Y where A -> B -> Y 
        '''
        self.continueorienttation = False
        oriented_edges_set = set()

        for (X,Y) in undirectededges:
            if (Y,X) not in self.dag.edges:
                if Y not in self.dag.nodes:
                    logging.debug(f"Y not in DAG: {Y}")
                    continue
                else:
                    parentsY = list(self.dag.predecessors(Y))
                    for parent in parentsY:
                        parentparents = list(self.dag.predecessors(parent))
                        if set(parentparents).intersection(set(self.skeletongraph.neighbors(X))) == None:
                            self.dag.add_edge(X, Y)
                            oriented_edges_set.add((X,Y))
                            oriented_edges_set.add((Y,X))
                            logging.debug(f"orienting {X} -> {Y} logging rule 4")
                            self.continueorienttation = True
                            break

        undirectededges-=oriented_edges_set
        return 0
             
