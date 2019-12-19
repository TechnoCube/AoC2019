import textwrap

IMAGE_DIMENSIONS = [25, 6]


def read_encoded_image(filepath):
    file = open(filepath, "r")
    return file.read()


def count_0s(layer):
    return layer.count('0')


class ImageDecoder:

    def __init__(self, encoded_image):
        self.image = encoded_image
        self.layer_size = IMAGE_DIMENSIONS[0] * IMAGE_DIMENSIONS[1]
        self.layers = textwrap.wrap(self.image, self.layer_size)

    def part1(self):
        fewest_0_layer = min(self.layers, key=count_0s)
        return fewest_0_layer.count('1') * fewest_0_layer.count('2')

    def part2(self):
        final_image = []
        for pixel_index in range(self.layer_size):
            layer_index = 0
            while self.layers[layer_index][pixel_index] == '2':
                layer_index += 1
            final_image.append(self.layers[layer_index][pixel_index])

        final_image = "".join(final_image)
        return textwrap.wrap(final_image, IMAGE_DIMENSIONS[0])


if __name__ == "__main__":
    image = read_encoded_image(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\AoC2019\day08\encoded_image.txt")
    decoder = ImageDecoder(image)
    print("1s multiplied by 2s in layer with least 0s: {}\n".format(decoder.part1()))
    print('\n'.join(decoder.part2()))
