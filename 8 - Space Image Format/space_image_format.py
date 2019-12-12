""" Advent of Code - day 8 (part 1): Space Image Format
Extract a hidden message from an image format used by space elves.

https://adventofcode.com/2019/day/8
"""

# Run tests in addition to main tasks?
TEST = False

class SpaceImage():
    """Reprents an image in the format used by the space elves.
    
    Gives easy access to flattened and tile representation of the image."""

    color_encoding = {
        '0': '⬛', # black; represented by U+2B1B (black large square)
        '1': '⬜', # white; represented by U+2B1C (white large square)
        '2': ' ', # transparent; represented by (a space)
    }

    def __init__(self, pixels: list or tuple, width: int, height: int):
        self.width = width
        self.height = height
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
        self.flattened = self._flatten()
        self.visualization = self._visualize()

    def _flatten(self) -> list:
        """Flatten the image into a single layer by ignoring transparent pixels.

        Returns a 2-dimensional list: a list of pixel rows with each row containing the pixel values."""
        flattened = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # compare layers front to back and grab first non transparent pixel
                for l in range(len(self.layers)):
                    if (value := self.layers[l][y][x]) != '2':
                        break
                row.append(value)
            flattened.append(row)
        return flattened

    def find_layers_with_fewest_occurences(self, character) -> list:
        """Find the layers with the least occurences of a given character (pixel value).

        Returns a list with the indices of the layers."""
        least = None; results = []
        for index, layer in enumerate(self.layers):
            count = sum(row.count(character) for row in layer)
            if least is None or count < least:
                least = count
                results = [index]
            elif count == least:
                results.append(index)
        return results

    def print_flattened(self) -> None:
        """Prints out a row by row representation of the flattened image."""
        for row in self.flattened:
            print(row)        

    def print_layers(self) -> None:
        """Prints out a row by row representation of the image's layers."""
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
    
    def _visualize(self):
        """Visualize the flattened image using Unicode characters.

        Returns a list of strings with each string representing a pixel row."""
        rows_as_strings = ["".join(row) for row in self.flattened]
        visualization = "\n".join(rows_as_strings)
        for code, glyph in self.__class__.color_encoding.items():
            visualization = visualization.replace(code, glyph)
        return visualization

if __name__ == "__main__":   
    # a simple example provided by the web page
    if TEST:
        test_data = [p for p in "123456789012"]
        test_data_width = 3
        test_data_height = 2
        test_image = SpaceImage(test_data, test_data_width, test_data_height)
        test_image.print_layers()
    
    with open("input.txt", "r") as f:
        data = [p for p in f.read().strip()]
    space_image = SpaceImage(data, 25, 6)
    to_search_for = '0'
    l_indices_w_least = space_image.find_layers_with_fewest_occurences(to_search_for)
    l_index_least = l_indices_w_least[0]
    assert len(l_indices_w_least) == 1, f"multiple layers are tied for least occurences of {to_search_for}, handle this case manually!"
    sum_product = space_image.sum_product(l_index_least, "1", "2")
    print("==== part 1 ====")
    print(f"{sum_product = }")
    print("\n==== part 2 ====")
    print("Try to visually discern a message (multiple letters) from this crude drawing:\n - letters are in white tiles\n - the background is black")
    print(space_image.visualization)
