import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm

import os
import re
from igraph import Graph
import leidenalg
from datetime import datetime

from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import pdist, euclidean, cityblock, jaccard

CONST = 5000

class Cell:
    
    def __init__(self, cell_id, cell_num, cell_type, cell_type_num, x, y):
        self.id = cell_id
        self.id_num = cell_num
        self.cell_type = cell_type
        self.cell_type_num = cell_type_num
        self.type_percentage = None
        self.x = x
        self.y = y
    
    def set_type_percentage(self, cells, types, distance_matrix, neighborhood_diameter):
        """
        Calculate the percentage of cell types in neighborhood of 
        this cell and set it as a type_percentage parameter.
        """
        self.type_percentage = np.zeros(len(types))
        self.type_percentage[self.cell_type_num] += 1
        
        num_of_cells_in_neighborhood = 1
        for cell in cells:
            if distance_matrix[self.id_num][cell.id_num] < neighborhood_diameter:
                self.type_percentage[cell.cell_type_num] += 1
                num_of_cells_in_neighborhood += 1
                
        self.type_percentage /= num_of_cells_in_neighborhood

    def coordinate_distance_to(self, other_cell):
        """
        Calculate the Euclidean distance between this cell and another cell.
        """
        return euclidean([self.x, self.y], [other_cell.x, other_cell.y])
    
    def percentage_distance_to(self, other_cell, dist="Manhattan", param=None):
        """
        Calculate the similarity (distance) between percentage 
        of types of this cell and another cell.
        """
        if dist == "Manhattan":
            return cityblock(self.type_percentage, other_cell.type_percentage)
        elif dist == "Jaccard":
            p_this_cell = [1 if p > param else 0 for p in self.type_percentage]
            p_other_cell = [1 if p > param else 0 for p in other_cell.type_percentage]
            return jaccard(p_this_cell, p_other_cell)
        else: #euclidean
            return euclidean(self.type_percentage, other_cell.type_percentage)
        
def get_distance_matrix(cells, distance_matrix_name, type="coordinate", neighborhood_diameter=None, dist="Manhattan", param=None):
    paramStr = None
    if param != None:
        paramStr = re.sub(r'\.', '', str(param))
    matrix_name = f"{type}_{distance_matrix_name}_diameter_{neighborhood_diameter}_dist_{dist}_param_{paramStr}"
    if os.path.exists(f"matrices/{matrix_name}.npy"):
        print(f"====== Distance matrix {matrix_name} already exists. Fetching it.")
        return np.load(f"matrices/{matrix_name}.npy")
    else:
        start_time = datetime.now()
        print(f"====== Creating {type} distance matrix {type}_{distance_matrix_name} . . .")
        
        n = len(cells)
        distance_matrix =  np.zeros((n, n), dtype=float) 
        
        if type == "coordinate":
            for i in range(0, n - 1):
                if i % CONST == 0:
                        print(f"Progress for creating distance matrix: {i}/{n}")
                for j in range(i + 1, n):
                    distance_matrix[i][j] = cells[i].coordinate_distance_to(cells[j])
                    distance_matrix[j][i] = distance_matrix[i][j]
        else:
            for i in range(0, n - 1):
                if i % CONST == 0:
                    print(f"Progress for creating distance matrix: {i}/{n}")
                for j in range(i + 1, n):
                    distance_matrix[i][j] = cells[i].percentage_distance_to(cells[j], dist, param)
                    distance_matrix[j][i] = distance_matrix[i][j]

        print(f"Distance {type} matrix created. Saving it . . .")
        if not os.path.exists('matrices'):
            os.makedirs('matrices')
        np.save(f"matrices/{matrix_name}.npy", distance_matrix)
        
        upper_triangle_array = distance_matrix[np.triu_indices(distance_matrix.shape[0], k=1)]
        plot_values(upper_triangle_array, f"allDistances_{matrix_name}", "Distances", "Number of cell pairs with specified distances")
        
        
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

        num_vertices = len(distance_matrix)
        reduced_graph.add_vertices(num_vertices)

        # Iterate through each node and identify num_of_closest_neighbors closest neighbors
        for i in range(num_vertices):
            if i % CONST ==0:
                print(f"Progress: {i}/{num_vertices}")
            # Sort neighbors by edge weight (excluding self)
            neighbors = [(j, weight) for j, weight in enumerate(distance_matrix[i]) if i != j]
            neighbors.sort(key=lambda x: x[1])

            # Add up to N closest neighbors to the reduced graph
            for j, weight in neighbors[:num_of_closest_neighbors]:
                reduced_graph.add_edge(i, j, weight=weight)
        
        # graph = Graph.Weighted_Adjacency(distance_matrix, mode='undirected', attr='weight', loops=False)
        
        print(f"Saving graph {graph_name} . . .")
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        reduced_graph.write_graphml(f"graphs/{graph_name}")
        
        print(f"###### job completed in: {datetime.now() - start_time}")
        return reduced_graph

def plot_cluster_stats(y_values, name, xlabel, ylabel):
    x_values = np.arange(len(y_values))

    plt.bar(x_values, y_values, width=0.8, align='center')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(name)
    
    plt.close()
    
def plot_values(data_array, name, xlabel, ylabel, bins = 100):
    
    plt.hist(data_array, bins)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(name)
    
    plt.close()
    
def plot_legend(node_colors, name):
    figure, ax = plt.subplots()
    
    m = len(node_colors)
    colors = set(node_colors)
    legend_elements = []
    
    for i, color in enumerate(colors):
        legend_elements.append(patches.Patch(color=color, label=f'{i}'))
        
    ax.legend(handles=legend_elements, loc='upper right')
    
    print(f"Saving legend for {name} . . .")
    figure.savefig(f"legend_for_{name}.png")
    
    plt.close()

def plot_clusters(cells, node_colors, name, diameter, text):
    start_time = datetime.now()
    print("====== Plotting clusters . . .")
    
    figure, ax = plt.subplots()
    ax.set_aspect('equal')
    
    n = len(cells)
    plot_legend(node_colors, name)
    
    for cell in cells:
        if cell.id_num == 0:
            circle = patches.Circle((cell.x, cell.y), radius=diameter, edgecolor='red', facecolor='none')
            ax.add_patch(circle)
        elif cell.id_num % CONST == 0:
            print(f"Progress for plotting clusters: {cell.id_num}/{n}")
        x = cell.x
        y = cell.y
        color = node_colors[cell.id_num]
        ax.scatter(x, y, color=color, s=2, alpha=1)

    ax.set_title(text)
    ax.set_xlabel("cell x coordinate")
    ax.set_ylabel("cell y coordinate")
        
    if "embryo" in name:
        ax.invert_yaxis()
        
    print(f"Saving plot for {name} . . .")
    figure.savefig(f"clusters_for_{name}.png")
    plt.close()
    print(f"###### job completed in: {datetime.now() - start_time}")

def cluster_leiden(graph, cells, name, diameter):
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
    plot_clusters(cells, node_colors, name, diameter, text)
    
    print(f"###### job completed in: {datetime.now() - start_time}")
    return partition.membership
    
def cluster_agglomerative(distance_matrix, cells, name, diameter, linkage_method, threshold=None):
    start_time = datetime.now()
    print("====== Started Agglomerative clustering . . .")
    
    condensed_distance_matrix = pdist(distance_matrix)
    linkage_matrix = linkage(condensed_distance_matrix, method=linkage_method)
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
            print(f"Number of clusters: {len(clusters)}")
            score = silhouette_score(distance_matrix, clusters, metric='precomputed')
            if score > max_score:
                max_threshold = threshold
                max_score = score
                optimal_clusters = clusters
    else:
        optimal_clusters = fcluster(linkage_matrix, t=threshold, criterion='distance')
        max_score = silhouette_score(distance_matrix, optimal_clusters, metric='precomputed')
        max_threshold = threshold
    
    
    num_clusters = len(set(optimal_clusters))
    optimal_clusters = np.array(optimal_clusters)
    optimal_clusters -= 1
    
    print(f"Number of clusters: {num_clusters}")

    color_map = cm.get_cmap('tab20c', num_clusters)
    colors = [color_map(i) for i in range(num_clusters)]
    
    node_colors = [colors[cluster] for cluster in optimal_clusters]
    text = f"silhouette_score: {max_score:.3f} number_of_clusters:{num_clusters}"
    plot_clusters(cells, node_colors, f"{name}_threshold_{max_threshold}", diameter, text)
    
    print(f"###### job completed in: {datetime.now() - start_time}")
    return optimal_clusters
    
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

def set_type_percentage_for_all_cells(cells, types, filename, neighborhood_diameter):
    start_time = datetime.now()
    print("====== Set type_percentage for all cells . . .")
    
    distance_matrix = get_distance_matrix(cells, filename)
    n = len(cells)
    for cell in cells:
        if cell.id_num % CONST == 0:
            print(f"Progress for calculating type percentage of cells: {cell.id_num}/{n}")
        cell.set_type_percentage(cells, types, distance_matrix, neighborhood_diameter)

    print(f"###### job completed in: {datetime.now() - start_time}")

def is_cluster_homogeneous(cluster, cell_ids, percentage_distance_matrix, name):
    start_time = datetime.now()
    print(f"====== Calculate if cluster {cluster} is homogeneous. . .")
    
    n = len(cell_ids)
    distances = []
    
    for i in range(n-1):
        for j in range(i + 1, n):
            distances.append(percentage_distance_matrix[cell_ids[i]][cell_ids[j]])
    
    plot_values(distances, f"{name}_isHomogeneous_cluster_{cluster}", "Distances", "Number of cell pairs with specified distance")
    print(f"###### job completed in: {datetime.now() - start_time}")
    
    return distances
    
def cluster_stat(cluster, cell_ids, num_of_types, cells, percentage_distance_matrix, name):
    start_time = datetime.now()
    print(f"====== Calculate cluster {cluster} stats . . .")
    
    type_count = np.zeros(num_of_types)
    cell_num = len(cell_ids)
    
    for cell_id in cell_ids:
        type_count[cells[cell_id].cell_type_num] += 1
    
    type_percentage = type_count / cell_num
    
    plot_cluster_stats(type_count, f"{name}_typeCount_cluster_{cluster}", "Type number", "Number of cells with specified type")
    plot_cluster_stats(type_percentage, f"{name}_typePercentage_cluster_{cluster}", "Type number", "Percentage of cells with specified type")
    is_cluster_homogeneous(cluster, cell_ids, percentage_distance_matrix, f"{name}_isHomogeneous_cluster_{cluster}")
        
    print(f"###### job completed in: {datetime.now() - start_time}")
    return type_count, type_percentage

def clusters_stat(clusters, num_of_types, cells, percentage_distance_matrix, name):
    start_time = datetime.now()
    print("====== Calculate clusters stats . . .")
    
    clusters_dict = {}
    
    for i, cluster in enumerate(clusters):
        if cluster not in clusters_dict:
            clusters_dict[cluster] = []
        clusters_dict[cluster].append(i)
        
    for cluster in clusters_dict:
        cell_ids = clusters_dict[cluster]
        cluster_stat(cluster, cell_ids, num_of_types, cells, percentage_distance_matrix, name)
    
    print(f"###### job completed in: {datetime.now() - start_time}")


def clustering(filename, neighborhood_diameter, cluster_alg = "leiden", cluster_param= None, linkage_method="single", num_of_closest_neighbors=None, dist="Manhattan", param=None):
    start_time = datetime.now()
    graph_name = f"{filename}_diameter_{neighborhood_diameter}_clusterAlg_{cluster_alg}_dist_{dist}"
    if param != None:
        paramStr = re.sub(r'\.', '', str(param))
        graph_name =f"{graph_name}_param_{paramStr}"
    if num_of_closest_neighbors != None:
        graph_name =f"{graph_name}_closestNeighbors_{num_of_closest_neighbors}"

    print(f"=== Clustering {graph_name}. . .")
    
    data = pd.read_csv(f"{filename}.csv")
    
    cells, types = get_cells_and_types(data)
    set_type_percentage_for_all_cells(cells, types, filename, neighborhood_diameter)

    percentage_distance_matrix = get_distance_matrix(cells, filename, "percentage", neighborhood_diameter, dist, param)
    
    if cluster_alg == "leiden":
        graph = create_reduced_graph(graph_name, percentage_distance_matrix, num_of_closest_neighbors)
        clusters = cluster_leiden(graph, cells, graph_name, neighborhood_diameter)
    else:
        clusters = cluster_agglomerative(percentage_distance_matrix, cells, graph_name, neighborhood_diameter, linkage_method, cluster_param)
        
    clusters_stat(clusters, len(types), cells, percentage_distance_matrix, graph_name)
    
    if not os.path.exists(f"clusters_folder"):
        os.makedirs(f"clusters_folder")
    np.save(f"clusters_folder/{graph_name}.npy", np.array(clusters))
    
    print(f"### job completed in: {datetime.now() - start_time}")
    
def cluster(filename):
    #clustering(filename=filename, neighborhood_diameter=200, cluster_alg="agglomerative")
    #clustering(filename=filename, neighborhood_diameter=350, cluster_alg="agglomerative")
    clustering(filename=filename, neighborhood_diameter=200, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    clustering(filename=filename, neighborhood_diameter=200, num_of_closest_neighbors=20)
    clustering(filename=filename, neighborhood_diameter=500, cluster_alg="agglomerative")
    clustering(filename=filename, neighborhood_diameter=200, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)

    #clustering(filename=filename, neighborhood_diameter=350, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_diameter=500, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    
    #clustering(filename=filename, neighborhood_diameter=200, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_diameter=350, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_diameter=500, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_diameter=200, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_diameter=350, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_diameter=500, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    
    #clustering(filename=filename, neighborhood_diameter=350, cluster_alg="agglomerative", dist="Jaccard", param=0.4)
    #clustering(filename=filename, neighborhood_diameter=350, num_of_closest_neighbors=20, dist="Jaccard", param=0.4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clustering')
    parser.add_argument('-fn', '--filename', type=str, required=True,
                        help='File name for cell data')
    parser.add_argument('-R', '--neighborhood_radius', type=int, required=True,
                        help='Neighborhood radius for cell neighborhood')
    parser.add_argument('-df', '--distance_function', type=str, required=False, default="Manhattan", 
                        help='Distance function used for calculating distance between cell types percentage of different cells')
    parser.add_argument('-alg', '--cluster_alg', type=str, required=False,
                        default="leiden", help='Algorithm used for clustering of cells')
    
    args = parser.parse_args()

    if args.distance_function == 'Jaccard':
        parser.add_argument('-param', '--jaccard_param', type=float, required=True,
                            help='Parameter for Jaccard distance')    
    
    if args.cluster_alg == 'leiden':
        parser.add_argument('-closest', '--num_of_closest_neighbors', type=int, required=True,
                            help='Number of closest neighbors fro graph reduction')
        
    if args.cluster_alg == 'agglomerative':
        parser.add_argument('-method', '--linkage_method', type=str, required=False,
                        default="single", help='Linkage method for agglomerative clustering algorithm')
        parser.add_argument('-t', '--threshold', type=int, required=False,
                        default=None, help='Threshold for agglomerative clustering algorithm')
    
    #cluster(args.filename)
    clustering(args.filename, args.neighborhood_diameter, args.distance_function, args.param_for_jaccard_dist, 
            args.cluster_alg, args.cluster_param, args.linkage_method, args.num_of_closest_neighbors)
