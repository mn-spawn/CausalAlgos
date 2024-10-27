#Madeline Spawn
#FCI Algorithm

import pandas as pd
import logging

from PCAlgo import PC
from scipy.stats import pearsonr, spearmanr
from datagenerator import generatedataframe


def main():
    #create data
    #here B is dependent on A, with all other nodes independent
    generatedataframe(100, {'A': ['B'], 'B': [], 'C': [], 'D': []}, 'testdata/binarytest.csv', 2)
    generatedataframe(100, {'A': ['B'], 'B': [], 'C': [], 'D': []}, 'testdata/cardinality3test.csv', 3)
    generatedataframe(100, {'A': ['B'], 'B': [], 'C': [], 'D': []}, 'testdata/cardinality4test.csv', 4)
    generatedataframe(100, {'A': ['B'], 'B': [], 'C': [], 'D': []}, 'testdata/cardinality100test.csv', 100)
    

    #load data
    #data2 = pd.read_csv('testdata/binarytest.csv', delimiter=',')
    #data3 = pd.read_csv('testdata/cardinality3test.csv', delimiter=',')
    # data4 = pd.read_csv('testdata/cardinality4test.csv', delimiter=',')
    data100 = pd.read_csv('testdata/cardinality100test.csv', delimiter=',')

    
    alpha = 0.05

    #run PC algorithm
    pc = PC(data100, alpha, indtest=spearmanr)
    pc.runPC()
    

if __name__ == "__main__":
    main()



