from data_loading import get_log_close_values
import os

import networkx as nx
import numpy as np

class ClusteringModel:

    def __init__(self, tickers) -> None:
        self.tickers = tickers
        self.data_path = r'../data/ohlc-us/'
        self.adjacency_matrix = None #saving adjacency matrix for clustering
    
    def create_graph(self, tickers):
        available_tickers = [ticker for ticker in tickers if f'{ticker.lower()}.us.txt'
                              in os.listdir(self.data_path)]

        # Initialize an empty adjacency matrix
        adjacency_matrix = np.zeros((len(available_tickers), len(available_tickers)))

        # Calculate the DDTW distance for each pair of tickers
        for i in range(len(available_tickers)):
            for j in range(i+1, len(available_tickers)):
                seq1 = get_log_close_values(available_tickers[i])
                seq2 = get_log_close_values(available_tickers[j])
                ddtw_distance = ddtw_distance(seq1, seq2, K = 500)
                adjacency_matrix[i][j] = ddtw_distance
                adjacency_matrix[j][i] = ddtw_distance  # because DDTW is a symmetric measure

        # Create a graph from the adjacency matrix
        G = nx.from_numpy_matrix(adjacency_matrix)

        # Label nodes with the correct ticker names
        label_mapping = {i: ticker for i, ticker in enumerate(available_tickers)}
        G = nx.relabel_nodes(G, label_mapping)
        available_tickers_idx = {available_tickers[i]:i for i in range(len(available_tickers))}

        # Set edge weights
        for i, j in G.edges():
            G[i][j]['weight'] = adjacency_matrix[available_tickers_idx[i]][available_tickers_idx[j]]

        return adjacency_matrix, G