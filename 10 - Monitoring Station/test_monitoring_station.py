import pprint as pp

from test_data import *
from monitoring_station import *

afs = [AsteroidField(t["text representation"]) for t in tests]

for af in afs:
    # log input data
    print("==== visualisation ====")
    print(af.visualize(), end="\n"*2)
    print("==== location map ====")
    for row in af.location_map:
        print(row)
    print()

    # visualization of spiral path
    print("==== path illustration ====")
    center = (3, 3)
    path_illustration = af.illustrate_traversal(*center, max_hops=20)
    print(path_illustration, end="\n"*2)
