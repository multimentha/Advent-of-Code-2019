""""Find the best location for a monitoring station. The best location is on that asteroid from which the most other asteroids can be seen (are in direct line of sight)."""

# let's try the object oriented approach
class AsteroidField():
    """Represents an asteroid field.

    Offers methods for calculating optimal positions and the like."""

    def __init__(self, text_representation: str):
        self.text_representation = text_representation
        self.location_map = [[c for c in line] for line in text_representation.splitlines()]
        self.width = len(self.location_map[0])
        self.height = len(self.location_map)
        self.tile_count = self.width * self.height
    
    def visualize(self):
        return self.text_representation

    def illustrate_traversal(self, center_x: int, center_y: int, max_hops: int = None) -> str:
        """For an asteroid positioned at (center_x, center_y), illustrate the order in which other asteroids are checked to be in line of sight.

        If max_hops is not specified, the path will be as long as necessary to cover the  entire asteroid field.

        Returns a string with each line representing a row of the grid. The path starts at zero and grows from there."""
        # represent path in 2d grid
        spiral_path = self.spiral_path(center_x, center_y, max_hops)
        spiral_path.insert(0, (center_x, center_y))
        hop = 0
        digits = len(str(self.tile_count))
        grid = [["-".rjust(digits).center(digits+2) for tile in range(self.width)] for line in range(self.height)]
        for tile in spiral_path:
            x, y = tile[0], tile[1]
            try:
                grid[y][x] = str(hop).rjust(digits).center(digits+2)
            except IndexError as ie: # the spiral path has gone outside of the visual grid
                # just ignore it
                pass
            hop += 1
        # convert list grid to text lines
        lines = ["".join(str(num) for num in row) for row in grid]
        grid_representation = "\n".join(lines)
        return grid_representation

    def position_inside_grid(self, x: int, y: int):
            """Determine wether an x, y position is inside the asteroid field."""
            return 0 <= x < self.width and 0 <= y < self.height

    def spiral_path(self, center_x: int, center_y, max_hops:int = None) -> list:
        """Yield (x,y) coordinates of a spiraled path around the start position (0 based) for a given number of hops.

        If max_hops is not specified, the path will be as long as necessary to cover the  entire asteroid field.

        The path begins with the center (0) and and then spirals around it clockwise, starting from the tile top left of the center (1) as shown here:
         9   10   11   12   13
        24    1    2    3   14
        23    8    0    4   15
        22    7    6    5   16
        21   20   19   18   17
        """

        # check input to function
        if max_hops is not None:
            assert type(max_hops) is int
            assert max_hops >= 1

        # assemble path tile by tile
        grid_tiles_traversed = 0 # tiles specifically INSIDE of the asteroid field
        hops = 1 # start at 1 not 0 because the initial tile is already in the path
        path = [(center_x, center_y)]
        edge_length = 2; next_turn_in = edge_length
        directions = (
            (+1, 0), # right
            (0, +1), # down"
            (-1, 0), # left"
            (0, -1), # up"
        )
        rings = 0 # debug stat: how often the path has spiraled around the center
        direction = 0 # index for the above tuple
        tile = (center_x - 1, center_y - 1)
        finished = False
        while not finished:
            if self.position_inside_grid(*tile):
                grid_tiles_traversed += 1
                path.append(tile)
            # go to next tile
            tile = [sum(coords) for coords in zip(tile, directions[direction])] # element wise addtion of 2 tuples updates x, y position
            hops += 1
            next_turn_in -= 1
            if next_turn_in == 0:
                direction += 1
                if direction == len(directions):
                    rings += 1
                    edge_length += 2
                    direction = 0
                    # offset position by 1 tile diagonally towards top left
                    tile[0] -= 1; tile[1] -= 1
                next_turn_in = edge_length
            # is the path long enough yet?
            grid_searched = max_hops is None and grid_tiles_traversed == self.tile_count - 1
            enough_hops = hops == max_hops
            if grid_searched or enough_hops : finished = True
        return path
