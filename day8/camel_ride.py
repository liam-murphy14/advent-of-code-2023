from functools import reduce


def parse_problem(lines: list[str]) -> tuple[str, dict[str, dict[str, str]]]:
    lr_string = lines[0].strip()
    nodes = dict()
    for line in lines[2:]:
        node, next_nodes = [s.strip() for s in line.split("=")]
        left_node, right_node = next_nodes[1:-1].split(", ")
        nodes[node] = {"L": left_node, "R": right_node}
    return lr_string, nodes


def find_num_steps(
    lr_string: str,
    nodes: dict[str, dict[str, str]],
    start_node: str | None = None,
    end_node: str | None = None,
) -> int:
    steps = 0
    current_node = "AAA" if start_node is None else start_node
    while_condition = (
        current_node != end_node if end_node is not None else current_node[-1] != "Z"
    )
    while while_condition:
        if current_node not in nodes:
            raise ValueError
        current_node = nodes[current_node][lr_string[steps % len(lr_string)]]
        steps += 1
        while_condition = (
            current_node != end_node
            if end_node is not None
            else current_node[-1] != "Z"
        )
    return steps


def get_lcm(x: int, y: int) -> int:
    return (x * y) // get_gcd(x, y)


def get_gcd(x: int, y: int) -> int:
    while y != 0:
        temp = y
        y = x % y
        x = temp
    return x


def part_one(lines: list[str]) -> int:
    lr_string, nodes = parse_problem(lines)
    return find_num_steps(lr_string, nodes, "AAA", "ZZZ")


def part_two(lines: list[str]) -> int:
    lr_string, nodes = parse_problem(lines)
    min_cycle_lengths = list()
    for node in nodes:
        if node[-1] != "A":
            continue
        min_cycle_lengths.append(find_num_steps(lr_string, nodes, node))
    return reduce(get_lcm, min_cycle_lengths)


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(part_two(infile.readlines()))
