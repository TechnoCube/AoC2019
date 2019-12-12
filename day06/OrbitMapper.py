from anytree import Node, PreOrderIter, Walker


def read_map(filepath):
    file = open(filepath, "r")
    return file.read().splitlines()


def build_orbit_tree(map):
    #  Create dictionary for quick node lookup during tree building
    orbit_dictionary = {}
    for orbit in map:
        planets = orbit.split(")")

        #  Check if the center planet node already exists or needs to be created
        if planets[0] in orbit_dictionary:
            center_planet_node = orbit_dictionary[planets[0]]
        else:
            center_planet_node = Node(planets[0])
            orbit_dictionary[planets[0]] = center_planet_node

        #  Check if orbiting planet node exists and set the center planet node as the parent
        if planets[1] in orbit_dictionary:
            orbit_dictionary[planets[1]].parent = center_planet_node
        else:
            orbit_planet_node = Node(planets[1], parent=center_planet_node)
            orbit_dictionary[planets[1]] = orbit_planet_node

    #  After the map has been processed, return the COM node and the SAN and YOU nodes for part 2
    return orbit_dictionary["COM"], orbit_dictionary["YOU"], orbit_dictionary["SAN"]


def count_orbits(orbit_tree_head_node):
    total = 0
    for orbit_node in PreOrderIter(orbit_tree_head_node):
        total += orbit_node.depth
    return total


def count_orbit_jumps(origin, destination):
    walker = Walker()
    up, common, down = walker.walk(origin, destination)
    return len(up) + len(down) - 2  # Subtract 2 since the origin and destination themselves do not require jumps


if __name__ == "__main__":
    map = read_map(r"C:\Users\pafrankl\PycharmProjects\AdventOfCode\day06\orbit_map.txt")
    orbit_tree_head, you_node, san_node = build_orbit_tree(map)
    print("Total orbits: {}".format(count_orbits(orbit_tree_head)))
    print("Orbital transfers from you to Santa: {}".format(count_orbit_jumps(you_node, san_node)))
