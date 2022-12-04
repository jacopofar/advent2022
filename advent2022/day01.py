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


def part_one(problem_input: list[list[int]]) -> int:
    return max(sum(calories) for calories in problem_input)


def part_two(problem_input: list[list[int]]) -> int:
    totals: list[int] = sorted(
        [sum(calories) for calories in problem_input], reverse=True
    )
    return sum(totals[:3])


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
