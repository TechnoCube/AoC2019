import math


class FuelCalculator:
    def calculate(self, mass: int):
        retval = mass / 3
        retval = math.floor(retval)
        retval -= 2
        if (retval > 0):
            return retval + self.calculate(retval)
        return 0

    def open_inputs(self, filepath):
        file = open(filepath, "r")
        inputs = file.readlines()
        return inputs

    def total_fuel_required(self):
        total = 0
        for mass in self.open_inputs(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\fuel_calculation_input.txt"):
            total += self.calculate(int(mass))
        print("Total fuel needed: {}".format(total))


if __name__ == "__main__":
    calc = FuelCalculator()
    calc.total_fuel_required()
