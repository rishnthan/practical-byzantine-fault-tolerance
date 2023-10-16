import numpy as np
import random
import math

# Generate random data (100 coordinates within the range [0, 100])
random.seed(0)
data = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(100)]
data_list = list(data)
# Convert the data to a NumPy array for consistency with the code
data = np.array(data)   

# Randomly select 25 starting centroids from the data
num_clusters = 25
starting_centroids_indices = np.random.choice(len(data), num_clusters, replace=False)
starting_centroids = data[starting_centroids_indices]

# bounds for each centroid (within the range of data)
bounds = [(0, 100)] * (num_clusters * 2)

# objective function (inertia) to be minimized
def objective_function(centroids):
    centroids = centroids.reshape(num_clusters, 2)
    # Calculate the inertia (sum of squared distances to the nearest centroid)
    distances = np.min(np.linalg.norm(data[:, np.newaxis] - centroids, axis=2), axis=1)
    inertia = np.sum(distances ** 2)
    return inertia

def differential_search_algorithm(objective_function, bounds, max_iter, npop, F, CR):
    pop = np.random.randint([b[0] for b in bounds], [b[1] for b in bounds], size=(npop, len(bounds)))
    fitness = np.array([objective_function(ind) for ind in pop])

    for _ in range(max_iter):
        new_pop = np.copy(pop)

        for i in range(npop):
            idxs = np.arange(npop)
            np.random.shuffle(idxs)
            a, b, c = pop[idxs[:3]]
            jrand = np.random.randint(len(bounds))

            for j in range(len(bounds)):
                if np.random.rand() < CR or j == jrand:
                    new_pop[i][j] = a[j] + F * (b[j] - c[j])

            new_pop[i] = np.clip(new_pop[i], [b[0] for b in bounds], [b[1] for b in bounds])
            new_fitness = objective_function(new_pop[i])

            if new_fitness < fitness[i]:
                pop[i] = new_pop[i]
                fitness[i] = new_fitness

    best_solution = pop[np.argmin(fitness)]
    return best_solution

# Perform Differential Search Algorithm to optimize the centroids
best_centroids = differential_search_algorithm(objective_function, bounds, max_iter=100, npop=50, F=0.5, CR=0.7)


best_centroids_list = [tuple(best_centroids[i:i+2]) for i in range(0, len(best_centroids), 2)]
#print(best_centroids_list)

def get_new_centroid(centroid_list, coordinate_list):
    nearest_coordinates = []
    
    for centroid in centroid_list:
        nearest_coordinate = min(coordinate_list, key=lambda coord: math.dist(centroid, coord))
        nearest_coordinates.append(nearest_coordinate)
    
    return nearest_coordinates

new_centroids = get_new_centroid(best_centroids_list, data_list)
#print("CENTROIDS")
#print(new_centroids)
def find_nearest_coordinates(centroids, coordinates, k=3):
    nearest_coordinates = []
    available_coordinates = coordinates.copy()  # Create a copy to avoid modifying the original list
    
    for centroid in centroids:
        if centroid in available_coordinates:
            available_coordinates.remove(centroid)

    for centroid in centroids:
        nearest_coords = []
        
        for _ in range(k):
            distances = [np.linalg.norm(np.array(centroid) - np.array(coord)) for coord in available_coordinates]
            if not distances:  # If there are no more available coordinates, break the loop
                break
            nearest_index = np.argmin(distances)
            nearest_coord = available_coordinates.pop(nearest_index)
            nearest_coords.append(nearest_coord)
        
        nearest_coords.insert(0, centroid)
        nearest_coordinates.append(nearest_coords)
    
    return nearest_coordinates

nearest_coordinates = find_nearest_coordinates(new_centroids, data_list)
print("CLUSTERS")
print(nearest_coordinates)
