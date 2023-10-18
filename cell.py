import numpy as np
from scipy.spatial.distance import euclidean, cityblock, jaccard, hamming

class Cell:
    
    def __init__(self, cell_id, cell_num, cell_type, cell_type_num, x, y):
        self.id = cell_id
        self.id_num = cell_num
        self.type = cell_type
        self.type_num = cell_type_num
        self.types_percentage = None
        self.x = x
        self.y = y
    
    def set_types_percentage(self, cells, num_of_types, distance_matrix, neighborhood_radius):
        """
        Calculate the percentage of cell types in neighborhood of 
        this cell and set it as a types_percentage parameter.
        """
        self.types_percentage = np.zeros(num_of_types)
        self.types_percentage[self.type_num] += 1
        
        num_of_cells_in_neighborhood = 1
        for cell in cells:
            if distance_matrix[self.id_num][cell.id_num] < neighborhood_radius:
                self.types_percentage[cell.type_num] += 1
                num_of_cells_in_neighborhood += 1
                
        self.types_percentage /= num_of_cells_in_neighborhood

    def coordinate_distance_to(self, other_cell):
        """
        Calculate the Euclidean distance between this cell and cell other_cell.
        """
        return euclidean([self.x, self.y], [other_cell.x, other_cell.y])
    
    def percentage_distance_to(self, other_cell, dist="Manhattan", hamming_param=None):
        """
        Calculate the similarity (distance) between percentage 
        of types of this cell and cell other_cell.
        """
        if dist == "Manhattan":
            return cityblock(self.types_percentage, other_cell.types_percentage)
        elif dist == "Hamming":
            p_this_cell = [1 if p > hamming_param else 0 for p in self.types_percentage]
            p_other_cell = [1 if p > hamming_param else 0 for p in other_cell.types_percentage]
            return hamming(p_this_cell, p_other_cell)
        else: # Euclidean
            return euclidean(self.types_percentage, other_cell.types_percentage)

