from typing import Generator

MOVES_OFFSETS = dict(
    R=(1, 0),
    U=(0, -1),
    L=(-1, 0),
    D=(0, 1),
)

# one is the head
KNOTS_NUMBER = 10


def get_input() -> list[tuple[str, int]]:
    ret = []
    with open("input/day09.txt") as fr:
        for line in fr:
            direction, _, steps = line.partition(" ")
            ret.append((direction, int(steps)))
    return ret


def head_positions_generator(
    problem_input: list[tuple[str, int]]
) -> Generator[tuple[int, int], None, None]:
    """Yield the head position one by one as x, y coordinates."""
    # here I use the CG orientation of the Y-axis
    hx, hy = 0, 0
    # yield the first position, (0, 0)
    yield hx, hy
    for direction, steps in problem_input:
        # get offset for the given direction
        dx, dy = MOVES_OFFSETS[direction]
        for _ in range(steps):
            # move the head
            hx += dx
            hy += dy
            yield (hx, hy)


def sign(a: int) -> int:
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def tail_direction(hx: int, hy: int, tx: int, ty: int) -> tuple[int, int]:
    """Get the offset of the next move of the tail.

    Based on the problem definition, the movement, if any, is of 1 cell on the
    cardinal direction or diagonal, in order to keep a distance of at most 1
    from the head (the diagonal distance counts as 1).

    It looks like this:

    .DYD.
    D...D
    X.t.X
    D...D
    .DYD.

    Here t is the position of the tail and each square is a possible relative
    position of the head. If the head is in a position marked by ., there's no
    movement needed or possible, X and Y mark a movement on the X or Y axis
    respectively, and D on the diagonal.
    """
    dx, dy = (hx - tx), (hy - ty)
    # close enough, no movement
    if abs(dx) <= 1 and abs(dy) <= 1:
        return (0, 0)
    return (sign(dx), sign(dy))


def part_one(problem_input: list[tuple[str, int]]) -> int:
    # tail coordinates, initially 0, 0
    tx, ty = 0, 0
    tail_positions: set[tuple[int, int]] = set()
    for hx, hy in head_positions_generator(problem_input):
        # record where the tail is for the solution
        tail_positions.add((tx, ty))
        # get the movement the tail has to perform
        tdx, tdy = tail_direction(hx, hy, tx, ty)
        tx += tdx
        ty += tdy

    tail_positions.add((tx, ty))
    return len(tail_positions)


def part_two(problem_input: list[tuple[str, int]]) -> int:
    nodes = [(0, 0) for _ in range(KNOTS_NUMBER)]
    tail_positions: set[tuple[int, int]] = set()
    for hx, hy in head_positions_generator(problem_input):
        # record where the tail is for the solution
        tail_positions.add(nodes[-1])
        # set the first knot to head position
        # the others move with the same logic as before
        nodes[0] = (hx, hy)
        for idx in range(1, KNOTS_NUMBER):
            # this node coordinates
            nx, ny = nodes[idx]
            # it's relative head (the previous node) coordinates
            # note that for node with index 1 this is the head
            rhx, rhy = nodes[idx - 1]
            tdx, tdy = tail_direction(rhx, rhy, nx, ny)
            # update, NOTE that the update will be immediately visible
            # in the next iteration
            nodes[idx] = ((nx + tdx), (ny + tdy))

    tail_positions.add(nodes[-1])
    return len(tail_positions)


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
