#!/usr/bin/env python3

from math import gcd, atan2, pi

class Map:
    def __init__(self, the_map):
        self.map = the_map
        self.height = len(the_map)
        self.width = len(the_map[0])

    def __getitem__(self, coords):
        y, x = coords
        return self.map[y][x]


def load_map():
    fn = 'day10-input.txt'
    # fn = 'day10-input-test1.txt'
    with open(fn) as f:
        return Map(f.read().splitlines())


def signed_one(val):
    return -1 if val < 0 else 1

def get_blocked_asteroids(the_map, station_y, station_x, asteroid_y, asteroid_x):
    blocked_positions = set()

    y_diff = asteroid_y - station_y
    x_diff = asteroid_x - station_x

    diff_gcd = gcd(y_diff, x_diff)
    y_diff //= diff_gcd
    x_diff //= diff_gcd

    check_y = asteroid_y + y_diff
    check_x = asteroid_x + x_diff
    while 0 <= check_y < the_map.height and 0 <= check_x < the_map.width:
        if the_map[check_y, check_x] == '#':
            blocked_positions.add((check_y, check_x))
        check_y += y_diff
        check_x += x_diff

    return blocked_positions

def count_visible_asteroids(the_map, station_y, station_x):
    blocked = set()
    for y in range(the_map.height):
        for x in range(the_map.width):
            if the_map[y, x] == '#' and (y != station_y or x != station_x):
                blocked.update(get_blocked_asteroids(the_map, station_y, station_x, y, x))

    count = 0
    for y in range(the_map.height):
        for x in range(the_map.width):
            if the_map[y, x] == '#' and (y != station_y or x != station_x) and (y, x) not in blocked:
                count += 1

    return count


def get_best_location_count(the_map):
    counts = []
    for station_y in range(the_map.height):
        for station_x in range(the_map.width):
            if the_map[station_y, station_x] == '#':
                counts.append(((station_y, station_x), count_visible_asteroids(the_map, station_y, station_x)))

    return max(counts, key=lambda tup: tup[1])


def part1():
    the_map = load_map()
    best_count = get_best_location_count(the_map)[1]
    print(f'Part 1: {best_count}')


def asteroid_angle(station_coords, asteroids_coords):
    rad = atan2(station_coords[0] - asteroids_coords[0], asteroids_coords[1] - station_coords[1])
    deg = rad * 180.0/pi
    deg = 90 - deg
    if deg < 0:
        deg += 360

    return deg
    

def asteroid_distance(station_coords, asteroids_coords):
    return abs(station_coords[0] - asteroids_coords[0]) + abs(station_coords[1] - asteroids_coords[1])

def vaporization_sort_key(station_coords, asteroids_coords):
    return (
        asteroid_angle(station_coords, asteroids_coords),
        asteroid_distance(station_coords, asteroids_coords)
    )

def part2():
    the_map = load_map()
    best_location = get_best_location_count(the_map)[0]
    
    asteroid_coords = []
    for y in range(the_map.height):
        for asteroid in range(the_map.width):
            if the_map[y, asteroid] == '#' and (y, asteroid) != best_location:
                asteroid_coords.append((y, asteroid))

    ordered_by_angle_and_distance = list(sorted(
        asteroid_coords,
        key=lambda c: vaporization_sort_key(best_location, c)))

    ordered_without_subsequent_same_angle = []
    while len(ordered_by_angle_and_distance):
        added_this_iteration = []
        last_angle = -1
        for asteroid in ordered_by_angle_and_distance:
            angle = asteroid_angle(best_location, asteroid)
            if abs(angle - last_angle) < 0.000001:
                continue
            ordered_without_subsequent_same_angle.append(asteroid)
            added_this_iteration.append(asteroid)
            last_angle = angle

        for asteroid in added_this_iteration:
            ordered_by_angle_and_distance.remove(asteroid)

    twohundredth = ordered_without_subsequent_same_angle[199]
    print(f'Part 2: {twohundredth[1] * 100 + twohundredth[0]}')


part1()
part2()
