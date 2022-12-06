from copy import deepcopy


def get_input() -> str:
    with open("input/day06.txt") as fr:
        return fr.read()


def find_first_non_repeated_window(text: str, window_size: int) -> int:
    """Finds the position of the first substring of distinct chaacters.

    It's the 1-based index of the first character that was preceded by
    window_size characters that were all different.

    If not found, raises ValueError
    """
    for i in range(window_size - 1, len(text)):
        if len(set(text[i - window_size : i])) == window_size:
            return i
    raise ValueError(f"Could not find a window of {window_size} distinct characters")


def part_one(problem_input: str) -> int:
    return find_first_non_repeated_window(problem_input, 4)


def part_two(problem_input: str) -> int:
    return find_first_non_repeated_window(problem_input, 14)


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
