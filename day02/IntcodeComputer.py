OPCODE_PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,10,23,27,2,27,13,31,1,10,31,35,1,35,9,39,2,39,13,43,1,43,5,47,1,47,6,51,2,6,51,55,1,5,55,59,2,9,59,63,2,6,63,67,1,13,67,71,1,9,71,75,2,13,75,79,1,79,10,83,2,83,9,87,1,5,87,91,2,91,6,95,2,13,95,99,1,99,5,103,1,103,2,107,1,107,10,0,99,2,0,14,0]


class IntcodeComputer:

    def __init__(self, program):
        self.program = program
        self.program_complete = False

    def process_opcode(self, position):
        if self.program[position] == 1:
            num1 = self.program[self.program[position + 1]]
            num2 = self.program[self.program[position + 2]]
            self.program[self.program[position + 3]] = num1 + num2

        elif self.program[position] == 2:
            num1 = self.program[self.program[position + 1]]
            num2 = self.program[self.program[position + 2]]
            self.program[self.program[position + 3]] = num1 * num2

        elif self.program[position] == 99:
            self.program_complete = True

        else:
            raise Exception("Unknown opcode encountered.")

    def run_program(self, noun, verb):
        self.program[1] = noun
        self.program[2] = verb
        program_position = 0
        while not self.program_complete:
            self.process_opcode(program_position)
            program_position += 4

        return self.program[0]


if __name__ == "__main__":
    for noun in range(0, 99):
        for verb in range(0, 99):
            computer = IntcodeComputer(list(OPCODE_PROGRAM))
            if computer.run_program(noun, verb) == 19690720:
                print("Noun: {}     Verb: {}".format(noun, verb))
