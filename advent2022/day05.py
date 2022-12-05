from copy import deepcopy


def get_input() -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    stacks: list[list[str]] = [[] for _ in range(9)]
    moves = []
    in_stack_description = True
    with open("input/day05.txt") as fr:
        for line in fr:
            if in_stack_description:
                if line[1] == "1":
                    # this line was the label of the crates, switch to moves parsing
                    in_stack_description = False
                else:
                    for idx in range(1, len(line), 4):
                        if line[idx] != " ":
                            stacks[(idx - 1) // 4].insert(0, line[idx])
            else:
                if line == "\n":
                    continue
                [_, num_moves, _, from_i, _, to_i] = line.split(" ")
                moves.append((int(num_moves), int(from_i), int(to_i)))
    return stacks, moves


def perform_move(
    state: list[list[str]], num_moves: int, from_i: int, to_i: int
) -> None:
    for _ in range(num_moves):
        state[to_i].append(state[from_i].pop())


def perform_move_on_block(
    state: list[list[str]], num_moves: int, from_i: int, to_i: int
) -> None:
    for i in range(num_moves):
        state[to_i].append(state[from_i].pop(-num_moves + i))


def part_one(problem_input: tuple[list[list[str]], list[tuple[int, int, int]]]) -> str:
    state = deepcopy(problem_input[0])
    for num_moves, from_i, to_i in problem_input[1]:
        perform_move(state, num_moves, from_i - 1, to_i - 1)
    return "".join([s[-1] for s in state])


def part_two(problem_input: tuple[list[list[str]], list[tuple[int, int, int]]]) -> str:
    state = deepcopy(problem_input[0])
    for num_moves, from_i, to_i in problem_input[1]:
        perform_move_on_block(state, num_moves, from_i - 1, to_i - 1)
    return "".join([s[-1] for s in state])


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
