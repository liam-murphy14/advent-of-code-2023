def get_next_val(seq: list[int], forward: bool = True) -> int:
    diffs = seq.copy()
    new_vals = list()
    while not all(map(lambda x: x == 0, diffs)):
        new_vals.append(diffs[-1 if forward else 0])
        diffs = [diffs[i] - diffs[i - 1] for i in range(1, len(diffs))]

    if forward:
        return sum(new_vals)
    return fold_reverse_differences(new_vals)


def fold_reverse_differences(vals: list[int]) -> int:
    s = 0
    for val in vals[::-1]:
        s = val - s
    return s


def parse_problem(lines: list[str]):
    # returns generator
    return (list(map(lambda x: int(x), line.strip().split())) for line in lines)


def part_one(lines: list[str]):
    seqs = parse_problem(lines)
    s = 0
    for seq in seqs:
        s += get_next_val(seq)
    return s


def part_two(lines: list[str]):
    seqs = parse_problem(lines)
    s = 0
    for seq in seqs:
        next_val = get_next_val(seq, forward=False)
        s += next_val
    return s


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(part_two(infile.readlines()))
