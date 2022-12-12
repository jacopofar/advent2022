Coord = tuple[int, int]
Grid = dict[Coord, int]

# deal with it ;)
INFINITY = 999_999_999


def get_input() -> tuple[Grid, Coord, Coord]:
    ret: Grid = dict()
    start: Coord = (0, 0)
    end: Coord = (0, 0)

    with open("input/day12.txt") as fr:
        for ri, row in enumerate(fr):
            for ci, column_char in enumerate(row):
                if column_char == "S":
                    start = (ri, ci)
                    ret[(ri, ci)] = ord("a")
                elif column_char == "E":
                    end = (ri, ci)
                    ret[(ri, ci)] = ord("z")
                else:
                    ret[(ri, ci)] = ord(column_char)
    return ret, start, end


def reachable_cells(
    from_cell: Coord, grid: Grid, backwards: bool = False
) -> list[Coord]:
    """Gets the cells that can be reached from a given one.

    The grid edges and the 'at most 1 higher' logic are applied.

    The parameter backwards swaps the direction of the step.
    """
    current_height = grid[from_cell]
    x, y = from_cell
    result = []
    for c in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if c not in grid:
            continue
        # backwards inverts the logic
        if backwards:
            if current_height <= grid[c] + 1:
                result.append(c)
        else:
            if grid[c] <= current_height + 1:
                result.append(c)
    return result


def find_distances(
    grid: Grid, start: Coord, ends: list[Coord], backwards: bool = False
) -> dict[Coord, int]:
    """Find distances between a start cell and end ones.

    If an end cell is unreachable, the INFINITY value is returned for it.
    It's non actually infinite because of Python int type, but higher than an
    reasonable output.
    """
    # Usual Djikstra
    distances: dict[Coord, int] = {start: 0}
    while True:
        candidates: dict[Coord, int] = dict()
        for cell, distance in distances.items():
            for neighbor in reachable_cells(cell, grid, backwards=backwards):
                if neighbor not in distances:
                    # this min() is in case a neighbor can be reached in two
                    # different ways from the current explored graph
                    candidates[neighbor] = min(
                        distance + 1, candidates.get(neighbor, INFINITY)
                    )
        if len(candidates) == 0:
            return {e: distances.get(e, INFINITY) for e in ends}
        # now we have the list of candidates to expand the explored graph
        # let's find the closest ones (may be more than 1) and add them
        lowest_distance = min(candidates.values())
        for c, d in candidates.items():
            if d == lowest_distance:
                distances[c] = d
        # did we find all the end? stop then
        if all(e in distances for e in ends):
            return {e: distances[e] for e in ends}


def part_one(grid: Grid, start: Coord, end: Coord) -> int:
    return find_distances(grid, start, [end])[end]


def part_two(grid: Grid, _start: Coord, end: Coord) -> int:
    a_positions = [cell for cell, height in grid.items() if height == ord("a")]
    return min(find_distances(grid, end, a_positions, backwards=True).values())


def main() -> None:
    grid, start, end = get_input()
    print(part_one(grid, start, end))
    print(part_two(grid, start, end))


if __name__ == "__main__":
    main()
