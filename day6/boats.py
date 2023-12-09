from functools import reduce


def get_distance_traveled(race_time: int, hold_time: int) -> int:
    return (race_time - hold_time) * hold_time


def find_num_winners(race_time: int, record_distance: int) -> int:
    s = 0
    for i in range(race_time + 1):
        s += 1 if get_distance_traveled(race_time, i) > record_distance else 0
    return s


def find_num_winners_fast(race_time: int, record_distance: int) -> int:
    left_break = find_change_point(race_time, record_distance, 0, race_time, True)
    while get_distance_traveled(race_time, left_break) < record_distance:
        left_break += 1
    right_break = find_change_point(race_time, record_distance, 0, race_time, False)
    while get_distance_traveled(race_time, right_break) < record_distance:
        right_break -= 1
    return 1 + right_break - left_break


def find_change_point(
    race_time: int,
    record_distance: int,
    left: int,
    right: int,
    find_start_break: bool = True,
) -> int:
    if left > right:
        return left if find_start_break else right
    if left == right:
        return left
    mid = (left + right) // 2
    mid_is_winner = get_distance_traveled(race_time, mid) > record_distance
    if find_start_break:
        if mid_is_winner:
            return find_change_point(race_time, record_distance, left, mid - 1, True)
        return find_change_point(race_time, record_distance, mid + 1, right, True)
    if mid_is_winner:
        return find_change_point(race_time, record_distance, mid + 1, right, False)
    return find_change_point(race_time, record_distance, left, mid - 1, False)


def get_prod(lines: list[str]):
    times, distances = parse_problem(lines)
    num_winners = list()
    for i in range(len(times)):
        num_winners.append(find_num_winners_fast(times[i], distances[i]))
    return reduce(lambda x, y: x * y, num_winners)


def parse_problem(lines: list[str]):
    time_line, distance_line = lines[0], lines[1]
    times = [int(num) for num in time_line.strip().split()[1:]]
    distances = [int(num) for num in distance_line.strip().split()[1:]]
    return times, distances


def parse_bad_kerning(lines: list[str]):
    time_line, distance_line = lines[0], lines[1]
    times = [num for num in time_line.strip().split()[1:]]
    distances = [num for num in distance_line.strip().split()[1:]]
    time = int("".join(times))
    distance = int("".join(distances))
    return time, distance


def get_big_prod(lines: list[str]):
    time, distance = parse_bad_kerning(lines)
    return find_num_winners_fast(time, distance)


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(get_big_prod(infile.readlines()))
