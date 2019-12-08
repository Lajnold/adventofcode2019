#!/usr/bin/env python3

def load_pixel_data():
    with open('day08-input.txt') as f:
        return list(map(int, f.read().strip()))


def part1():
    pixels = load_pixel_data()
    pixels_per_layer = 25 * 6

    zeros_per_layer = []
    ones_per_layer = []
    twos_per_layer = []
    for layer_start in range(0, len(pixels), pixels_per_layer):
        num_zeros = 0
        num_ones = 0
        num_twos = 0
        for pn in range(layer_start, layer_start + pixels_per_layer):
            if pixels[pn] == 0:
                num_zeros += 1
            elif pixels[pn] == 1:
                num_ones += 1
            elif pixels[pn] == 2:
                num_twos += 1

        zeros_per_layer.append(num_zeros)
        ones_per_layer.append(num_ones)
        twos_per_layer.append(num_twos)

    fewest_zeros = min(zeros_per_layer)
    fewest_zeros_layer = zeros_per_layer.index(fewest_zeros)
    ones_times_twos = ones_per_layer[fewest_zeros_layer] * twos_per_layer[fewest_zeros_layer]
    print(f'Part 1: {ones_times_twos}')


def get_rendered_pixel(pixels, y, x):
    pixels_per_layer = 25 * 6
    num_layers = len(pixels) // pixels_per_layer

    for layer in range(num_layers):
        pix = pixels[(layer * pixels_per_layer) + (y * 25) + x]
        if pix != 2:
            return str(pix)

    return ' '

def part2():
    pixels = load_pixel_data()

    output = []
    for y in range(6):
        for x in range(25):
            rendered_pix = get_rendered_pixel(pixels, y, x)
            output.append(rendered_pix if rendered_pix == '1' else ' ')
        output.append('\n')

    print(f'Part 2:\n{"".join(output)}')


part1()
part2()
