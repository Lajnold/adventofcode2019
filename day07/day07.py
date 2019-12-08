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


class Intcode:

    def __init__(self, src, input_port, output_port):
        self.memory = list(map(int, src.strip().split(',')))
        self.ip = 0
        self.input_port = input_port
        self.input_idx = 0
        self.output_port = output_port
        self.halted = False

    def run(self):
        while not self.halted:
            modes, op = self._decode(self.memory[self.ip])
            print_instr(self.memory, self.ip, op)
            if op == 1:
                # add
                target = self.memory[self.ip + 3]
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                self.memory[target] = param1 + param2
                self.ip += 4
            elif op == 2:
                # mul
                target = self.memory[self.ip + 3]
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                self.memory[target] = param1 * param2
                self.ip += 4
            elif op == 3:
                # input
                if self.input_idx >= len(self.input_port):
                    break  # Wait for new input

                target = self.memory[self.ip + 1]
                self.memory[target] = self.input_port[self.input_idx]
                print_input(self.input_port, self.input_idx)
                self.input_idx += 1
                self.ip += 2
            elif op == 4:
                # output
                self.output_port.append(self._mode_value(modes, 0))
                print_last_output(self.output_port)
                self.ip += 2
            elif op == 5:
                # jump-if-true
                if self._mode_value(modes, 0) != 0:
                    self.ip = self._mode_value(modes, 1)
                else:
                    self.ip += 3
            elif op == 6:
                # jump-if-false
                if self._mode_value(modes, 0) == 0:
                    self.ip = self._mode_value(modes, 1)
                else:
                    self.ip += 3
            elif op == 7:
                # less-than
                target = self.memory[self.ip + 3]
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                self.memory[target] = 1 if param1 < param2 else 0
                self.ip += 4
            elif op == 8:
                # equals
                target = self.memory[self.ip + 3]
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                self.memory[target] = 1 if param1 == param2 else 0
                self.ip += 4
            elif op == 99:
                self.halted = True
                break
            else:
                print(f'Unknown op {op} at ip {self.ip}')
                self.halted = True
                break

    def _decode(self, code):
        code_str = str(code)
        modes = list(map(int, code_str[:-2]))
        modes.reverse()  # Reverse modes to match parameter order in code
        op = int(code_str[-2:])
        return modes, op

    def _imm_value(self, param_idx):
        return self.memory[self.ip + param_idx + 1]

    def _pos_value(self, param_idx):
        pos = self.memory[self.ip + param_idx + 1]
        return self.memory[pos]

    def _mode_value(self, modes, param_idx):
        mode = modes[-param_idx] if len(modes) > param_idx else 0
        if mode == 0:
            return self._pos_value(param_idx)
        else:
            return self._imm_value(param_idx)


def load_src():
    with open('day07-input.txt') as f:
        return f.read()


def gen_phase_combinations(start, stop):
    for p1 in range(start, stop):
        for p2 in range(start, stop):
            if p2 == p1: continue
            for p3 in range(start, stop):
                if p3 in [p1, p2]: continue
                for p4 in range(start, stop):
                    if p4 in [p1, p2, p3]: continue
                    for p5 in range(start, stop):
                        if p5 in [p1, p2, p3, p4]: continue
                        yield (p1, p2, p3, p4, p5)


def part1_run_with_phases(src, phases):
    prev_output = 0
    for i in range(5):
        input_port = [phases[i], prev_output]
        output_port = []
        amp = Intcode(src, input_port, output_port)
        amp.run()
        prev_output = output_port[-1]

    return prev_output

def part1():
    src = load_src()

    signals = []
    for phases in gen_phase_combinations(0, 5):
        signals.append(part1_run_with_phases(src, phases))

    print(f'Part 1: {max(signals)}')


def part2_run_with_phases(src, phases):
    output_port = []
    amps = []
    for i in range(5):
        prev_output_port = output_port
        output_port = []
        amps.append(Intcode(src, prev_output_port, output_port))

    amps[0].input_port = amps[-1].output_port
    
    for i in range(5):
        amps[i].input_port.append(phases[i])
        if i == 0:
            amps[i].input_port.append(0)

    while not amps[-1].halted:
        for amp in amps:
            amp.run()

    return amps[-1].output_port[-1]

def part2():
    src = load_src()
    
    signals = []
    for phases in gen_phase_combinations(5, 10):
        signals.append(part2_run_with_phases(src, phases))

    print(f'Part 2: {max(signals)}')

part1()
part2()
