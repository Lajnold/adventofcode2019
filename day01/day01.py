#!/usr/bin/env python3

with open('day01-input.txt') as f:
    modules = [int(line) for line in f.readlines()]

def part1():
    total_fuel = 0
    for mod in modules:
        total_fuel += mod // 3 - 2
    
    print(f'Part 1: {total_fuel}')


def part2():
    total_fuel = 0
    for mod in modules:
        mod_fuel = mod // 3 - 2
        total_fuel += mod_fuel
        while mod_fuel > 0:
            mod_fuel = mod_fuel // 3 - 2
            if mod_fuel > 0:
                total_fuel += mod_fuel
    
    print(f'Part 2: {total_fuel}')


part1()
part2()
