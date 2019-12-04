#!/usr/bin/env python3

password_range = (240920, 789857)

def matches_criteria_part1(num):
    # The value is within the given range.
    if num < password_range[0] or num > password_range[1]:
        return False

    # Two adjacent digits are the same.
    adjacent = False
    as_str = str(num)
    for i in range(len(as_str) - 1):
        if as_str[i] == as_str[i + 1]:
            adjacent = True
    if not adjacent:
        return False

    # Going from left to right, the digits never decrease.
    decreases = False
    for i in range(len(as_str) - 1):
        if as_str[i] > as_str[i + 1]:
            decreases = True
    if decreases:
        return False

    return True


def part1():
    num_matches = 0
    for i in range(password_range[0], password_range[1] + 1):
        if matches_criteria_part1(i):
            num_matches += 1

    print(f'Part 1: {num_matches}')


def matches_criteria_part2(num):
    # The value is within the given range.
    if num < password_range[0] or num > password_range[1]:
        return False

    # Two adjacent digits are the same. There must be two same adjacent digits not part of a
    # larger group; larger groups don't count.
    adjacent = False
    as_str = str(num)
    for i in range(len(as_str) - 1):
        chr = as_str[i]
        if (chr == as_str[i + 1]
                and (i == 0 or chr != as_str[i - 1])
                and (i == len(as_str) - 2 or chr != as_str[i + 2])):
            adjacent = True
    if not adjacent:
        return False

    # Going from left to right, the digits never decrease.
    decreases = False
    for i in range(len(as_str) - 1):
        if as_str[i] > as_str[i + 1]:
            decreases = True
    if decreases:
        return False

    return True


def part2():
    num_matches = 0
    for i in range(password_range[0], password_range[1] + 1):
        if matches_criteria_part2(i):
            num_matches += 1

    print(f'Part 2: {num_matches}')

part1()
part2()
