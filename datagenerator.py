import numpy as np
import pandas as pd
import random 


def generatedataframe(samplenum, relationships, csv, cardinality=2):
    '''
    Input: 
        samplenum: number of samples to generate
        relationships: dictionary of nodes and their dependencies
        csv: file to write data to
        cardinality: number of possible values for each node
    Output: csv file with generated data
    Purpose: to generate data to allow for relationship testing
    '''

    data = []

    for i in range(samplenum):
        nodedata = {node: random.randint(0, (cardinality-1)) for node in relationships.keys()}

        for node, dependencies in relationships.items():
            value = nodedata[node]

            for dep in dependencies:
                    adjustedvalue = value + random.randint(-5, 5)
                    nodedata[dep] = max(0, min(cardinality-1, adjustedvalue))
    
        data.append(nodedata)
    
    df = pd.DataFrame(data)
    df.to_csv(csv, index=False)

    return 0
