#!/usr/bin/env python3

with open('day02-input.txt') as f:
    initial_state = [int(x) for x in f.read().strip().split(',')]


def run_program(state):
    ip = 0
    while True:
        op = state[ip]
        if op == 1:
            state[state[ip + 3]] = state[state[ip + 1]] + state[state[ip + 2]]
        elif op == 2:
            state[state[ip + 3]] = state[state[ip + 1]] * state[state[ip + 2]]
        elif op == 99:
            break
        else:
            print(f'Unknown op {op} at ip {ip}')

        ip += 4


def part1():
    state = list(initial_state)
    state[1], state[2] = 12, 2
    run_program(state)
    print(f'Part 1: {state[0]}')


def part2():
    target = 19690720

    noun, verb = 0, 0
    while True:
        state = list(initial_state)
        state[1], state[2] = noun, verb
        run_program(state)

        if state[0] == target:
            print(f'Part 2: 100 * {noun} + {verb} == {100 * noun + verb}')
            break

        verb += 1
        if verb == 100:
            verb = 0
            noun += 1

part1()
part2()
