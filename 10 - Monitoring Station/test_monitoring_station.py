import pprint as pp

from test_data import *
from monitoring_station import *

afs = [AsteroidField(t["text representation"]) for t in tests]

for af in afs:
    print("==== visualisation ====")
    print(af.visualize(), "\n")
    print("==== location map ====")
    pp.pprint(af.location_map)
    print()

    # visualization of spiral path
    print("==== spiral path ====")
    grid = [[None for tile in range(af.width)] for line in range(af.height)]
    center = (2, 2)
    spiral_path = af.spiral_path(*center)
    spiral_path.insert(0, center)
    hop = 0
    for tile in spiral_path:
        x, y = tile[0], tile[1]
        grid[y][x] = str(hop)
        hop += 1
    pp.pprint(grid)
    print()

    print("==== path illustration ====")
    path_illustration = af.illustrate_spiral_path(2, 2)
    print(path_illustration)

