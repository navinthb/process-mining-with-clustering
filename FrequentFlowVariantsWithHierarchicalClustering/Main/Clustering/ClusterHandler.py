import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


# this calculates the distances among flows 
# using Jaccard similarity algorithm
def calculate_distances_with_jaccard(event_flows_df):
    
    # Covert data frame to a list
    event_flow_list = event_flows_df['Event Flow'].tolist()

    # Create an event list from the event flow list
    unique_flow_list = set()
    for flow in event_flow_list:
        unique_flow_list.update(flow)

    # Sort the events to ensure order
    unique_flow_list = sorted(unique_flow_list)

    # Now for each flow variant create a binary matrix representation of event pairs
    event_binary_matrix = []
    for flow in event_flow_list:
        binary_vector = [1 if event in flow else 0 for event in unique_flow_list]
        event_binary_matrix.append(binary_vector)

    # Convert the binary matrix into a numpy array
    event_binary_matrix_np = np.array(event_binary_matrix)

    # Calculate distances using Jaccard similarity
    pairwise_distance_list= pairwise_distances(event_binary_matrix_np, metric='jaccard')

    return pairwise_distance_list


# Performs Agglomerative heirachichal clustering with 
# a given given distance calculation method
def perform_hierarchical_clustering(pairwise_distance_list, method):
    
    # Perform hierarchical clustering using Average Linkage method
    clustered_flows = linkage(pairwise_distance_list, method=method)

    return clustered_flows


# Plot & save the dendogram for a given clustered flows
def generate_dendogram(clustered_flows, event_flows_df, col_name, title, xlabel, ylabel, save_figure_to):

    # Plot the dendrogram using given parameters
    plt.figure(figsize=(50, 12))  # Larger figsize for higher resolution
    dendrogram(clustered_flows, labels=event_flows_df[col_name].tolist(),
                                leaf_rotation=90, leaf_font_size=8)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Save the dendrogram as a PNG file
    plt.savefig(save_figure_to, dpi=300)