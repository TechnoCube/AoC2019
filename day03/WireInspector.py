WIRE_GRID_SIZE = 25000


class WireInspector:
    def __init__(self, wire_paths_file_location):
        self.wire_grid = [['o' for x in range(WIRE_GRID_SIZE)] for y in range(WIRE_GRID_SIZE)]
        wire_paths = open(wire_paths_file_location)
        self.path1 = wire_paths.readline()
        self.path1 = self.path1.split(",")
        self.path2 = wire_paths.readline()
        self.path2 = self.path2.split(",")
        self.intersections = []
        self.intersection_step_info = {}

    def trace_wire_a(self):
        x = int(WIRE_GRID_SIZE / 2)
        y = int(WIRE_GRID_SIZE / 2)  # the starting point is the center of the grid
        for vector in self.path1:
            direction = vector[0]
            distance = int(vector[1:])
            for i in range(distance):
                if direction == 'U':
                    y += 1

                elif direction == 'D':
                    y -= 1

                elif direction == 'R':
                    x += 1

                elif direction == 'L':
                    x -= 1

                else:
                    raise Exception("Invalid wire direction vector")

                self.wire_grid[x][y] = 'a'

    def trace_wire_b(self):
        x = int(WIRE_GRID_SIZE / 2)
        y = int(WIRE_GRID_SIZE / 2)  # the starting point is the center of the grid
        steps = 0
        for vector in self.path2:
            direction = vector[0]
            distance = int(vector[1:])
            for i in range(distance):
                steps += 1
                if direction == 'U':
                    y += 1

                elif direction == 'D':
                    y -= 1

                elif direction == 'R':
                    x += 1

                elif direction == 'L':
                    x -= 1

                else:
                    raise Exception("Invalid wire direction vector")

                if self.wire_grid[x][y] == 'a' or self.wire_grid[x][y] == '+':
                    self.wire_grid[x][y] = '+'
                    self.intersection_step_info["{},{}".format(x, y)] = steps
                else:
                    self.wire_grid[x][y] = 'b'

    def retrace_wire_a(self):
        x = int(WIRE_GRID_SIZE / 2)
        y = int(WIRE_GRID_SIZE / 2)  # the starting point is the center of the grid
        steps = 0
        for vector in self.path1:
            direction = vector[0]
            distance = int(vector[1:])
            for i in range(distance):
                steps += 1
                if direction == 'U':
                    y += 1

                elif direction == 'D':
                    y -= 1

                elif direction == 'R':
                    x += 1

                elif direction == 'L':
                    x -= 1

                else:
                    raise Exception("Invalid wire direction vector")

                if self.wire_grid[x][y] == '+':
                    self.wire_grid[x][y] = 'x'
                    self.intersection_step_info["{},{}".format(x, y)] += steps

    def find_nearest_intersection(self):
        center = int(WIRE_GRID_SIZE / 2)
        for x in range(WIRE_GRID_SIZE):
            for y in range(WIRE_GRID_SIZE):
                if self.wire_grid[x][y] == '+':
                    xdist = abs(x - center)
                    ydist = abs(y - center)
                    self.intersections.append(xdist + ydist)

        return min(self.intersections)


if __name__ == "__main__":
    inspector = WireInspector(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\wire_paths.txt")
    inspector.trace_wire_a()
    inspector.trace_wire_b()
    inspector.retrace_wire_a()
    print(min(inspector.intersection_step_info.values()))
