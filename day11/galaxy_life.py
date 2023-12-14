def expand_universe(lines: list[str]) -> list[str]:
    new_lines = list()
    for line in lines:
        new_lines.append(line)
        if all(map(lambda x: x == ".", line.strip())):
            new_lines.append(line)
    cols_to_add = set()
    for j in range(len(new_lines[0])):
        col = list()
        for i in range(len(new_lines)):
            if new_lines[i][j] == ".":
                col.append(True)
            else:
                col.append(False)
        if all(col):
            cols_to_add.add(j)

    for i in range(len(new_lines)):
        new_line = list()
        for j in range(len(new_lines[i])):
            new_line.append(new_lines[i][j])
            if j in cols_to_add:
                new_line.append(".")
        new_lines[i] = new_line
    return new_lines


def get_galaxy_positions(lines: list[str]) -> set[tuple[int, int]]:
    to_ret = set()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "#":
                to_ret.add((len(to_ret), i, j))
    return to_ret


def sum_shortest_paths(galaxies: set[tuple[int, int]]) -> int:
    s = 0
    pairs = set()
    for g_id, i, j in galaxies:
        for dest_g_id, dest_i, dest_j in galaxies:
            if (g_id, dest_g_id) in pairs:
                continue
            s += abs(dest_i - i) + abs(dest_j - j)
            pairs.add((g_id, dest_g_id))
            pairs.add((dest_g_id, g_id))
    return s


def part_one(lines: list[str]) -> int:
    new_lines = expand_universe(lines)
    galaxies = get_galaxy_positions(new_lines)
    return sum_shortest_paths(galaxies)


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(part_one(infile.readlines()))
