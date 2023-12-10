HAND_RANKS = {
    "five_kind": 7,
    "four_kind": 6,
    "full_house": 5,
    "three_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}

CARD_RANKS = {
    "A": 13,
    "K": 12,
    "Q": 11,
    # "J": 10, # part 1
    "J": 0,  # part 2
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


class CamelHand:
    def __init__(self, hand: str, bid: str):
        self.hand = hand
        # part 1
        # self.hand_type = self.get_hand_type(hand)
        # part 2
        self.hand_type = self.get_jacks_wild_hand_type(hand)
        self.bid = int(bid)

    def __repr__(self):
        return f"{self.hand_type}: {self.hand}"

    def __lt__(self, other):
        if HAND_RANKS[self.hand_type] < HAND_RANKS[other.hand_type]:
            return True
        elif HAND_RANKS[self.hand_type] > HAND_RANKS[other.hand_type]:
            return False
        for i in range(len(self.hand)):
            if CARD_RANKS[self.hand[i]] < CARD_RANKS[other.hand[i]]:
                return True
            elif CARD_RANKS[self.hand[i]] > CARD_RANKS[other.hand[i]]:
                return False
        return False

    def get_hand_type(self, hand: str) -> str:
        freqs = dict()
        for c in hand:
            if c not in freqs:
                freqs[c] = 0
            freqs[c] += 1
        vals = list(freqs.values())
        if max(vals) == 5:
            return "five_kind"
        elif max(vals) == 4:
            return "four_kind"
        elif max(vals) == 3:
            if 2 in vals:
                return "full_house"
            return "three_kind"
        elif max(vals) == 1:
            return "high_card"
        if vals.count(2) == 2:
            return "two_pair"
        return "one_pair"

    def get_jacks_wild_hand_type(self, hand: str) -> str:
        freqs = dict()
        num_jacks = 0
        for c in hand:
            if c == "J":
                num_jacks += 1
                continue
            if c not in freqs:
                freqs[c] = 0
            freqs[c] += 1
        vals = list(freqs.values())
        max_possible = max(vals) + num_jacks if vals else 5
        if max_possible == 5:
            return "five_kind"
        elif max_possible == 4:
            return "four_kind"
        elif max_possible == 3:
            if vals.count(2) == 2 and num_jacks == 1 or 2 in vals and num_jacks == 0:
                return "full_house"
            return "three_kind"
        elif max_possible == 1:
            return "high_card"
        if vals.count(2) == 2:
            return "two_pair"
        return "one_pair"


def parse_problem(lines: list[str]):
    hands = list()
    for line in lines:
        hand, bid = line.split()
        hands.append(CamelHand(hand, bid))
    return hands


def get_total_winnings(lines: list[str]) -> int:
    hands = parse_problem(lines)
    hands.sort()
    return sum([hand.bid * (i + 1) for i, hand in enumerate(hands)])


if __name__ == "__main__":
    with open("input.txt") as infile:
        print(get_total_winnings(infile.readlines()))
