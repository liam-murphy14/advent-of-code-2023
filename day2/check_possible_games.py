# part 1
def sum_game_list(r: int, g: int, b: int, lines: list[str]) -> int:
    id_draws_list = list(map(parse_game, lines))
    s = 0
    for game_id, game_draws in id_draws_list:
        if is_game_possible(r, g, b, game_draws):
            s += game_id
    return s


def is_game_possible(r: int, g: int, b: int, draws: list[tuple[int, int, int]]) -> bool:
    # draws: (r, g, b)
    for drawn_r, drawn_g, drawn_b in draws:
        if drawn_r > r or drawn_g > g or drawn_b > b:
            return False
    return True


# part 2
def get_min_possible_game(draws: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    # draws: (r, g, b)
    draw = [0, 0, 0]
    for drawn_r, drawn_g, drawn_b in draws:
        draw[0] = max(draw[0], drawn_r)
        draw[1] = max(draw[1], drawn_g)
        draw[2] = max(draw[2], drawn_b)
    return tuple(draw)


def sum_game_min_powers(lines: list[str]) -> int:
    id_draws_list = list(map(parse_game, lines))
    s = 0
    for game_id, game_draws in id_draws_list:
        r, g, b = get_min_possible_game(game_draws)
        s += r * g * b
    return s


# helpers
def parse_game(s: str) -> tuple[int, list[tuple[int, int, int]]]:
    game_tag, draws_list = s.split(": ")
    _, game_id = game_tag.split()
    draw_strings = draws_list.split("; ")
    draws = list(map(parse_draw, draw_strings))
    return int(game_id), draws


def parse_draw(s: str) -> tuple[int, int, int]:
    draw = [0, 0, 0]
    color_draws = s.split(", ")
    for color_draw in color_draws:
        num_string, color = color_draw.split()
        if color == "red":
            draw[0] = int(num_string)
        if color == "green":
            draw[1] = int(num_string)
        if color == "blue":
            draw[2] = int(num_string)
    return tuple(draw)


if __name__ == "__main__":
    with open("input.txt") as infile:
        # print(sum_game_list(12, 13, 14, infile.readlines()))
        print(sum_game_min_powers(infile.readlines()))
