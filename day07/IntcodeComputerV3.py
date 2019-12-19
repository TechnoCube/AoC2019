import itertools


def read_program(filepath):
    file = open(filepath, "r")
    program = file.read()
    return [int(n) for n in program.split(",")]


class IntcodeComputer:

    def __init__(self, program, phase):
        self.program = program
        self.program_complete = False
        self.program_position = 0
        self.inputs = [phase]
        self.output = 0
        self.program_output = False

    def reset_program(self):
        self.program_complete = False
        self.program_position = 0

    def retrieve_input(self):
        return self.inputs.pop(0)

    def process_output(self, output):
        self.output = output
        self.program_output = True

    def parse_instruction(self, position):
        instruction = str(self.program[position])

        if len(instruction) == 1:
            return int(instruction), (0, 0, 0)

        elif len(instruction) == 2:
            return int(instruction), (0, 0, 0)

        elif len(instruction) == 3:
            mode1 = int(instruction[0])
            return int(instruction[-2:]), (mode1, 0, 0)

        elif len(instruction) == 4:
            mode1 = int(instruction[1])
            mode2 = int(instruction[0])
            return int(instruction[-2:]), (mode1, mode2, 0)

        elif len(instruction) == 5:
            mode1 = int(instruction[2])
            mode2 = int(instruction[1])
            mode3 = int(instruction[0])
            return int(instruction[-2:]), (mode1, mode2, mode3)

        else:
            raise Exception("Unable to parse instruction")

    def get_parameter_values(self, num_of_params, param_modes, pos):
        if num_of_params == 1:
            value1 = self.program[pos + 1] if param_modes[0] == 1 else self.program[self.program[pos + 1]]
            return value1

        elif num_of_params == 2:
            value1 = self.program[pos + 1] if param_modes[0] == 1 else self.program[self.program[pos + 1]]
            value2 = self.program[pos + 2] if param_modes[1] == 1 else self.program[self.program[pos + 2]]
            return value1, value2

        else:
            raise Exception("Unable to get that number of parameters")

    def process_instruction(self):
        opcode, parameter_modes = self.parse_instruction(self.program_position)

        #  Add
        if opcode == 1:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            self.program[self.program[self.program_position + 3]] = value1 + value2
            self.program_position += 4

        #  Multiply
        elif opcode == 2:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            self.program[self.program[self.program_position + 3]] = value1 * value2
            self.program_position += 4

        #  Input
        elif opcode == 3:
            value = self.retrieve_input()
            self.program[self.program[self.program_position + 1]] = value
            self.program_position += 2

        #  Output
        elif opcode == 4:
            value1 = self.get_parameter_values(1, parameter_modes, self.program_position)
            self.process_output(value1)
            self.program_position += 2

        #  Jump if true
        elif opcode == 5:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if value1 != 0:
                self.program_position = value2
            else:
                self.program_position += 3

        #  Jump if false
        elif opcode == 6:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if value1 == 0:
                self.program_position = value2
            else:
                self.program_position += 3

        #  Less than
        elif opcode == 7:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if value1 < value2:
                self.program[self.program[self.program_position + 3]] = 1
            else:
                self.program[self.program[self.program_position + 3]] = 0
            self.program_position += 4

        #  Equals
        elif opcode == 8:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if value1 == value2:
                self.program[self.program[self.program_position + 3]] = 1
            else:
                self.program[self.program[self.program_position + 3]] = 0
            self.program_position += 4

        #  Exit
        elif opcode == 99:
            self.program_complete = True

        else:
            raise Exception("Unknown opcode encountered.")

    def run_program_part1(self, program):
        sequences = list(itertools.permutations([0, 1, 2, 3, 4]))
        thruster_signals = {}

        for phase_settings in sequences:
            amp_output = 0
            for setting in phase_settings:
                self.reset_program()
                self.program = program.copy()
                self.inputs.append(setting)
                self.inputs.append(amp_output)

                while not self.program_complete:
                    self.process_instruction()
                amp_output = self.output

            thruster_signals[amp_output] = phase_settings

        max_thruster_signal = max(thruster_signals.keys())
        print("{} is the maximum output, by using the following phase setting sequence: {}".format(max_thruster_signal, thruster_signals[max_thruster_signal]))

    def run_program_until_output(self):
        self.program_output = False
        while not self.program_output and not self.program_complete:
            self.process_instruction()

        return self.output


def run_full_feedback_loop(program, phase_values):
    amplifiers = [IntcodeComputer(program.copy(), phase) for phase in phase_values]
    amplifier_index = 0
    amp_output = 0

    #  Continue looping until the final amplifier's program is complete
    while not amplifiers[len(amplifiers) - 1].program_complete:
        current_amp = amplifiers[amplifier_index]
        current_amp.inputs.append(amp_output)
        amp_output = current_amp.run_program_until_output()
        amplifier_index = (amplifier_index + 1) % len(amplifiers)

    return amp_output


if __name__ == "__main__":
    prog = read_program(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\AoC2019\day07\amplifier_program.txt")
    sequences = list(itertools.permutations([5, 6, 7, 8, 9]))
    thruster_signals = {}

    for phase_settings in sequences:
        thruster_signals[run_full_feedback_loop(prog, phase_settings)] = phase_settings

    max_thruster_signal = max(thruster_signals.keys())
    print("{} is the maximum output, by using the following phase setting sequence: {}"
          .format(max_thruster_signal, thruster_signals[max_thruster_signal]))
