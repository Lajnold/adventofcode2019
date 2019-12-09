#!/usr/bin/env python3

class Intcode:

    def __init__(self, src, input_port, output_port):
        self.memory = dict(enumerate(map(int, src.strip().split(','))))
        self.ip = 0
        self.rb = 0
        self.input_port = input_port
        self.input_idx = 0
        self.output_port = output_port
        self.halted = False
        self.debug_print = False

    def run(self):
        while not self.halted:
            modes, op = self._decode(self._get_value(self.ip))
            self._print_instr(self.memory, self.ip, op)
            if op == 1:
                # add
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                target = self._mode_address(modes, 2)
                self.memory[target] = param1 + param2
                self.ip += 4
            elif op == 2:
                # mul
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                target = self._mode_address(modes, 2)
                self.memory[target] = param1 * param2
                self.ip += 4
            elif op == 3:
                # input
                if self.input_idx >= len(self.input_port):
                    break  # Wait for new input

                target = self._mode_address(modes, 0)
                self.memory[target] = self.input_port[self.input_idx]
                self._print_input(self.input_port, self.input_idx)
                self.input_idx += 1
                self.ip += 2
            elif op == 4:
                # output
                self.output_port.append(self._mode_value(modes, 0))
                self._print_last_output(self.output_port)
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
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                target = self._mode_address(modes, 2)
                self.memory[target] = 1 if param1 < param2 else 0
                self.ip += 4
            elif op == 8:
                # equals
                param1 = self._mode_value(modes, 0)
                param2 = self._mode_value(modes, 1)
                target = self._mode_address(modes, 2)
                self.memory[target] = 1 if param1 == param2 else 0
                self.ip += 4
            elif op == 9:
                # relative-base-offset
                self.rb += self._mode_value(modes, 0)
                self.ip += 2
                pass
            elif op == 99:
                self.halted = True
                break
            else:
                self.halted = True
                raise Exception(f'Unknown op {op} at ip {self.ip}')

    def _decode(self, code):
        code_str = str(code)
        modes = list(map(int, code_str[:-2]))
        modes.reverse()  # Reverse modes to match parameter order in code
        op = int(code_str[-2:])
        return modes, op

    def _get_param(self, param_idx):
        return self._get_value(self.ip + param_idx + 1)

    def _pos_address(self, param_idx):
        return self._get_param(param_idx)

    def _rel_address(self, param_idx):
        return self.rb + self._get_param(param_idx)

    def _mode_address(self, modes, param_idx):
        mode = modes[param_idx] if len(modes) > param_idx else 0
        if mode == 0:
            return self._pos_address(param_idx)
        elif mode == 2:
            return self._rel_address(param_idx)
        else:
            self.halted = True
            raise Exception(f'Invalid address mode {mode}')

    def _pos_value(self, param_idx):
        return self._get_value(self._pos_address(param_idx))

    def _rel_value(self, param_idx):
        return self._get_value(self._rel_address(param_idx))

    def _mode_value(self, modes, param_idx):
        mode = modes[param_idx] if len(modes) > param_idx else 0
        if mode == 0:
            return self._pos_value(param_idx)
        elif mode == 1:
            return self._get_param(param_idx)
        elif mode == 2:
            return self._rel_value(param_idx)
        else:
            self.halted = True
            raise f'Invalid value mode {mode}'

    def _get_value(self, address):
        return self.memory.get(address, 0)

    def _print_instr(self, memory, ip, op):
        if self.debug_print:
            if op in [1, 2, 7, 8]:
                print(f'P: {self._get_value(ip)}, {self._get_value(ip + 1)}, {self._get_value(ip + 2)}, {self._get_value(ip + 3)}')
            elif op in [5, 6]:
                print(f'P: {self._get_value(ip)}, {self._get_value(ip + 1)}, {self._get_value(ip + 2)}')
            elif op in [3, 4, 9]:
                print(f'P: {self._get_value(ip)}, {self._get_value(ip + 1)}')
            elif op in [99]:
                print(f'P: {self._get_value(ip)}')
            else:
                self.halted = True
                raise Exception(f'Invalid instruction: {op}')

    def _print_input(self, inputs, idx):
        if self.debug_print:
            print(f'I: {inputs[idx]}')

    def _print_last_output(self, outputs):
        if self.debug_print:
            print(f'O: {outputs[-1]}')


def load_src():
    with open('day09-input.txt') as f:
        return f.read()


def part1():
    src = load_src()
    input_port = [1]
    output_port = []
    program = Intcode(src, input_port, output_port)
    program.debug_print = False
    program.run()
    print(f'Part 1: {output_port}')


def part2():
    src = load_src()
    input_port = [2]
    output_port = []
    program = Intcode(src, input_port, output_port)
    program.debug_print = False
    program.run()
    print(f'Part 2: {output_port}')

part1()
part2()
