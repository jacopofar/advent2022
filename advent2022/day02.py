# score coming from game outcome
GAME_SCORES = dict(
    AX=3,
    AY=6,
    AZ=0,
    BX=0,
    BY=3,
    BZ=6,
    CX=6,
    CY=0,
    CZ=3,
)

MOVE_SCORE = dict(X=1, Y=2, Z=3)

# for part 2, completely different logic
#
GAME_SCORES2 = dict(
    AX=0 + 3,
    AY=3 + 1,
    AZ=6 + 2,
    BX=0 + 1,
    BY=3 + 2,
    BZ=6 + 3,
    CX=0 + 2,
    CY=3 + 3,
    CZ=6 + 1,
)


def get_input() -> list[str]:
    with open("input/day02.txt") as fr:
        return [l.strip().replace(" ", "") for l in fr.readlines()]


def part_one(problem_input: list[str]) -> int:
    return sum(GAME_SCORES[p] + MOVE_SCORE[p[1]] for p in problem_input)


def part_two(problem_input: list[str]) -> int:
    return sum(GAME_SCORES2[p] for p in problem_input)


if __name__ == "__main__":
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))
