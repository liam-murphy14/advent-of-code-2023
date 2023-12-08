from bisect import bisect_left


class MapFunction:
    def __init__(self, start: int = 0, end: int = 0, increment: int = 0):
        self.start = start
        self.end = end
        self.increment = increment

    def __repr__(self):
        return f"{self.start, self.end} -> {self.start + self.increment, self.end + self.increment}"

    def __lt__(self, other_function):
        # default sort by start of range
        return self.start < other_function.start

    def __bool__(self):
        return self.start <= self.end


class MapLayer:
    def __init__(self, map_functions: list[MapFunction]):
        self.map_functions = map_functions

    def combine(self, other_layer):
        self.map_functions.sort(key=lambda f: f.start + f.increment)
        other_layer.map_functions.sort()
        new_layer = list()  # will convert to object at end
        i, j = 0, 0
        while i < len(self.map_functions) or j < len(other_layer.map_functions):
            if i == len(self.map_functions):
                new_layer.append(other_layer.map_functions[j])
                j += 1
                continue
            if j == len(other_layer.map_functions):
                new_layer.append(self.map_functions[i])
                i += 1
                continue

            source_map = self.map_functions[i]
            dest_map = other_layer.map_functions[j]
            source_range_start = source_map.start + source_map.increment
            source_range_end = source_map.end + source_map.increment
            if source_range_start < dest_map.start:
                if source_range_end < dest_map.start:
                    # source misses left
                    new_layer.append(source_map)
                    i += 1
                elif source_range_end < dest_map.end:
                    # source overlaps left
                    first_range = MapFunction(
                        source_map.start,
                        dest_map.start - source_map.increment - 1,
                        source_map.increment,
                    )
                    second_range = MapFunction(
                        dest_map.start - source_map.increment,
                        source_map.start,
                        source_map.increment + dest_map.increment,
                    )
                    new_layer.append(first_range)
                    new_layer.append(second_range)
                    dest_map.start = source_range_end + 1
                    i += 1
                    if not dest_map:
                        j += 1
                else:
                    # source eats destination
                    first_range = MapFunction(
                        source_map.start,
                        dest_map.start - source_map.increment - 1,
                        source_map.increment,
                    )
                    second_range = MapFunction(
                        dest_map.start - source_map.increment,
                        dest_map.end - source_map.increment,
                        source_map.increment + dest_map.increment,
                    )
                    new_layer.append(first_range)
                    new_layer.append(second_range)
                    source_map.start = dest_map.end + 1 - source_map.increment
                    j += 1
                    if not source_map:
                        i += 1

            elif source_range_start >= dest_map.start:
                if source_range_start > dest_map.end:
                    # source misses right
                    new_layer.append(dest_map)
                    j += 1
                elif source_range_end > dest_map.end:
                    # source overlaps right
                    first_range = MapFunction(
                        dest_map.start, source_range_start - 1, dest_map.increment
                    )
                    second_range = MapFunction(
                        source_map.start,
                        dest_map.end - source_map.increment,
                        source_map.increment + dest_map.increment,
                    )
                    new_layer.append(first_range)
                    new_layer.append(second_range)
                    source_map.start = dest_map.end + 1 - source_map.increment
                    j += 1
                    if not source_map:
                        i += 1

                else:
                    # dest eats source
                    first_range = MapFunction(
                        dest_map.start, source_range_start - 1, dest_map.increment
                    )
                    second_range = MapFunction(
                        source_map.start,
                        source_map.end,
                        source_map.increment + dest_map.increment,
                    )
                    new_layer.append(first_range)
                    new_layer.append(second_range)
                    dest_map.start = source_range_end + 1
                    i += 1
                    if not dest_map:
                        j += 1
        return MapLayer(list(filter(lambda m: m.__bool__() == True, new_layer)))

    def get_value_of_point(self, point: int):
        self.map_functions.sort()
        insertion_point = bisect_left(
            list(map(lambda f: f.start, self.map_functions)), point
        )
        if insertion_point == 0:
            return point
        else:
            possible_map = self.map_functions[insertion_point - 1]
            if possible_map.start <= point <= possible_map.end:
                return point + possible_map.increment
            possible_map = self.map_functions[insertion_point]
            if possible_map.start <= point <= possible_map.end:
                return point + possible_map.increment
            return point


def make_total_map(map_lines: list[str]) -> list[tuple[int, int, int]]:
    total_map = list()
    for line in map_lines:
        total_map.append(tuple([int(item) for item in line.strip().split()]))
    return total_map


def parse_problem(
    lines: list[str],
) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    seeds = lines[0].strip().split()[1:]
    seeds = [int(s) for s in seeds]
    map_string_lists = list()
    current_list = list()
    for line in lines[2:]:
        if not line.strip():
            map_string_lists.append(current_list)
            current_list = list()
        else:
            current_list.append(line)
    if current_list:
        map_string_lists.append(current_list)
    map_list = [make_total_map(lines[1:]) for lines in map_string_lists]
    return seeds, map_list


def find_min_location(lines: list[str]):
    seeds, map_list = parse_problem(lines)
    map_layers = list()
    for map_function_list in map_list:
        new_map_layer = list()
        for dest_start, source_start, range_len in map_function_list:
            new_map_fun = MapFunction(
                source_start, source_start + range_len - 1, dest_start - source_start
            )
            new_map_layer.append(new_map_fun)
        map_layers.append(MapLayer(new_map_layer))
    final_map_layer = map_layers[0]
    for dest_map_layer in map_layers[1:]:
        final_map_layer = final_map_layer.combine(dest_map_layer)
    seed_vals = [final_map_layer.get_value_of_point(seed) for seed in seeds]
    return min(seed_vals)


def find_min_location_range(lines: list[str]):
    seeds, map_list = parse_problem(lines)
    seed_map_layer_list = [
        MapFunction(seeds[i], seeds[i] + seeds[i + 1], 0)
        for i in range(0, len(seeds), 2)
    ]
    seed_map_layer = MapLayer(seed_map_layer_list)

    map_layers = [seed_map_layer]
    for map_function_list in map_list:
        new_map_layer = list()
        for dest_start, source_start, range_len in map_function_list:
            new_map_fun = MapFunction(
                source_start, source_start + range_len - 1, dest_start - source_start
            )
            new_map_layer.append(new_map_fun)
        map_layers.append(MapLayer(new_map_layer))
    final_map_layer = map_layers[0]
    for dest_map_layer in map_layers[1:]:
        final_map_layer = final_map_layer.combine(dest_map_layer)
    final_possible_vals = list()
    for fun in final_map_layer.map_functions:
        start_val, final_possible = fun.start, fun.start + fun.increment
        for seed_fun in seed_map_layer.map_functions:
            if seed_fun.start <= start_val <= seed_fun.end:
                final_possible_vals.append(final_possible)
    return min(final_possible_vals)


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(find_min_location_range(infile.readlines()))
