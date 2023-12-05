# for part 1
def get_first_last_dig(s: str) -> tuple[str, str]:
    left, right = 0, len(s) - 1
    found_left, found_right = False, False
    while left <= right and not (found_left and found_right):
        if not found_left:
            if s[left].isdigit():
                found_left = True
            else:
                left += 1
        if not found_right:
            if s[right].isdigit():
                found_right = True
            else:
                right -= 1
    if found_left and found_right:
        return s[left], s[right]
    print(
        f"Value Error get_first_last_dig: {s}, {left}, {right}, {s[left]}, {s[right]}"
    )
    raise ValueError


def get_line_value(pair: tuple[str, str]) -> int:
    try:
        return int("".join(pair))
    except ValueError:
        print(f"ValueError get_line_value: {pair}")
        raise ValueError


# for part 2
def get_line_value(s: str, numbers: dict[str, int], numbers_lengths: set[int]) -> int:
    left, right = 0, len(s) - 1
    left_val, right_val = None, None
    while left < len(s) and right >= 0 and (left_val is None or right_val is None):
        if left_val is None:
            written_num = check_nums(left, s, False, numbers, numbers_lengths)
            if s[left].isdigit():
                left_val = int(s[left])
            elif written_num != -1:
                left_val = written_num
            else:
                left += 1
        if right_val is None:
            written_num = check_nums(right, s, True, numbers, numbers_lengths)
            if s[right].isdigit():
                right_val = int(s[right])
            elif written_num != -1:
                right_val = written_num
            else:
                right -= 1
    if left_val is not None and right_val is not None:
        return (left_val * 10) + right_val
    print(
        f"Value Error get_first_last_dig: {s}, {left}, {right}, {s[left]}, {s[right]}"
    )
    raise ValueError


def check_nums(
    i: int, s: str, forward: bool, numbers: dict[str, int], numbers_lengths: set[int]
) -> int:
    for di in numbers_lengths:
        if forward and i + di > len(s):
            continue
        if not forward and i - di < -1:
            continue
        start = i
        end = i + di
        if not forward:
            start = 1 + i - di
            end = 1 + i
        if s[start:end] in numbers:
            return numbers[s[start:end]]
    # sentinel
    return -1


if __name__ == "__main__":
    s = 0
    with open("input.txt") as infile:
        # part 1
        # line_values_generator = (get_line_value(get_first_last_dig(line)) for line in infile.readlines())

        # part 2
        numbers = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        numbers_lengths = set(map(lambda s: len(s), numbers))
        line_values_generator = (
            get_line_value(line, numbers, numbers_lengths)
            for line in infile.readlines()
        )
        for v in line_values_generator:
            s += v
    print(s)
