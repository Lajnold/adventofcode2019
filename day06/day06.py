#!/usr/bin/env python3

def load_orbits():
    with open('day06-input.txt') as f:
        # AAA)BBB
        lines = f.read().strip().splitlines()
        orbits = [line.split(')') for line in lines]
        orbits_dict = { b: a for a, b in orbits }
        return orbits_dict

def get_count(orbits, counts, obj):
    if obj == "COM":
        return 0

    cnt = counts.get(obj)
    if cnt is not None:
        return cnt
    else:
        next_obj = orbits.get(obj)
        next_cnt = get_count(orbits, counts, next_obj)
        counts[obj] = next_cnt + 1
        return next_cnt + 1

def part1():
    orbits = load_orbits()
    counts = {}
    total_orbits = sum(get_count(orbits, counts, obj) for obj in orbits.keys())
    print(f'Part 1: {total_orbits}')

def trace_path_to_com(orbits, obj):
    path_with_length = []
    next_obj = orbits.get(obj)
    length = 0
    while next_obj is not None:
        path_with_length.append((next_obj, length))
        length += 1
        next_obj = orbits.get(next_obj)

    return path_with_length

def part2():
    orbits = load_orbits()
    you_path = trace_path_to_com(orbits, 'YOU')
    san_path = trace_path_to_com(orbits, 'SAN')
    san_path_dict = { o: c for o, c in san_path }
    for obj_tup in you_path:
        if obj_tup[0] in san_path_dict:
            transfers_required = obj_tup[1] + san_path_dict[obj_tup[0]]
            break

    print(f'Part 2: {transfers_required}')

part1()
part2()
