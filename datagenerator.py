import numpy as np
import pandas as pd
import networkx as nx
import numpy as np
import csv
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

def generate_domino_data(graph, alpha, beta, output_csv, num_samples=10000):
    """
    Generate domino-like model data for a directed graph and save it to a CSV file.

    Parameters:
        graph (networkx.DiGraph): A directed graph.
        alpha (float): Probability for root nodes to be 1.
        beta (float): Probability for child nodes to be 0 if at least one parent is 1 or to be 1 if all parents are zero.
        output_csv (str): Path to the output CSV file.

    Returns:
        None
    """
    # Ensure the graph is a directed acyclic graph (DAG)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("The input graph must be a directed acyclic graph (DAG).")

    # Get nodes in topological order
    topo_order = list(nx.topological_sort(graph))

    # Prepare to collect rows of data
    rows = []

    # Generate multiple samples (e.g., 10 samples for demonstration)
    for _ in range(num_samples):
        # Dictionary to store the value of each node for this sample
        node_values = {}

        # Iterate through nodes in topological order
        for node in topo_order:
            parents = list(graph.predecessors(node))

            if not parents:  # Root node
                node_values[node] = int(np.random.rand() < alpha)
            else:  # Non-root node
                if any(node_values[parent] for parent in parents):
                    node_values[node] = 1
                else:
                    node_values[node] = 0
                if np.random.rand() < beta:
                    node_values[node]=(node_values[node]-1)*-1

        # Append the values of nodes in topological order to rows
        rows.append([node_values[node] for node in topo_order])

    # Write rows to a CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header (node names)
        writer.writerow(topo_order)
        # Write data rows
        writer.writerows(rows)