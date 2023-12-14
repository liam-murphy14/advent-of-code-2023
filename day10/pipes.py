from collections import deque

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}


def parse_problem(lines: list[str]) -> tuple[tuple[int, int], list[str]]:
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "S":
                return (i, j), lines
    raise ValueError(f"error parsing problem, {lines}")


def get_possible_next_steps(lines: list[str], i: int, j: int) -> set[tuple[int, int]]:
    if not 0 <= i < len(lines) or not 0 <= j < len(lines[i]):
        return set()
    if lines[i][j] == "S":
        return {(i + DIRS[key][0], j + DIRS[key][1], key) for key in DIRS}
    if lines[i][j] == "-":
        to_ret = set()
        for d in ["E", "W"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == "|":
        to_ret = set()
        for d in ["N", "S"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == "L":
        to_ret = set()
        for d in ["N", "E"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == "J":
        to_ret = set()
        for d in ["N", "W"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == "7":
        to_ret = set()
        for d in ["S", "W"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == "F":
        to_ret = set()
        for d in ["S", "E"]:
            di, dj = DIRS[d]
            to_ret.add((i + di, j + dj, d))
        return to_ret
    if lines[i][j] == ".":
        return set()
    raise ValueError(f"getting value for ({i}, {j}): {lines[i][j]}")


def get_next_step(
    lines: list[str], i: int, j: int, last_i: int, last_j: int
) -> set[tuple[int, int]]:
    possible_nexts = get_possible_next_steps(lines, i, j)
    to_rem = list()
    for tup in possible_nexts:
        test_i, test_j, direction = tup
        if last_i == test_i and last_j == test_j:
            to_rem.append(tup)
        if not 0 <= test_i < len(lines) or not 0 <= test_j < len(lines[i]):
            to_rem.append(tup)
    for tup in to_rem:
        if tup not in possible_nexts:
            continue
        possible_nexts.remove(tup)
    return possible_nexts


def trace_path_distance(
    lines: list[str], start_i: int, start_j: int, start_dir: str
) -> int:
    visited = set()
    di, dj = DIRS[start_dir]
    q = deque()
    q.append((start_i + di, start_j + dj, start_i, start_j, 1))
    while q:
        i, j, last_i, last_j, distance = q.popleft()
        if i == start_i and j == start_j:
            return distance
        if (i, j) in visited:
            return -1
        visited.add((i, j))
        next_steps = get_next_step(lines, i, j, last_i, last_j)
        for new_i, new_j, direction in next_steps:
            q.append((new_i, new_j, i, j, distance + 1))
    return -1


def part_one(lines: list[str]) -> int:
    (start_i, start_j), lines = parse_problem(lines)
    for start_dir in DIRS:
        path_dist = trace_path_distance(lines, start_i, start_j, start_dir)
        if path_dist != -1:
            return path_dist // 2
    return -1


def part_two(lines: list[str]) -> int:
    (start_i, start_j), lines = parse_problem(lines)
    for start_dir in DIRS:
        path_dist, lr_balance, visited_nodes = trace_path_distance_and_orientation(
            lines, start_i, start_j, start_dir
        )
        if path_dist != -1:
            return get_fill(lines, lr_balance, visited_nodes)
    return -1


def get_fill(
    lines: list[str], lr_balance: int, visited_nodes: set[tuple[int, int, str]]
) -> int:
    area = 0
    flooded_nodes = {(i, j) for i, j, direction in visited_nodes}
    for i, j, direction in visited_nodes:
        area += flood(lines, lr_balance, i, j, direction, flooded_nodes)
    return area


def flood(
    lines: list[str],
    lr_balance: int,
    i: int,
    j: int,
    direction: str,
    flooded_nodes: set[tuple[int, int]],
) -> int:
    inner_dirs = set()
    if lr_balance < 0:
        if direction == "N":
            inner_dirs.add(DIRS["W"])
            if lines[i][j] == "F":
                inner_dirs.add(DIRS["N"])
        if direction == "E":
            inner_dirs.add(DIRS["N"])
            if lines[i][j] == "7":
                inner_dirs.add(DIRS["E"])
        if direction == "S":
            inner_dirs.add(DIRS["E"])
            if lines[i][j] == "J":
                inner_dirs.add(DIRS["S"])
        if direction == "W":
            inner_dirs.add(DIRS["S"])
            if lines[i][j] == "L":
                inner_dirs.add(DIRS["W"])
    elif lr_balance > 0:
        if direction == "N":
            inner_dirs.add(DIRS["E"])
            if lines[i][j] == "7":
                inner_dirs.add(DIRS["N"])
        if direction == "E":
            inner_dirs.add(DIRS["S"])
            if lines[i][j] == "J":
                inner_dirs.add(DIRS["E"])
        if direction == "S":
            inner_dirs.add(DIRS["W"])
            if lines[i][j] == "L":
                inner_dirs.add(DIRS["S"])
        if direction == "W":
            inner_dirs.add(DIRS["N"])
            if lines[i][j] == "F":
                inner_dirs.add(DIRS["W"])
    if not inner_dirs:
        raise ValueError(f"error flooding {lr_balance, i, j, direction}")
    return sum((flood_fill(i + di, j + dj, flooded_nodes) for di, dj in inner_dirs))


def flood_fill(i, j, flooded_nodes):
    if (i, j) in flooded_nodes:
        return 0
    total = 1
    flooded_nodes.add((i, j))
    for di, dj in DIRS.values():
        total += flood_fill(i + di, j + dj, flooded_nodes)
    return total


def trace_path_distance_and_orientation(
    lines: list[str], start_i: int, start_j: int, start_dir: str
) -> int:
    visited = set()
    lr_balance = 0  # negative is left, positive right
    di, dj = DIRS[start_dir]
    q = deque()
    q.append((start_i + di, start_j + dj, start_i, start_j, 1, start_dir))
    while q:
        i, j, last_i, last_j, distance, last_dir = q.popleft()
        if i == start_i and j == start_j:
            visited.add((i, j, last_dir))
            return distance, lr_balance, visited
        if (i, j, last_dir) in visited:
            return -1, 100000, set()
        visited.add((i, j, last_dir))
        next_steps = get_next_step(lines, i, j, last_i, last_j)

        for new_i, new_j, direction in next_steps:
            to_add_to_dir = get_direction_difference(last_dir, direction)
            lr_balance += to_add_to_dir
            q.append((new_i, new_j, i, j, distance + 1, direction))
    return -1, 100000, set()


def get_direction_difference(last_dir: str, new_dir: str) -> int:
    if last_dir == new_dir:
        return 0
    if last_dir == "N":
        if new_dir == "E":
            return 1
        if new_dir == "W":
            return -1
    elif last_dir == "E":
        if new_dir == "N":
            return -1
        if new_dir == "S":
            return 1
    elif last_dir == "S":
        if new_dir == "E":
            return -1
        if new_dir == "W":
            return 1
    elif last_dir == "W":
        if new_dir == "N":
            return 1
        if new_dir == "S":
            return -1
    raise ValueError(f"Error getting direction difference for {last_dir} -> {new_dir}")


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(part_two(infile.readlines()))
