import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

def k_medoid(data, distance_matrix, seeds):
    distance_matrix_to_seeds = np.array(distance_matrix[seeds])
    
    max_difference_allowed = 30
    current_cluster_sizes = np.asarray([0,0,0,0])

    choosen_seeds = [None] * distance_matrix.shape[0]

    while(True):
        best_match = (None, None, None)

        mask = np.argwhere(current_cluster_sizes < np.min(current_cluster_sizes) + max_difference_allowed).flatten()
        for index, distances_in_point in enumerate(distance_matrix_to_seeds):
            if (choosen_seeds[index] is None):
                min_dist = np.min(distances_in_point[mask])
                suggested_match = (index, np.argwhere(distances_in_point == min_dist)[0][0], min_dist)
                if (best_match[2] is None or suggested_match[2] < best_match[2]):
                    best_match = suggested_match
        if (best_match[0] is None):
            break


        choosen_seeds[best_match[0]] = best_match[1]    
        current_cluster_sizes[best_match[1]] += 1    


    data["cluster"] = [seeds[i] for i in choosen_seeds]

    cluster_map = data.plot(column="cluster", markersize=10, cmap='Set1')
    data.loc[seeds].plot(ax=cluster_map, color="black", markersize=20)

    return data


data = gpd.read_file("example-data\\unesco_asia.gpkg", driver="GPKG")
#data = gpd.read_file("example-data\\capitals.gpkg", driver="GPKG")

distance_matrix = data.geometry.apply(lambda x: data.distance(x).astype(np.int64))

#seeds = [0,1,2,3]
#seeds = np.argsort(distance_matrix.sum())[0:4]
seeds = np.argsort(distance_matrix.loc[:,0:9].sum())[0:4]

i = 0
data = k_medoid(data, distance_matrix, seeds)
print(i, seeds)

seed_combinations_so_far = []
while(True):
    new_seeds = []
    for seed in seeds:
        points_in_seed = data[data["cluster"] == seed].index

        small_matrix = distance_matrix.loc[points_in_seed,points_in_seed]
        sumdists = small_matrix.sum(axis=1)
        new_seeds.append(sumdists.index[np.argmin(sumdists)])


    if (set(new_seeds) in seed_combinations_so_far):
        break
    else:
        seed_combinations_so_far.append(set(new_seeds))
        seeds = new_seeds
        data = k_medoid(data, distance_matrix, seeds)

        i+=1
        print(i, seeds)

plt.show()
