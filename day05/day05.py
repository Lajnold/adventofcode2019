#!/usr/bin/env python3

debug_print = False

def print_instr(state, ip, op):
    if debug_print:
        if op == 1 or op == 2:
            print(f'P: {state[ip]}, {state[ip + 1]}, {state[ip + 2]}, {state[ip + 3]}')
        elif op == 3 or op == 4:
            print(f'P: {state[ip]}, {state[ip + 1]}')
        else:
            print(f'P: {state[ip]}')

def print_input(inputs, idx):
    if debug_print:
        print(f'I: {inputs[idx]}')

def print_last_output(outputs):
    if debug_print:
        print(f'O: {outputs[-1]}')


with open('day05-input.txt') as f:
    # 1002,4,3,4,33
    # 11002,4,3,4,33
    program = list(map(int, f.read().strip().split(',')))


def decode(code):
    code_str = str(code)
    modes = list(map(int, code_str[:-2]))
    modes.reverse()  # Reverse modes to match parameter order in code
    op = int(code_str[-2:])
    return modes, op

def imm_value(state, ip, param_idx):
    return state[ip + param_idx + 1]

def pos_value(state, ip, param_idx):
    pos = state[ip + param_idx + 1]
    return state[pos]

def mode_value(state, ip, modes, param_idx):
    mode = modes[-param_idx] if len(modes) > param_idx else 0
    if mode == 0:
        return pos_value(state, ip, param_idx)
    else:
        return imm_value(state, ip, param_idx)

def run_program(state, inputs, outputs):
    ip = 0
    input_idx = 0
    while True:
        modes, op = decode(state[ip])
        print_instr(state, ip, op)
        if op == 1:
            # add
            target = state[ip + 3]
            param1 = mode_value(state, ip, modes, 0)
            param2 = mode_value(state, ip, modes, 1)
            state[target] = param1 + param2
            ip += 4
        elif op == 2:
            # mul
            target = state[ip + 3]
            param1 = mode_value(state, ip, modes, 0)
            param2 = mode_value(state, ip, modes, 1)
            state[target] = param1 * param2
            ip += 4
        elif op == 3:
            # input
            target = state[ip + 1]
            state[target] = inputs[input_idx]
            print_input(inputs, input_idx)
            input_idx += 1
            ip += 2
        elif op == 4:
            # output
            outputs.append(mode_value(state, ip, modes, 0))
            print_last_output(outputs)
            ip += 2
        elif op == 5:
            # jump-if-true
            if mode_value(state, ip, modes, 0) != 0:
                ip = mode_value(state, ip, modes, 1)
            else:
                ip += 3
        elif op == 6:
            # jump-if-false
            if mode_value(state, ip, modes, 0) == 0:
                ip = mode_value(state, ip, modes, 1)
            else:
                ip += 3
        elif op == 7:
            # less-than
            target = state[ip + 3]
            param1 = mode_value(state, ip, modes, 0)
            param2 = mode_value(state, ip, modes, 1)
            state[target] = 1 if param1 < param2 else 0
            ip += 4
        elif op == 8:
            # equals
            target = state[ip + 3]
            param1 = mode_value(state, ip, modes, 0)
            param2 = mode_value(state, ip, modes, 1)
            state[target] = 1 if param1 == param2 else 0
            ip += 4
        elif op == 99:
            break
        else:
            print(f'Unknown op {op} at ip {ip}')
            return


def part1():
    state = list(program)
    inputs = [1]
    outputs = []
    run_program(state, inputs, outputs)
    print(f'Part 1: {outputs}')


def part2():
    state = list(program)
    inputs = [5]
    outputs = []
    run_program(state, inputs, outputs)
    print(f'Part 2: {outputs}')

part1()
part2()
