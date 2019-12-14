import pprint as pp

from test_data import *
from monitoring_station import *

afs = [AsteroidField(t["text representation"]) for t in tests]

for af in afs:
    print("==== visualisation ====")
    print(af.visualize(), "\n")
    print("==== location map ====")
    pp.pprint(af.location_map, "\n")

    # visualization of spiral path
    print("==== spiral path ====")
    grid = [[None for tile in range(af.width)] for line in range(af.height)]
    print(grid, "\n")
