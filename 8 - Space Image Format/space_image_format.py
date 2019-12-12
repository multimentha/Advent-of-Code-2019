""" Advent of Code - day 8 (part 1): Space Image Format
Extract a metric from an image format used by space elves.

https://adventofcode.com/2019/day/8
"""

# set which images to analyze
TEST = False
PART1 = True
PART2 = True

class SpaceImage():
    """Reprents an image in the format used by the space elves."""

    color_encoding = {
        '0': '⬛', # black; represented by U+2B1B (black large square)
        '1': '⬜', # white; represented by U+2B1C (white large square)
        '2': ' ', # transparent; represented by (a space)
    }

    def __init__(self, pixels: list or tuple, width: int, height: int):
        pixels_per_layer = width * height
        layer_count = len(pixels) // pixels_per_layer
        self.layers = list()
        assert layer_count * pixels_per_layer == len(pixels), "This image's pixel count does not match the specified width or height."
        # parse pixels into a 3-D array like this:
        # layers = [layer1, layer2, ...]
        # layer = [row1, row2, ...]
        # row = [pixel1, pixel2, ...]
        pixel = 0; row = 0
        layer = []
        while pixel < len(pixels):
            scanline = pixels[pixel:pixel+width]
            pixel += width
            layer.append(scanline)
            row += 1
            if row == height:
                row = 0
                self.layers.append(layer)
                layer = []

    def find_layers_with_fewest_occurences(self, character) -> list:
        """Find the layers with the least occurences of a given character (pixel value).

        Returns a list with the indices of the layers."""
        # use first layer as initial comparison
        least = None; results = []
        for index, layer in enumerate(self.layers):
            count = sum(row.count(character) for row in layer)
            if least is None or count < least:
                least = count
                results = [index]
            elif count == least:
                results.append(index)
        return results

    def print_image(self) -> None:
        """Prints out a pixel row by pixel row string representation of the image data."""
        for index, layer in enumerate(self.layers):
            print(f"== layer {index} ==")
            for row in layer:
                print(row)

    def sum_product(self, layer_index: int, a: str, b: str) -> int:
        """Find and count all instances of a and b in the layer, then form their product.
        
        Returns sum(instances(a)) * sum(instances(b))."""
        sum_of_a = sum(row.count(a) for row in self.layers[layer_index])
        sum_of_b = sum(row.count(b) for row in self.layers[layer_index])
        return sum_of_a * sum_of_b

if __name__ == "__main__":   
    # a simple example to practice on
    if TEST:
        test_data = [p for p in "123456789012"]
        test_data_width = 3
        test_data_height = 2
        test_image = SpaceImage(test_data, test_data_width, test_data_height)
        test_image.print_image()
    
    # process part 1
    if PART1 or PART2:        
        with open("input.txt", "r") as f:
            data = [p for p in f.read().strip()]
        space_image = SpaceImage(data, 25, 6)
        # space_image.print_image()
        to_search_for = '0'
        l_indices_w_least = space_image.find_layers_with_fewest_occurences(to_search_for)
        l_index_least = l_indices_w_least[0]
        assert len(l_indices_w_least) == 1, f"multiple layers are tied for least occurences of {to_search_for}, handle this case manually!"
        # print(f"{l_index_least = }")
        sum_product = space_image.sum_product(l_index_least, "1", "2")
        print(f"{sum_product = }")

    # process part 2
