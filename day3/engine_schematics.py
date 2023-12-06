# part 1
def is_part_number(
    matrix: list[str], num_row: int, num_start: int, num_end: int
) -> bool:
    for j in range(num_start, num_end + 1):
        if is_part_around_cell(matrix, num_row, j):
            return True
    return False


def is_part_around_cell(matrix: list[str], i: int, j: int) -> bool:
    p = i - 1
    q = j - 1
    for dp in range(3):
        for dq in range(3):
            if (
                0 <= p + dp < len(matrix)
                and 0 <= q + dq < len(matrix[p])
                and matrix[p + dp][q + dq] != "."
                and not matrix[p + dp][q + dq].isdigit()
            ):
                return True
    return False


def sum_part_numbers(matrix: list[str]) -> int:
    s, i = 0, 0
    while i < len(matrix):
        j = 0
        while j < len(matrix[i]):
            start_num = j
            while j < len(matrix[i]) and matrix[i][j].isdigit():
                j += 1
            j = j - 1 if j > start_num else j
            if matrix[i][start_num].isdigit() and is_part_number(
                matrix, i, start_num, j
            ):
                s += int(matrix[i][start_num : j + 1])
            j += 1
        i += 1
    return s


# part 2
def find_gears_for_number(
    matrix: list[str], num_row: int, num_start: int, num_end: int
) -> set[tuple[int, int]]:
    gears = set()
    for j in range(num_start, num_end + 1):
        for g in find_gears_around_cell(matrix, num_row, j):
            gears.add(g)
    return gears


def find_gears_around_cell(matrix: list[str], i: int, j: int) -> list[tuple[int, int]]:
    p = i - 1
    q = j - 1
    gears = list()
    for dp in range(3):
        for dq in range(3):
            if (
                0 <= p + dp < len(matrix)
                and 0 <= q + dq < len(matrix[p])
                and matrix[p + dp][q + dq] == "*"
            ):
                gears.append((p + dp, q + dq))
    return gears


def sum_gear_ratios(matrix: list[str]) -> int:
    s, i = 0, 0
    gears_to_num = dict()
    while i < len(matrix):
        j = 0
        while j < len(matrix[i]):
            start_num = j
            while j < len(matrix[i]) and matrix[i][j].isdigit():
                j += 1
            j = j - 1 if j > start_num else j
            if matrix[i][start_num].isdigit():
                for g in find_gears_for_number(matrix, i, start_num, j):
                    if g not in gears_to_num:
                        gears_to_num[g] = list()
                    gears_to_num[g].append(int(matrix[i][start_num : j + 1]))
            j += 1
        i += 1
    for gear in gears_to_num:
        numlist = gears_to_num[gear]
        if len(numlist) != 2:
            continue
        s += numlist[0] * numlist[1]
    return s


if __name__ == "__main__":
    with open("input.txt") as infile:
        lines = list(map(lambda l: l.strip(), infile.readlines()))
        # print(sum_part_numbers(lines))
        print(sum_gear_ratios(lines))
