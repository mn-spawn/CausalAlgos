#Madeline Spawn
#FCI Algorithm
#An Anytime Algorithm for Causal Inference, Spirtes, 2001

class FCI:
    def __init__(self, V):
        self.V = V

    def completegraph(self):
        ''' 
        Input: vertices, V
        Output: complete graph, Q
        Purpose: Forms a complete graph between all vertices in V
        '''

        Q = self.V + 1
        return Q

    def edgepruning(self, Q):
        ''' 
        Input: Complete graph Q
        Output: 
        Purpose: 
        '''
        prunedgraph = Q + 1
        return prunedgraph

    def orientation(self, prunedgraph):
        ''' 
        Input: 
        Output: 
        Purpose: 
        '''
        orientedgraph = prunedgraph + 1
        return orientedgraph

    def dseparationpruning(self, orientedgraph):
        ''' 
        Input: 
        Output: 
        Purpose: 
        '''
        dsepgraph = orientedgraph + 1
        return dsepgraph 

    def orientationupdate(self, dsepgraph):
        ''' 
        Input: 
        Output: 
        Purpose: 
        '''
        updatedgraph = dsepgraph + 1
        return updatedgraph
        

    def tripleorientation(self, updatedgraph):
        ''' 
        Input: 
        Output: 
        Purpose:
        '''
      
        tripleorientedgraph = updatedgraph + 1
        return tripleorientedgraph

    def finalorientation(self, tripleorientedgraph):
        ''' 
        Input: 
        Output: 
        Purpose: 
        '''
        finalorientedgraph = tripleorientedgraph + 1
        return finalorientedgraph

    def runfci(self):
        ''' 
        Input: 
        Output: 
        Purpose: 
        '''
        
        Q = self.completegraph()
        prunedQ = self.edgepruning(Q)
        orientedQ = self.orientation(prunedQ)
        dsepQ = self.dseparationpruning(orientedQ)
        updatedQ = self.orientationupdate(dsepQ)
        tripleQ = self.tripleorientation(updatedQ)
        finalQ = self.finalorientation(tripleQ)

        return finalQ


    