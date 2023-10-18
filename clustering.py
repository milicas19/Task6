
from datetime import datetime
import os
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm

from igraph import Graph
import leidenalg

from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score

from cell import Cell

CONST = 5000

############ CREATING DISTANCE MATRIX AND GRAPH ############

def get_distance_matrix(cells, distance_matrix_name, type="coordinate", neighborhood_radius=None, dist="Manhattan", param=None):
    if type == "coordinate":
        matrix_name = f"{type}_{distance_matrix_name}"
    else: # percentage
        param_str = ""
        if dist == "Hamming":
            param_str = re.sub(r'\.', '', str(param))
            param_str = f"_param_{param_str}"
        matrix_name = f"{type}_{distance_matrix_name}_radius_{neighborhood_radius}_dist_{dist}{param_str}"
    if os.path.exists(f"matrices/{matrix_name}.npy"):
        print(f"###### Distance matrix {matrix_name} already exists. Fetching it.")
        return np.load(f"matrices/{matrix_name}.npy")
    else:
        start_time = datetime.now()
        print(f"====== Creating {type} distance matrix {matrix_name} . . .")
        
        n = len(cells)
        distance_matrix =  np.zeros((n, n), dtype=float) 
        
        if type == "coordinate":
            for i in range(0, n - 1):
                if i % CONST == 0:
                        print(f"Progress for creating distance matrix: {i}/{n}")
                for j in range(i + 1, n):
                    distance_matrix[i][j] = cells[i].coordinate_distance_to(cells[j])
                    distance_matrix[j][i] = distance_matrix[i][j]
        else: # percentage
            for i in range(0, n - 1):
                if i % CONST == 0:
                    print(f"Progress for creating distance matrix: {i}/{n}")
                for j in range(i + 1, n):
                    distance_matrix[i][j] = cells[i].percentage_distance_to(cells[j], dist, param)
                    distance_matrix[j][i] = distance_matrix[i][j]

        print(f"Distance matrix {matrix_name} created. Saving it . . .")
        if not os.path.exists('matrices'):
            os.makedirs('matrices')
        np.save(f"matrices/{matrix_name}.npy", distance_matrix)
        
        upper_triangle_array = distance_matrix[np.triu_indices(distance_matrix.shape[0], k=1)]
        plot_values(upper_triangle_array, f"allDistances_{matrix_name}", "Distances", "Number of cell pairs with specified distance", f"MEAN: {np.mean(upper_triangle_array)}")
        
        print(f"###### job completed in: {datetime.now() - start_time}")
        return distance_matrix

def create_reduced_graph(graph_name, distance_matrix, num_of_closest_neighbors):
    if os.path.exists(f"graphs/{graph_name}"):
        print(f"Graph {graph_name} exits. Fetching it . . .")
        return Graph.Read_GraphML(f"graphs/{graph_name}")
    else:
        start_time = datetime.now()
        print(f"====== Creating graph {graph_name}. . .")
        
        reduced_graph = Graph()

        num_of_vertices = len(distance_matrix)
        reduced_graph.add_vertices(num_of_vertices)

        for i in range(num_of_vertices):
            if i % CONST ==0:
                print(f"Progress: {i}/{num_of_vertices}")
            neighbors = [(j, weight) for j, weight in enumerate(distance_matrix[i]) if i != j]
            neighbors.sort(key=lambda x: x[1])
            for j, weight in neighbors[:num_of_closest_neighbors]:
                reduced_graph.add_edge(i, j, weight=weight)
        
        # graph = Graph.Weighted_Adjacency(distance_matrix, mode='undirected', attr='weight', loops=False)
        
        print(f"Saving graph {graph_name} . . .")
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        reduced_graph.write_graphml(f"graphs/{graph_name}")
        
        print(f"###### job completed in: {datetime.now() - start_time}")
        return reduced_graph

############ PLOT FUNCTIONS ############

def plot_cluster_stats(y_values, name, xlabel, ylabel):
    x_values = np.arange(len(y_values))

    plt.bar(x_values, y_values, width=0.8, align='center')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(name)
    
    plt.close()
    
def plot_values(data_array, name, xlabel, ylabel, text="", bins = 100):
    plt.hist(data_array, bins)

    plt.title(text)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(name)
    
    plt.close()
    
def plot_legend(colors, name):
    figure, ax = plt.subplots()
    
    legend_elements = []
    
    for cluster in colors:
        color = colors[cluster]
        legend_elements.append(patches.Patch(color=color, label=f'{cluster}'))
        
    ax.legend(handles=legend_elements, loc='upper right')
    
    print(f"Saving legend for {name} . . .")
    figure.savefig(f"legend_for_{name}.png")
    
    plt.close()

def plot_clusters(clusters, cells, node_colors, name, radius, text):
    start_time = datetime.now()
    print("====== Plotting clusters . . .")
    
    figure, ax = plt.subplots()
    ax.set_aspect('equal')
    
    n = len(cells)
    colors = {}
    
    for cell in cells:
        if cell.id_num == 0:
            circle = patches.Circle((cell.x, cell.y), radius=radius, edgecolor='red', facecolor='none')
            ax.add_patch(circle)
        elif cell.id_num % CONST == 0:
            print(f"Progress for plotting clusters: {cell.id_num}/{n}")
        x = cell.x
        y = cell.y
        color = node_colors[cell.id_num]
        if clusters[cell.id_num] not in colors:
            colors[clusters[cell.id_num]] = color
        
        ax.scatter(x, y, color=color, s=0.5, alpha=1)

    plot_legend(colors, name)
    
    ax.set_title(text)
    ax.set_xlabel("cell x coordinate")
    ax.set_ylabel("cell y coordinate")
        
    if "embryo" in name:
        ax.invert_yaxis()
        
    print(f"Saving plot for {name} . . .")
    figure.savefig(f"clusters_for_{name}.png")
    plt.close()
    
    print(f"###### job completed in: {datetime.now() - start_time}")
    
############ LEIDEN CLUSTERING ############

def cluster_leiden(graph, cells, name, radius, distance_matrix, num_of_types):
    start_time = datetime.now()
    print("====== Started Leiden clustering . . .")
    
    partition = leidenalg.find_partition(graph=graph, partition_type=leidenalg.ModularityVertexPartition, n_iterations=-1, seed=0)
    num_clusters = len(set(partition.membership))
    
    print(f"Modularity: {partition.modularity:.3f}")
    print(f"Number of clusters: {num_clusters}")

    color_map = cm.get_cmap('tab20c', num_clusters)
    colors = [color_map(i) for i in range(num_clusters)]
    
    node_colors = [colors[cluster] for cluster in partition.membership]
    text = f"modularity: {partition.modularity:.3f} number_of_clusters:{num_clusters}"
    plot_clusters(partition.membership, cells, node_colors, name, radius, text)
    
    clusters_stat(partition.membership, num_of_types, cells, distance_matrix, name)
    
    print(f"###### job completed in: {datetime.now() - start_time}")
    return partition.membership

############ AGGLOMERATIVE CLUSTERING ############

def cluster_agglomerative(distance_matrix, cells, name, radius, num_of_types, linkage_method, threshold=None):
    start_time = datetime.now()
    print("====== Started Agglomerative clustering . . .")
    
    if os.path.exists(f"linkage_matrix/{name}.npy"):
        print(f"Linkage matrix {name} already exists. Fetching it.")
        linkage_matrix = np.load(f"linkage_matrix/{name}.npy")
    else:
        print(f"Creating linkage matrix {name} . . .")
        linkage_matrix = linkage(distance_matrix, method=linkage_method)
        if not os.path.exists("linkage_matrix"):
            os.makedirs("linkage_matrix") 
        np.save(f"linkage_matrix/{name}.npy", linkage_matrix)
        print(f"Linkage matrix {name} created . . .")
        
    max_linkage_value = linkage_matrix[:, 2].max()
    print(f"Maximum Linkage Value: {max_linkage_value}")
    
    divide_by = [10, 8, 6, 4, 2, 1.5, 1.2]
    thresholds = [max_linkage_value/d for d in divide_by]
    
    if threshold == None:
        print("Threshold is not given. Calculating optimal threshold . . .")
        max_score = 0
        for threshold in thresholds:
            print(f"Calculating clusters for threshold {threshold} . . .")
            clusters = fcluster(linkage_matrix, t=threshold, criterion='distance')
            print(f"Number of clusters: {len(set(clusters))}")
            score = silhouette_score(distance_matrix, clusters, metric='precomputed')
            if score > max_score:
                max_score = score
                optimal_threshold = threshold
                optimal_clusters = clusters
    else:
        optimal_clusters = fcluster(linkage_matrix, t=threshold, criterion='distance')
        max_score = silhouette_score(distance_matrix, optimal_clusters, metric='precomputed')
        optimal_threshold = threshold
    
    
    num_clusters = len(set(optimal_clusters))
    optimal_clusters = np.array(optimal_clusters)
    optimal_clusters -= 1
    
    print(f"Optimal number of clusters: {num_clusters}")

    color_map = cm.get_cmap('tab20c', num_clusters)
    colors = [color_map(i) for i in range(num_clusters)]
    
    node_colors = [colors[cluster] for cluster in optimal_clusters]
    text = f"silhouette_score: {max_score:.3f} number_of_clusters:{num_clusters}"
    plot_clusters(optimal_clusters, cells, node_colors, f"{name}_threshold_{int(optimal_threshold)}", radius, text)
    
    clusters_stat(optimal_clusters, num_of_types, cells, distance_matrix, f"{name}_threshold_{int(optimal_threshold)}")
    
    print(f"###### job completed in: {datetime.now() - start_time}")
    return optimal_clusters

############ CLUSTER STATISTICS ############    

def is_cluster_homogeneous(cluster, cell_ids, percentage_distance_matrix, name):
    start_time = datetime.now()
    print(f"====== Calculate if cluster {cluster} is homogeneous. . .")
    
    n = len(cell_ids)
    distances = []
    
    for i in range(n-1):
        for j in range(i + 1, n):
            distances.append(percentage_distance_matrix[cell_ids[i]][cell_ids[j]])
    
    print(f"cluster distances MEAN: {np.mean(distances)}")
    
    plot_values(distances, f"{name}_isHomogeneous_cluster_{cluster}", "Distances", "Number of cell pairs with specified distance", f"cluster {cluster} distances -> MEAN: {np.mean(distances)}")
    print(f"###### job completed in: {datetime.now() - start_time}")
    
    return distances
    
def cluster_stat(cluster, cell_ids, num_of_types, cells, percentage_distance_matrix, name):
    start_time = datetime.now()
    print(f"====== Calculate cluster {cluster} stats . . .")
    
    type_count = np.zeros(num_of_types)
    cell_num = len(cell_ids)
    
    for cell_id in cell_ids:
        type_count[cells[cell_id].type_num] += 1
    
    types_percentage = type_count / cell_num
    
    plot_cluster_stats(type_count, f"{name}_typeCount_cluster_{cluster}", "Type number", "Number of cells with specified type")
    plot_cluster_stats(types_percentage, f"{name}_typePercentage_cluster_{cluster}", "Type number", "Percentage of cells with specified type")
    is_cluster_homogeneous(cluster, cell_ids, percentage_distance_matrix, f"{name}_isHomogeneous_cluster_{cluster}")
        
    print(f"###### job completed in: {datetime.now() - start_time}")
    return type_count, types_percentage

def clusters_stat(clusters, num_of_types, cells, percentage_distance_matrix, name):
    start_time = datetime.now()
    print("====== Calculate clusters stats . . .")
    
    upper_triangle_values = percentage_distance_matrix[np.triu_indices_from(percentage_distance_matrix, k=1)]
    print(f"all distances MEAN: {np.mean(upper_triangle_values)}")
    
    clusters_dict = {}
    
    for i, cluster in enumerate(clusters):
        if cluster not in clusters_dict:
            clusters_dict[cluster] = []
        clusters_dict[cluster].append(i)
        
    for cluster in clusters_dict:
        cell_ids = clusters_dict[cluster]
        cluster_stat(cluster, cell_ids, num_of_types, cells, percentage_distance_matrix, name)
    
    print(f"###### job completed in: {datetime.now() - start_time}")

########################

def get_cells_and_types(data):
    start_time = datetime.now()
    print("====== Get cells and types from data . . .")
    
    types = {}
    cells = []
    i = 0
    n = len(data)
    for index, row in data.iterrows():
        if index % CONST == 0:
            print(f"Progress : {index}/{n}")
        if row['sim anno'] not in types:
            types[row['sim anno']] = i
            i += 1
        cell = Cell(row['cell_ID'], index, row['sim anno'], types[row['sim anno']], row['x'], row['y'])
        cells.append(cell)
        
    print(f"###### job completed in: {datetime.now() - start_time}")
    return cells, types

def set_types_percentage_for_all_cells(cells, num_of_types, filename, neighborhood_radius):
    start_time = datetime.now()
    print("====== Set types_percentage for all cells . . .")
    
    distance_matrix = get_distance_matrix(cells, filename)
    n = len(cells)
    for cell in cells:
        if cell.id_num % CONST == 0:
            print(f"Progress for calculating types percentage for all cells: {cell.id_num}/{n}")
        cell.set_types_percentage(cells, num_of_types, distance_matrix, neighborhood_radius)

    print(f"###### job completed in: {datetime.now() - start_time}")

############ CLUSTERING ############

def clustering(filename, neighborhood_radius, dist="Manhattan", hamming_param=0.3, cluster_alg = "leiden", linkage_method="single", threshold= None, num_of_closest_neighbors=20):
    start_time = datetime.now()
    agglomerative_params = ""
    if cluster_alg == "agglomerative":
        agglomerative_params = f"{agglomerative_params}_linkageMethod_{linkage_method}"
    name = f"{filename}_radius_{neighborhood_radius}_clusterAlg_{cluster_alg}{agglomerative_params}_dist_{dist}"
    if dist == "Hamming":
        param_str = re.sub(r'\.', '', str(hamming_param))
        name =f"{name}_param_{param_str}"
    if cluster_alg == "leiden":
        name =f"{name}_closestNeighbors_{num_of_closest_neighbors}"

    print(f"=== Clustering {name}. . .")
    
    data = pd.read_csv(f"{filename}.csv")
    
    cells, types = get_cells_and_types(data)
    num_of_types = len(types)
    set_types_percentage_for_all_cells(cells, num_of_types, filename, neighborhood_radius)

    percentage_distance_matrix = get_distance_matrix(cells, filename, "percentage", neighborhood_radius, dist, hamming_param)
    
    if cluster_alg == "leiden":
        graph = create_reduced_graph(name, percentage_distance_matrix, num_of_closest_neighbors)
        clusters = cluster_leiden(graph, cells, name, neighborhood_radius, percentage_distance_matrix, num_of_types)
    else:
        clusters = cluster_agglomerative(percentage_distance_matrix, cells, name, neighborhood_radius, 
                                        num_of_types, linkage_method, threshold)
    
    if not os.path.exists(f"clusters_folder"):
        os.makedirs(f"clusters_folder")
    np.save(f"clusters_folder/{name}.npy", np.array(clusters))
    
    print(f"### job completed in: {datetime.now() - start_time}")
    
