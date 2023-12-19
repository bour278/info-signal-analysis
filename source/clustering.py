from data_loading import get_log_close_values
from equity_names import Equity
import os

import networkx as nx
from sklearn.cluster import KMeans
import numpy as np
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.offline as pyo

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

        # Label nodes with the correct aticker names
        label_mapping = {i: ticker for i, ticker in enumerate(available_tickers)}
        G = nx.relabel_nodes(G, label_mapping)
        available_tickers_idx = {available_tickers[i]:i for i in range(len(available_tickers))}

        # Set edge weights
        for i, j in G.edges():
            G[i][j]['weight'] = adjacency_matrix[available_tickers_idx[i]][available_tickers_idx[j]]

        return adjacency_matrix, G
    
    def initialize_nodes_edges(self, G):
        edge_x = []
        edge_y = []

        pos = nx.spring_layout(G)

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node, pos in pos.items():
            x, y = pos
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
        
        return edge_x, edge_y, node_x, node_y
    
    def cluster_and_visualize(self, algorithm='kmeans', num_clusters=6):
        adjacency_matrix, G = self.create_graph(self.tickers)

        edge_x, edge_y, node_x, node_y = self.initialize_nodes_edges(G)

        pos = nx.spring_layout(G)
        node_positions = [pos[node] for node in G.nodes()]

        if algorithm == 'kmeans':
            # Apply K-Means clustering to the node positions
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            node_clusters = kmeans.fit_predict(node_positions)
            title = 'Node Communities'
        elif algorithm == 'louvain':
            # Apply Louvain clustering
            node_clusters = list(nx.community.best_partition(G).values())
            title = 'Node Communities (Louvain)'

        # Create a colormap for coloring nodes based on their cluster
        colormap = ['red', 'lightblue', 'lightgreen', 'purple', 'orange', 'pink', 'cyan', 'pink', 'orchid']
        node_colors = [colormap[cluster % len(colormap)] for cluster in node_clusters]

        # Rest of the code for generating edge_trace

        # Create a scatter trace for nodes with colors based on their cluster
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',  # Display hover text
            hovertext=[Equity[equity].value for equity in self.tickers],  # Use equity names as hover text
            text=self.tickers,  # Use equity symbols as node labels
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                color=node_colors,  # Use the community colors
                size=30,
                colorbar=dict(
                    thickness=15,
                    title=title,  # You can change the title
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Add edge_trace and modified node_trace to the data list
        data = [edge_trace, node_trace]

        layout = go.Layout(
            showlegend=False,
            hovermode='closest',
            title=f'{algorithm} Clustering of Equities Network'
        )

        # Create the figure and display or save the graph
        fig = go.Figure(data=data, layout=layout)

        # Display the graph (in a Jupyter Notebook) or save it to an HTML file
        pyo.iplot(fig)