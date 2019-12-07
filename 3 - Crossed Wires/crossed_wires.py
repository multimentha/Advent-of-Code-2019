import collections
import itertools
import operator
import os
import pprint as pp

class PatchField():
    """Load, visualize and analyze wire patch fields."""
    symbols = {
        "bend": "+",
        "central port": "O",
        "crossing": "X",
        "empty": ".",
        "horizontal": "-",
        "vertical": "|",
    }
    directions = {
        "D": (0, +1),
        "L": (-1, 0),
        "R": (+1, 0),
        "U": (0, -1),
    }

    def __init__(self, filepath: str):
        # read in data from text file
        self.source_file = filepath
        with open(filepath) as fh:
            lines = [line.strip() for line in fh.readlines()]
        self.wires = [line.split(",") for line in lines[0:2]]
        # check if there are entries for expected closest distances (only the case for test data)
        try:
            int(lines[2])
        except (IndexError, ValueError):
            self.expected_closest_manhattan = None
        else:
            self.expected_closest_manhattan = int(lines[2])
        try:
            int(lines[3])
        except (IndexError, ValueError):
            self.expected_closest_manhattan = None
        else:
            self.expected_fewest_combined_steps = int(lines[3])

        # compute statistics
        self.coordinate_chains = [self.xy_coordinate_chain(wire) for wire in self.wires]
        self.common_bends = self.find_common_bends(self.coordinate_chains[0], self.coordinate_chains[1])  # hard coded for the 1st 2 chains at the moment
        self.lookup_map = self.create_lookup_map(self.wires)
        self.crossovers = self.find_crossovers(self.lookup_map)
        self.closest_crossovers = self.find_closest_crossover(self.crossovers)
        self.closest_manhattan = self.closest_crossovers[0][1] if self.closest_crossovers else None
        self.lowest_signal_delay_crossovers = self.find_lowest_signal_delay_crossovers(self.crossovers)

    def xy_coordinate_chain(self, wire: list) -> list:
        """Visualize a single wire strand in ASCII art."""
        # keep track of coordinates
        # the central port is where the wires emerge from the wall and always 0, 0
        start_x = 0; start_y = 0
        chain = [(start_x, start_y)]
        x, y = start_x, start_y
        for instr in wire:
            direction, amount = instr[0], int(instr[1:])
            x += PatchField.directions[direction][0] * amount
            y += PatchField.directions[direction][1] * amount
            chain.append((x, y, ))
        return chain

    def create_lookup_map(self, wires: list) -> dict:
        """Return a dictionary which can be used to look up which wires around found on a specific position of the patch field and how long it took each to get there.
        
        Use (x, y) tuples as the keys to search the dictionary.
        Values are (w-1, w-2, ...) tuples where w-N holds the possible signal distances of a wire to that position. E. g. a tuple w-1 = (20, 310) represents that this wire reaches this position after 20 and 310 steps. An empty tuple means that the wire never runs through this spot.
        """

        def default_returner():
            return [[] for w in wires] # e.g. [[], [], []] for 3 wires
        lmap = collections.defaultdict(default_returner)
        # fill the dictionary with locations from each wire

        def move_towards(x: int, y: int, direction: str) -> tuple:
            """"Given a (<x>, <y>) position looks up the coordinate change defined by <direction> and returns a tuple with an updated position."""
            return tuple(sum(elem) for elem in zip((x,y), self.__class__.directions[direction]))

        for i, w in enumerate(wires):
            # walk over every single tile that the wire passes through in sequence and add its absolute position to the dictionary
            x = 0; y = 0; steps = 1
            for instr in w:
                direction, amount = instr[0], int(instr[1:])
                while amount:
                    x, y = move_towards(x, y, direction)
                    lmap[(x, y)][i].append(steps)
                    amount -= 1
                    steps += 1
        return lmap

    def find_common_bends(self, chain1: list, chain2: list) -> list:
        """Find locations in which both wires take a turn (are bent)."""
        chain1 = set(chain1); chain2 = set(chain2)
        common_bends = chain1.intersection(chain2)
        common_bends.remove((0,0))
        return list(common_bends)

    def find_crossovers(self, lookupmap: dict, threshold: int = 2) -> list:
        """Find all the coordinates at which a minimum number of wires (default = 2) are present.
        
        Returns a list of all coordinate pairs where this is the case."""
        crossovers = []
        for k, v in lookupmap.items():
            unique_presences = 0
            wire = 0
            while unique_presences < threshold and wire < len(v) :
                if len(v[wire]) > 0: unique_presences += 1
                wire += 1
            if unique_presences >= threshold:
                crossovers.append(k)
        return crossovers

    def find_enclosure(self, coordinate_chains: list) -> tuple:
        """Return a tuple that describes how far to the left, right, top, bottom a field needs to extend to hold all wires in the coordinate_chains list.

        Assumes the center port as the origin (0, 0) of a cartesian coordinate system."""
        x_min = min(c_pair[0] for chain in coordinate_chains for c_pair in chain)
        x_max = max(c_pair[0] for chain in coordinate_chains for c_pair in chain)
        y_min = min(c_pair[1] for chain in coordinate_chains for c_pair in chain)
        y_max = max(c_pair[1] for chain in coordinate_chains for c_pair in chain)
        return x_min, x_max, y_min, y_max

    def find_closest_crossover(self, crossovers: list, x: int = 0, y: int =0) -> list or None:
        """Filters a list of coordinates down to those with the closest Manhattan (rectilinear) distance to x and y.

        Returns a list with tuples of format (x, y, rectilinear distance)

        (x, y) defaults to (0, 0) which is typically location of the central port.
        
        If there are no crossovers, None object is returned instead."""

        def manhattan_dist(x1, y1, x2, y2):
            return abs(x2 - x1) + abs(y2 - y1)

        if not crossovers:
            winners = None
        else:
            mh_dists = list()
            # compute rectilinear distance for each pair
            for c in crossovers:
                mh_dists.append((c, manhattan_dist(c[0], c[1], x, y)))
            lowest = min(mh_d[1] for mh_d in mh_dists)
            winners = [entry for entry in mh_dists if entry[1] == lowest]
        return winners

    def find_lowest_signal_delay_crossovers(self, crossovers: list, x=0, y=0) -> list:
        """Filters a list of crossover coordinates down to the one with the lowest sginal delay. If multiple spots are tied for lowest, all of them are included in the result.
        
        Returns a list with tuples of format (x, y, signal delay). The list is empty if there are no crossovers.
        
        (x, y) defaults to (0, 0) which is typically the location of the central port."""
        lowest = []
        if crossovers:
            # build a list that can easily be compared and filtered
            comparison = []
            # append signal delay to each (x, y) pair
            for crossover in crossovers:
                a, b = crossover[0], crossover[1]
                signal_delays = self.lookup_map[a, b]
                min_signal_delays = [min(wire) for wire in signal_delays]
                combined_lowest_signal_delay = sum(min_signal_delays)
                comparison.append((crossover, combined_lowest_signal_delay), )
            global_minimal_signal_delay = min(c[1] for c in comparison)
            lowest = [l for l in comparison if l[1] == global_minimal_signal_delay]
        return lowest

    def prepare_field(self, x_min: int, x_max: int, y_min: int, y_max: int, padding: int = 1) -> list:
        """Prepare 2-dimensional list that will be used to represent a patch field with wires in it. All positions in the field are initialized as having the symbol that reprsents an empty spot (usually a dot).

        Padding specifices the amount of extra columns or lines added to each side so that it's easier to visually distinguish the end of a wire.
        
        Returns a list of strings."""
        width = x_max - x_min + 1 + padding
        height = y_max- y_min + 1 + padding
        line = [PatchField.symbols["empty"]] * width
        field = [line for column in range(height)]
        return field

# run program on field data
if __name__ == "__main__":
    patch_field = PatchField("input/input.txt")
    print("Wire crossings closest to the central port, as measured by Manhattan (rectilinear) distance:")
    for crossover in patch_field.closest_crossovers:
        (x, y), d = crossover
        print(f"{x = }, {y = }, Manhattan distance = {d}")

    print("\nWire crossings closest to the central port, as measured by combined signal delay distance:")
    for sd_crossover in patch_field.lowest_signal_delay_crossovers:
        (x, y), delay = sd_crossover
        print(f"{x = }, {y = }, combined signal delay = {delay}")
