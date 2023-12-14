def expand_universe(lines: list[str]) -> tuple[set[str], set[str]]:
    row_blanks, col_blanks = set(), set()
    for i, line in enumerate(lines):
        if all(map(lambda x: x == ".", line.strip())):
            row_blanks.add(i)
    for j in range(len(lines[0])):
        col = list()
        for i in range(len(lines)):
            if lines[i][j] == ".":
                col.append(True)
            else:
                col.append(False)
        if all(col):
            col_blanks.add(j)

    return row_blanks, col_blanks


def get_galaxy_positions(lines: list[str]) -> set[tuple[int, int]]:
    to_ret = set()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "#":
                to_ret.add((len(to_ret), i, j))
    return to_ret


def sum_shortest_paths(
    galaxies: set[tuple[int, int]],
    row_blanks: set[str],
    col_blanks: set[str],
    expansion_factor: int = 1,
) -> int:
    s = 0
    pairs = set()
    expansion_factor = expansion_factor - 1
    for g_id, i, j in galaxies:
        for dest_g_id, dest_i, dest_j in galaxies:
            if (g_id, dest_g_id) in pairs:
                continue
            s += (
                abs(dest_i - i)
                + abs(dest_j - j)
                + expansion_factor
                * len(
                    [row for row in row_blanks if i < row < dest_i or dest_i < row < i]
                )
                + expansion_factor
                * len(
                    [col for col in col_blanks if j < col < dest_j or dest_j < col < j]
                )
            )
            pairs.add((g_id, dest_g_id))
            pairs.add((dest_g_id, g_id))
    return s


def part_one(lines: list[str]) -> int:
    row_blanks, col_blanks = expand_universe(lines)
    galaxies = get_galaxy_positions(lines)
    return sum_shortest_paths(galaxies, row_blanks, col_blanks, 2)


def part_two(lines: list[str]) -> int:
    row_blanks, col_blanks = expand_universe(lines)
    galaxies = get_galaxy_positions(lines)
    return sum_shortest_paths(galaxies, row_blanks, col_blanks, 1_000_000)


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(part_two(infile.readlines()))
