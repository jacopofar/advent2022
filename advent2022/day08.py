def get_input() -> tuple[list[list[int]], int, int]:
    ret = []
    with open("input/day08.txt") as fr:
        for tree_line in fr:
            ret.append([int(t) for t in tree_line.strip()])
    return ret, len(ret), len(ret[0])


def part_one(problem_input: tuple[list[list[int]], int, int]) -> int:
    grid, mx, my = problem_input
    explorers: list[tuple[int, int, int, int]] = []
    for x in range(mx):
        explorers.append((x, 0, 0, 1))
        explorers.append((x, my - 1, 0, -1))
    for y in range(my):
        explorers.append((0, y, 1, 0))
        explorers.append((mx - 1, y, -1, 0))

    found_trees: set[tuple[int, int]] = set()
    for x, y, ox, oy in explorers:
        max_height = -1
        while True:
            try:
                candidate_tree = grid[x][y]
                # if the index is negative, it's still OOB
                if x < 0 or y < 0:
                    raise IndexError("out out bounds")
                if candidate_tree > max_height:
                    max_height = candidate_tree
                    found_trees.add((x, y))
                    if max_height == 9:
                        # no trees taller than 9, so just stop early
                        break
                x, y = x + ox, y + oy
            except IndexError:
                # we are outside the grid, no more exploration
                break
    return len(found_trees)


def scenic_score(grid: list[list[int]], x: int, y: int) -> int:
    max_height = grid[x][y]
    distances = []
    for ox, oy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        visible_tree_count = 0
        ex, ey = x, y
        while True:
            ex, ey = ex + ox, ey + oy
            try:
                if ex < 0 or ey < 0:
                    raise IndexError("out out bounds")
                if grid[ex][ey] >= max_height:
                    visible_tree_count += 1
                    break
                visible_tree_count += 1

            except IndexError:
                # we are outside the grid, no more exploration
                break
        distances.append(visible_tree_count)
    [a, b, c, d] = distances
    return a * b * c * d


def part_two(problem_input: tuple[list[list[int]], int, int]) -> int:
    grid, mx, my = problem_input
    return max(
        scenic_score(grid, x, y) for x in range(1, mx - 1) for y in range(1, my - 1)
    )


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
