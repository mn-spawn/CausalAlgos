#Madeline Spawn
#FCI Algorithm

import pandas as pd
from PCAlgo import PC
from scipy.stats import chi2
import logging

def main():

    #load data
    data = pd.read_csv('testdata/binarytest.csv', delimiter=',')
    # data = pd.read_csv('testdata/cardinality3test.csv', delimiter=',')
    # data = pd.read_csv('testdata/cardinality4test.csv', delimiter=',')

    alpha = 0.05

    #run PC algorithm
    pc = PC(data, alpha, indtest='chi2')
    pc.runPC()
    

if __name__ == "__main__":
    main()



