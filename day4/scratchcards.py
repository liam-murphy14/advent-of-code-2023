def parse_card_num_and_cols(s: str) -> tuple[str, list[str], list[str]]:
    card_tag, num_cols = s.strip().split(":")
    _, card_id = card_tag.strip().split()
    winners_col, plays_col = num_cols.strip().split("|")
    winners_list = winners_col.strip().split()
    plays_list = plays_col.strip().split()
    return card_id, winners_list, plays_list


def get_winning_numbers_list(
    winners_list: list[str], plays_list: list[str]
) -> list[str]:
    winners_set = set(winners_list)
    winning_numbers_list = list()
    for num in plays_list:
        if num in winners_set:
            winning_numbers_list.append(num)
    return winning_numbers_list


# part 1
def get_points(winning_numbers_list: list[str]) -> int:
    if not winning_numbers_list:
        return 0
    return 2 ** (len(winning_numbers_list) - 1)


def sum_points(lines: list[str]) -> int:
    s = 0
    for line in lines:
        card_id, winners_list, plays_list = parse_card_num_and_cols(line)
        winning_numbers = get_winning_numbers_list(winners_list, plays_list)
        s += get_points(winning_numbers)
    return s


# part 2
def sum_scratch_cards(lines: list[str]) -> int:
    card_instances = dict()
    for line in lines:
        card_id, winners_list, plays_list = parse_card_num_and_cols(line)
        card_id = int(card_id)  # for easier selection
        if card_id not in card_instances:
            card_instances[card_id] = 1
        winning_numbers = get_winning_numbers_list(winners_list, plays_list)
        for i in range(1, len(winning_numbers) + 1):
            card_id_to_copy = card_id + i
            if card_id_to_copy not in card_instances:
                card_instances[card_id_to_copy] = 1
            card_instances[card_id_to_copy] += card_instances[card_id]
    return sum(card_instances.values())


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(sum_scratch_cards(infile.readlines()))
