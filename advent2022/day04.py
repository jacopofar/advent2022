import re

NON_DIGIT = re.compile(r"[^0-9]")


def get_input() -> list[tuple[int, int, int, int]]:
    ret = []
    with open("input/day04.txt") as fr:
        for line in fr:
            [a, b, c, d, _] = NON_DIGIT.split(line)
            ret.append(
                (
                    int(a),
                    int(b),
                    int(c),
                    int(d),
                )
            )
        return ret


def part_one(problem_input: list[tuple[int, int, int, int]]) -> int:
    return sum(
        1 for a, b, c, d in problem_input if (a <= c and b >= d) or (c <= a and d >= b)
    )


def part_two(problem_input: list[tuple[int, int, int, int]]) -> int:
    return sum(1 for a, b, c, d in problem_input if min((b, d)) >= max((a, c)))


if __name__ == "__main__":
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))
