from copy import deepcopy

Coord = tuple[int, int]
SAND_POUR_POINT = (500, 0)


def sign(a: int) -> int:
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def enumerate_coords(previous_x: int, previous_y: int, x: int, y: int) -> set[Coord]:
    ret: set[Coord] = set()
    sx = sign(x - previous_x)
    sy = sign(y - previous_y)
    cx, cy = previous_x, previous_y
    while cx != x or cy != y:
        ret.add((cx, cy))
        cx += sx
        cy += sy
    ret.add((cx, cy))
    return ret


def get_input() -> set[Coord]:
    with open("input/day14.txt") as fr:
        coords: set[Coord] = set()
        for multiline in fr.read().strip().split("\n"):
            previous_x, previous_y = None, None
            for cpair in multiline.split("->"):
                a, _, b = cpair.partition(",")
                x, y = int(a), int(b)
                if previous_x is not None:
                    coords |= enumerate_coords(previous_x, previous_y, x, y)
                previous_x, previous_y = x, y
    return coords


def get_bbox(rocks: set[Coord]) -> tuple[int, int, int, int]:
    min_x = min(x for x, _ in rocks)
    max_x = max(x for x, _ in rocks)
    min_y = min(y for _, y in rocks)
    max_y = max(y for _, y in rocks)
    return (min_x, max_x, min_y, max_y)


def show_state(rocks: set[Coord], sand: set[Coord]) -> None:
    min_x, max_x, min_y, max_y = get_bbox(rocks)
    for y in range(min_y - 1, max_y + 1):
        line = ""
        for x in range(min_x - 1, max_x + 1):
            if (x, y) in rocks:
                line += "#"
            elif (x, y) in sand:
                line += "o"
            else:
                line += "."
        print(line)


def final_sand_grain_position(
    initial_pos: Coord, abyss_limit: int, rocks: set[Coord], sand: set[Coord]
) -> Coord:
    x, y = initial_pos
    while y < abyss_limit:
        for candidate in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
            if candidate not in rocks and candidate not in sand:
                x, y = candidate
                break
        else:
            return x, y
    raise IndexError("welcome to the abyss 🕳️")


def part_one(rocks: set[Coord]) -> int:
    sand: set[Coord] = set()
    # lower than this is the abyss, doesn't change so calculate it once
    # and reuse it
    abyss_limit = get_bbox(rocks)[3]
    while True:
        try:
            c = final_sand_grain_position(SAND_POUR_POINT, abyss_limit, rocks, sand)
        except IndexError:
            show_state(rocks, sand)
            return len(sand)

        sand.add(c)


def part_two(rocks: set[Coord]) -> int:
    _, max_x, _, rock_bottom = get_bbox(rocks)
    rocks_with_bottom = deepcopy(rocks)
    abyss_limit = get_bbox(rocks)[3] + 2
    # use rock bottom as a margin for the bottom because the sand accumulates
    # following a triangle so in worst case will reach that point before
    # occluding the pour point
    for x in range(0, max_x + rock_bottom * 2):
        rocks_with_bottom.add((x - rock_bottom, abyss_limit))
    sand: set[Coord] = set()
    while SAND_POUR_POINT not in sand:
        c = final_sand_grain_position(
            SAND_POUR_POINT, abyss_limit, rocks_with_bottom, sand
        )
        sand.add(c)
    show_state(rocks, sand)
    return len(sand)


def main() -> None:
    rocks = get_input()
    print(part_one(rocks))
    print(part_two(rocks))


if __name__ == "__main__":
    main()
