#Madeline Spawn
#FCI Algorithm

import pandas as pd
import logging
import pingouin as pg

from PCAlgo import PC
from scipy.stats import pearsonr, spearmanr, chisquare
from datagenerator import generatedataframe

#retention data from: https://www.ccd.pitt.edu//wp-content/uploads/files/Retention.txt

def main():
    #create data
    #here B is dependent on A, with all other nodes independent
    generatedataframe(100, {'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': []}, 'testdata/binarytest.csv', 2)
    generatedataframe(100, {'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': []}, 'testdata/cardinality3test.csv', 3)
    generatedataframe(100, {'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': []}, 'testdata/cardinality4test.csv', 4)
    generatedataframe(100, {'A': ['B'], 'B': ['C'], 'C': [], 'D': ['E'], 'E': []}, 'testdata/cardinality100test.csv', 100)
    

    #load data
    #data2 = pd.read_csv('testdata/binarytest.csv', delimiter=',')
    #data3 = pd.read_csv('testdata/cardinality3test.csv', delimiter=',')
    # data4 = pd.read_csv('testdata/cardinality4test.csv', delimiter=',')
    data100 = pd.read_csv('testdata/cardinality100test.csv', delimiter=',')
    #retention = pd.read_csv('testdata/Retention.csv', delimiter=',')

    
    alpha = 0.025

    #run PC algorithm
    #pc = PC(data2, alpha, indtest=spearmanr, debug=True)
    #pc = PC(data3, alpha, indtest=spearmanr, debug=True)
    #pc = PC(data4, alpha, indtest=spearmanr, debug=True)
    pc = PC(data100, alpha, indtest=spearmanr, condindtest=pg.partial_corr, debug=True)
    #pc = PC(retention, alpha, indtest=spearmanr, debug=True)


    pc.runPC()
    

if __name__ == "__main__":
    main()



