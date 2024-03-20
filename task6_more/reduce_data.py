import argparse
from clustering import clustering

def cluster(filename):
    #clustering(filename=filename, neighborhood_radius=200, cluster_alg="agglomerative")
    #clustering(filename=filename, neighborhood_radius=350, cluster_alg="agglomerative")
    clustering(filename=filename, neighborhood_radius=200, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    clustering(filename=filename, neighborhood_radius=200, num_of_closest_neighbors=20)
    clustering(filename=filename, neighborhood_radius=500, cluster_alg="agglomerative")
    clustering(filename=filename, neighborhood_radius=200, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)

    #clustering(filename=filename, neighborhood_radius=350, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_radius=500, cluster_alg="agglomerative", dist="Jaccard", param=0.3)
    
    #clustering(filename=filename, neighborhood_radius=200, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_radius=350, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_radius=500, num_of_closest_neighbors=20)
    #clustering(filename=filename, neighborhood_radius=200, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_radius=350, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    #clustering(filename=filename, neighborhood_radius=500, num_of_closest_neighbors=20, dist="Jaccard", param=0.3)
    
    #clustering(filename=filename, neighborhood_radius=350, cluster_alg="agglomerative", dist="Jaccard", param=0.4)
    #clustering(filename=filename, neighborhood_radius=350, num_of_closest_neighbors=20, dist="Jaccard", param=0.4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clustering')
    parser.add_argument('-fn', '--filename', type=str, required=True,
                        help='File name for cell data')
    parser.add_argument('-R', '--neighborhood_radius', type=int, required=True,
                        help='Neighborhood radius for cell neighborhood')
    parser.add_argument('-df', '--distance_function', type=str, required=False, default="Manhattan", 
                        help='Distance function used for calculating distance between cell types percentage of different cells')
    parser.add_argument('-param', '--hamming_param', type=float, required=False,
                        default=0.3, help='Parameter for Jaccard distance') 
    parser.add_argument('-alg', '--cluster_alg', type=str, required=False,
                        default="leiden", help='Algorithm used for clustering of cells')
    parser.add_argument('-closest', '--num_of_closest_neighbors', type=int, required=False,
                        default=20, help='Number of closest neighbors fro graph reduction')
    parser.add_argument('-method', '--linkage_method', type=str, required=False,
                        default="single", help='Linkage method for agglomerative clustering algorithm')
    parser.add_argument('-t', '--threshold', type=int, required=False,
                        default=None, help='Threshold for agglomerative clustering algorithm')

    args = parser.parse_args()

    #cluster(args.filename)
    clustering(args.filename, args.neighborhood_radius, args.distance_function, args.hamming_param, 
            args.cluster_alg, args.linkage_method, args.threshold, args.num_of_closest_neighbors)