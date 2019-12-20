ALLOCATED_MEMORY = 65536


def read_program(filepath):
    file = open(filepath, "r")
    program = file.read()
    return [int(n) for n in program.split(",")]


class IntcodeComputer:

    def __init__(self, program, starting_input):
        self.program = program
        self.program.extend([0] * (ALLOCATED_MEMORY - len(program)))
        self.program_complete = False
        self.program_position = 0
        self.inputs = [starting_input]
        self.output = 0
        self.program_output = False
        self.relative_base = 0

    def reset_program(self):
        self.program_complete = False
        self.program_position = 0

    def retrieve_input(self):
        return self.inputs.pop(0)

    def process_output(self, output):
        self.output = output
        self.program_output = True
        print("The BOOST program outputs a value: {}".format(output))

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
        value1, value2 = None, None
        if num_of_params >= 1:
            if param_modes[0] == 1:  # Immediate mode
                value1 = self.program[pos + 1]
            elif param_modes[0] == 2:  # Relative mode (relative base + offset)
                value1 = self.program[self.relative_base + self.program[pos + 1]]
            else:  # Position mode / default
                value1 = self.program[self.program[pos + 1]]

        #  If only one parameter is needed, return now
        if num_of_params == 1:
            return value1

        elif num_of_params >= 2:
            if param_modes[1] == 1:  # Immediate mode
                value2 = self.program[pos + 2]
            elif param_modes[1] == 2:  # Relative mode (relative base + offset)
                value2 = self.program[self.relative_base + self.program[pos + 2]]
            else:  # Position mode / default
                value2 = self.program[self.program[pos + 2]]
            return value1, value2

        else:
            raise Exception("Unable to get that number of parameters")

    def process_instruction(self):
        opcode, parameter_modes = self.parse_instruction(self.program_position)

        #  Add
        if opcode == 1:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if parameter_modes[2] == 2:  # Store result in relative mode
                self.program[self.relative_base + self.program[self.program_position + 3]] = value1 + value2
            else:  # Store result in position mode / default
                self.program[self.program[self.program_position + 3]] = value1 + value2
            self.program_position += 4

        #  Multiply
        elif opcode == 2:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            if parameter_modes[2] == 2:  # Store result in relative mode
                self.program[self.relative_base + self.program[self.program_position + 3]] = value1 * value2
            else:  # Store result in position mode / default
                self.program[self.program[self.program_position + 3]] = value1 * value2
            self.program_position += 4

        #  Input
        elif opcode == 3:
            value = self.retrieve_input()
            if parameter_modes[2] == 2:  # Store result in relative mode
                self.program[self.relative_base + self.program[self.program_position + 3]] = value
            else:  # Store result in position mode / default
                self.program[self.program[self.program_position + 3]] = value
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
            result = 1 if value1 < value2 else 0

            if parameter_modes[2] == 2:  # Store result in relative mode
                self.program[self.relative_base + self.program[self.program_position + 3]] = result
            else:  # Store result in position mode / default
                self.program[self.program[self.program_position + 3]] = result
            self.program_position += 4

        #  Equals
        elif opcode == 8:
            value1, value2 = self.get_parameter_values(2, parameter_modes, self.program_position)
            result = 1 if value1 == value2 else 0

            if parameter_modes[2] == 2:  # Store result in relative mode
                self.program[self.relative_base + self.program[self.program_position + 3]] = result
            else:  # Store result in position mode / default
                self.program[self.program[self.program_position + 3]] = result
            self.program_position += 4

        #  Relative base offset
        elif opcode == 9:
            value1 = self.get_parameter_values(1, parameter_modes, self.program_position)
            self.relative_base += value1
            self.program_position += 2

        #  Exit
        elif opcode == 99:
            self.program_complete = True

        else:
            raise Exception("Unknown opcode encountered.")

    def run_program_until_output(self):
        self.program_output = False
        while not self.program_output and not self.program_complete:
            self.process_instruction()

        return self.output

    def run_program(self):
        while not self.program_complete:
            self.process_instruction()


if __name__ == "__main__":
    prog = read_program(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\AoC2019\day09\boost_program.txt")
    computer = IntcodeComputer(prog, 2)
    computer.run_program()
