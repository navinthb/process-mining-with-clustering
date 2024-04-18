import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
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

    return pairwise_distance_list, event_binary_matrix_np


# Performs Agglomerative heirachichal clustering with 
# a given given distance calculation method
def perform_hierarchical_clustering(pairwise_distance_list, method):
    
    # Perform hierarchical clustering using Average Linkage method
    clustered_flows = linkage(pairwise_distance_list, method=method)

    return clustered_flows


# Plot & save the dendogram for a given clustered flows
def generate_dendogram(clustered_flows, event_flows_df, col_name, title, xlabel, ylabel, save_location):

    # Plot the dendrogram using given parameters
    plt.figure(figsize=(50, 12))
    dendrogram(clustered_flows, labels=event_flows_df[col_name].tolist(),
                                leaf_rotation=90, leaf_font_size=8)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Save the dendrogram as a PNG file
    plt.savefig(save_location, dpi=300)


# calculate silhouette score values & plot for analysis
def plot_silhouette_scores(clustered_flows, event_binary_matrix_np):

    # Calculate silhouette scores for different numbers of clusters
    silhouette_score_list = []
    
    # Test is performed from 2-10 clsuters 
    # set max number of clusters as 10
    maximum_clusters = 10
    
    for cluster_count in range(2, maximum_clusters + 1):
        # Perform clustering
        cluster_sets = fcluster(clustered_flows, cluster_count, criterion='maxclust')
        # Calculate silhouette score
        silhouette_avg = silhouette_score(event_binary_matrix_np, cluster_sets)
        silhouette_score_list.append(silhouette_avg)

    # Find optimal number of clusterss based on the silhouette score
    opt_num_of_clusters = silhouette_score_list.index( max(silhouette_score_list)) + 2

    # Plot the silhouette scores
    plt.figure( figsize=(10, 8))
    plt.plot(range (2, maximum_clusters + 1), 
                      silhouette_score_list)
    plt.title('Silhouette Values for the Dataset')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Scores')
    plt.xticks(range(2, maximum_clusters + 1))
    plt.grid(True)
    plt.show()

    return opt_num_of_clusters



# calculate squared distances & plot for elbow analysis
def plot_elbow_method(clustered_flows, event_binary_matrix_np):

    # Calculate sum of squared distances for different numbers of clusters
    sum_of_squared_distance_list = []
    maximum_clusters = 10

    for cluster_count in range (1, maximum_clusters +  1):
        # Perform clustering
        cluster_sets = fcluster(clustered_flows, cluster_count, criterion='maxclust', )
        
        # Calculate cluster centroids
        centroid_list = []
        for cluster_id in range(1, cluster_count + 1):
            cluster_points = event_binary_matrix_np[cluster_sets == cluster_id]
            centroid = cluster_points.mean(axis=0)
            centroid_list.append(centroid)
        
        # Calculate sum of squared distances
        ssd = 0
        for cluster_id in range(1, cluster_count + 1):
            cluster_points = event_binary_matrix_np[cluster_sets == cluster_id]
            centroid = centroid_list[cluster_id - 1]
            distances = cdist(cluster_points, [centroid], metric='euclidean')
            ssd += np.sum(distances ** 2)
        
        sum_of_squared_distance_list.append(ssd)

    # Plot the elbow curve
    plt.figure(figsize=(10, 8))
    plt.plot(range(1, maximum_clusters + 1), 
                   sum_of_squared_distance_list,
                   marker='o')
    plt.title('Elbow Method Analysis')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Squared Distances (Sum)')
    plt.xticks(range(1, maximum_clusters + 1))
    plt.grid(True)
    plt.show()




# form clusters based on weights
def form_cluster_variants(event_flows_df, clustered_flows, num_of_clusters, max_variants):

    # Initialize clusters
    clusters = [[] for _ in range(num_of_clusters)]
    
    # Select event flows for cluster
    cluster_assignments = fcluster(clustered_flows, num_of_clusters, criterion='maxclust')
    
    # Append event flows to the respective cluster based on weights
    for i, group in event_flows_df.groupby(cluster_assignments):
        # Sort each group by weights
        group_sorted = group.sort_values(by='Weight', ascending=False).head(max_variants)
        clusters[i - 1].extend(group_sorted['Event Flow'].tolist())
    
    return clusters