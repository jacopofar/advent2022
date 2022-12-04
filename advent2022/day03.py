def get_input() -> list[str]:
    with open("input/day03.txt") as fr:
        return [l.strip().replace(" ", "") for l in fr.readlines()]


def item_value(l: str) -> int:
    # Lowercase item types a through z have priorities 1 through 26.
    # Uppercase item types A through Z have priorities 27 through 52.
    if l.islower():
        return ord(l) - ord("a") + 1
    else:
        return ord(l) - ord("A") + 27


def part_one(problem_input: list[str]) -> int:
    ret: int = 0
    for rucksack in problem_input:
        num = len(rucksack) // 2
        common = set(rucksack[:num]) & set(rucksack[num:])
        assert len(common) == 1
        letter = list(common)[0]
        ret += item_value(letter)
    return ret


def part_two(problem_input: list[str]) -> int:
    ret: int = 0
    for idx in range(0, len(problem_input), 3):
        common = (
            set(problem_input[idx])
            & set(problem_input[idx + 1])
            & set(problem_input[idx + 2])
        )
        assert len(common) == 1
        letter = list(common)[0]
        ret += item_value(letter)
    return ret


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
