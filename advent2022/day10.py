from typing import Generator

SCREEN_HEIGHT = 6
SCREEN_WIDTH = 40


def get_input() -> list[tuple[str, int]]:
    ret = []
    with open("input/day10.txt") as fr:
        for line in fr:
            instruction, _, value = line.strip().partition(" ")
            ret.append((instruction, int(value) if instruction == "addx" else 0))
    return ret


def processor_generator(
    problem_input: list[tuple[str, int]]
) -> Generator[tuple[int, int], None, None]:
    """Yield the cycle counter and register."""
    ic = 0
    x = 1
    for op, value in problem_input:
        if op == "noop":
            ic += 1
            yield (ic, x)
        elif op == "addx":
            ic += 1
            yield (ic, x)
            ic += 1
            yield (ic, x)
            x += value
        else:
            raise ValueError(f"Unknown instruction '{op}'")
    yield (ic, x)


def part_one(problem_input: list[tuple[str, int]]) -> int:
    total_sum = 0
    for ic, x in processor_generator(problem_input):
        if (ic - 20) % 40 == 0:
            total_sum += ic * x
    return total_sum


def part_two(problem_input: list[tuple[str, int]]) -> str:
    screen_content = ""
    for ic, x in processor_generator(problem_input):
        if (ic - 1) % SCREEN_WIDTH == 0 and ic != 0:
            screen_content += "\n"
        if abs(((ic - 1) % SCREEN_WIDTH) - x) <= 1:
            screen_content += "#"
        else:
            screen_content += "."
    return screen_content


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
