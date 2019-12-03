#!/usr/bin/env python3

def parse_move(move_str):
    # Input: 'R123'
    # Output: ('R', 123)
    d = move_str[0]
    n = int(move_str[1:])
    return d, n

def load_paths():
    with open('day03-input.txt') as f:
        lines = f.readlines()
        paths = []
        for line in lines:
            paths.append([parse_move(x) for x in line.split(',')])
    
    return paths

def move_pos(pos, d, n):
    if d == 'U':
        return (pos[0] + n, pos[1])
    if d == 'D':
        return (pos[0] - n, pos[1])
    if d == 'R':
        return (pos[0], pos[1] + n)
    if d == 'L':
        return (pos[0], pos[1] - n)

def apply_move(pos, move, steps_so_far, first_wire_locations, intersections, is_first_wire):
    for i in range(move[1]):
        pos = move_pos(pos, move[0], 1)
        if is_first_wire:
            if pos not in first_wire_locations.keys():
                first_wire_locations[pos] = steps_so_far + i + 1
        else:
            if pos in first_wire_locations.keys():
                intersections.add((pos, steps_so_far + i + 1))

    return pos

def part1():
    paths = load_paths()

    first_wire_locations = dict()
    intersections = set()

    pos = (0, 0)
    steps_so_far = 0
    for move in paths[0]:
        pos = apply_move(pos, move, steps_so_far, first_wire_locations, intersections, True)
        steps_so_far += move[1]

    pos = (0, 0)
    steps_so_far = 0
    for move in paths[1]:
        pos = apply_move(pos, move, steps_so_far, first_wire_locations, intersections, False)
        steps_so_far += move[1]

    closest_intersection = None
    for inter in intersections:
        inter_pos = inter[0]
        dist = abs(inter_pos[0]) + abs(inter_pos[1])
        if closest_intersection is None or dist < closest_intersection:
            closest_intersection = dist

    print(f'Part 1: {closest_intersection}')

def part2():
    paths = load_paths()

    first_wire_locations = dict()
    intersections = set()

    pos = (0, 0)
    steps_so_far = 0
    for move in paths[0]:
        pos = apply_move(pos, move, steps_so_far, first_wire_locations, intersections, True)
        steps_so_far += move[1]

    pos = (0, 0)
    steps_so_far = 0
    for move in paths[1]:
        pos = apply_move(pos, move, steps_so_far, first_wire_locations, intersections, False)
        steps_so_far += move[1]

    shortest_intersection = None
    for inter in intersections:
        inter_pos = inter[0]
        inter_steps = inter[1]
        passed_steps = first_wire_locations[inter_pos]
        tot_steps = inter_steps + passed_steps
        if shortest_intersection is None or tot_steps < shortest_intersection:
            shortest_intersection = tot_steps

    print(f'Part 2: {shortest_intersection}')


part1()
part2()
