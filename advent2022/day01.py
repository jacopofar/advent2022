def get_input() -> list[list[int]]:
    res = []
    with open("input/day01.txt") as fr:
        partial: list[int] = []
        for line in fr:
            if line == "\n":
                res.append(partial)
                partial = []
            else:
                partial.append(int(line.strip()))
        res.append(partial)
    return res


def part1(problem_input: list[list[int]]) -> int:
    return max(sum(calories) for calories in problem_input)


def part2(problem_input: list[list[int]]) -> int:
    totals: list[int] = sorted(
        [sum(calories) for calories in problem_input], reverse=True
    )
    return sum(totals[:3])


if __name__ == "__main__":
    problem_input = get_input()
    print(part1(problem_input))
    print(part2(problem_input))
