import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

def k_means(data, seeds):
    data["cluster"] = data.geometry.apply(lambda x: np.argmin([x.distance(s) for s in seeds]))

    cluster_map = data.plot(column="cluster", markersize=10, cmap='Set1')
    seeds.plot(ax=cluster_map, color="black", markersize=20)

    return data


data = gpd.read_file("example-data\\unesco_asia.gpkg", driver="GPKG")
#data = gpd.read_file("example-data\\capitals.gpkg", driver="GPKG")

distance_matrix = data.geometry.apply(lambda x: data.distance(x).astype(np.int64))
seeds = data.loc[np.argsort(distance_matrix.loc[:,0:9].sum())[0:4], 'geometry']

i = 0
data = k_means(data, seeds)
print(i, seeds)

seed_combinations_so_far = []
while(True):
    new_seeds = []
    for i, seed in enumerate(seeds):
        points_in_seed = data[data["cluster"] == i].loc[:,'geometry']
        new_seed = Point(np.mean(points_in_seed.x), np.mean(points_in_seed.y))
        new_seeds.append(new_seed)



    sets_to_compare = [(s.x,s.y) for s in new_seeds]
    if (set(sets_to_compare) in seed_combinations_so_far):
        break
    else:
        seed_combinations_so_far.append(set(sets_to_compare))
        seeds = gpd.GeoDataFrame(geometry = new_seeds).geometry
        data = k_means(data, seeds)

        i+=1
        print(i, seeds)

plt.show()
