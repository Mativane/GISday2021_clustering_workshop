import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

def k_medoid(data, distance_matrix, seeds):
    distance_matrix_to_seeds = np.array(distance_matrix[seeds])
    closest_seeds = np.argmin(distance_matrix_to_seeds, axis=1)
    data["cluster"] = [seeds[i] for i in closest_seeds]

    cluster_map = data.plot(column="cluster", markersize=10)
    data.loc[seeds].plot(ax=cluster_map, color="red", markersize=20)

    return data


#data = gpd.read_file("example-data\\capitals.gpkg", driver="GPKG")
data = gpd.read_file("example-data\\unesco_asia.gpkg", driver="GPKG")

#seeds = [0,1,2,3]
seeds = [0,1,2,3,4,5]

distance_matrix = data.geometry.apply(lambda x: data.distance(x).astype(np.int64))

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
