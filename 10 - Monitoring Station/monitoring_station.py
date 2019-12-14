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
    
    def visualize(self):
        return self.text_representation

    def spiral_path(self, start_x: int, start_y) -> list:
        """Yield (x,y) coordinates of a spiraled path around the start position (0 based).

        The path begins to the upper left of the start position and spirals around it clockwise, covering every tile in the grid in this fashion."""

        def tile_inside_grid(x: int, y: int):
            """Determine wether an x, y position is inside the asteroid field."""
            return 0 <= x < self.width and 0 <= start_y < self.height

        # ensure start position is inside the grid
        assert 0 <= start_x < self.width, "The given start_x is outside of the grid!"
        assert 0 <= start_y < self.height, "The given start_y is outside of the grid!"

        # assemble path tile by tile
        path = []
        tiles_to_go = self.width * self.height
        edge_length = 3; next_turn_in = edge_length
        directions = (
            (+1, 0), # right
            (0, +1), # down"
            (-1, 0), # left"
            (0, -1), # up"
        )
        rounds = 0 # debug stat: how often the path has spiraled around the center
        direction = 0 # index for the above tuple
        tile = (start_x - 1, start_y -1)
        while tiles_to_go:
            if tile_inside_grid(*tile):
                path.append(tile)
                tiles_to_go -= 1
            # go to next tile
            tile = [sum(coords) for coords in zip(tile, directions[direction])] # element wise addtion of 2 tuples updates x, y position
            next_turn_in -= 1
            if next_turn_in == 0:
                direction += 1
                if direction == len(directions):
                    rounds += 1
                    edge_length += 2
                    direction = 0
                next_turn_in = edge_length
        return path
