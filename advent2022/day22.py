import re
from typing import Callable, Iterable

InputMap = dict[complex, str]
WrapFunction = Callable[[complex, complex, InputMap, complex], tuple[complex, complex]]


def get_input() -> tuple[InputMap, complex, list[str]]:
    ret: InputMap = dict()
    max_columns = 0
    with open("input/day22.txt") as fr:
        for row_idx, line in enumerate(fr):
            if "L" in line or "R" in line:
                return (
                    ret,
                    (1 + max_columns + 1j * (row_idx - 1)),
                    re.split("(R|L)", line),
                )

            max_columns = max(max_columns, len(line))
            for col_idx, c in enumerate(line[:-1]):
                ret[col_idx + 1 + (1 + row_idx) * 1j] = c
    raise ValueError("Could not find the line with instructions")


def get_starting_position(plane: InputMap) -> complex:
    pos = 1
    while True:
        if plane[pos + 1 + 1j] == " ":
            pos += 1
        else:
            return pos + 1 + 1j


def step_forward(
    position: complex,
    direction: complex,
    plane: InputMap,
    size: complex,
    wrap_logic: WrapFunction,
) -> tuple[complex, complex]:
    next_position = position + direction
    next_direction = direction
    # is the next position real? if no ask wrap logic what to do
    if plane.get(next_position, " ") == " ":
        next_position, next_direction = wrap_logic(position, direction, plane, size)

    next_cell = plane[next_position]
    # is it a wall? no movement
    if next_cell == "#":
        return position, direction
    # is it allowed? move
    # NOTE changing direction is part of the movement too
    if next_cell == ".":
        return next_position, next_direction

    raise ValueError(f"something went very wrong...")


def show_map(
    plane: InputMap, size: complex, position: complex, direction: complex
) -> None:
    directions = {
        (1): ">",
        (-1): "<",
        (1j): "V",
        (-1j): "^",
    }
    for row in range(1, int(size.imag) + 3):
        line = ""
        for col in range(1, int(size.real) + 3):
            this_pos = col + 1j * row
            if this_pos == position:
                line += directions[direction]
            else:
                line += plane.get(this_pos, " ")
        print(line)
    import time

    time.sleep(0.5)


def final_score(position: complex, direction: complex) -> int:
    directions_scores = {
        (1): 0,
        (-1): 2,
        (1j): 1,
        (-1j): 3,
    }
    return int(1000 * position.imag + 4 * position.real + directions_scores[direction])


def part_one_wrapping(
    position: complex, direction: complex, plane: InputMap, size: complex
) -> tuple[complex, complex]:
    next_position = position + direction
    # reset the next_position to wrap around
    if direction == 1:
        next_position = 1 + 1j * next_position.imag
    elif direction == -1:
        next_position = size.real + 1j * next_position.imag
    elif direction == 1j:
        next_position = next_position.real + 1j
    elif direction == -1j:
        next_position = next_position.real + 1j * size.imag
    else:
        raise ValueError(f"Impossible direction {direction}")
    # now proceed to find the first real cell
    while plane.get(next_position, " ") == " ":
        next_position += direction
    return next_position, direction


def follow_instructions(
    plane: InputMap, size: complex, instructions: list[str], wrap_logic: WrapFunction
) -> int:
    position, direction = (get_starting_position(plane), 1 + 0j)
    # show_map(plane, size, position, direction)
    for inst in instructions:
        # show_map(plane, size, position, direction)
        # print(inst, position, direction)
        if inst == "L":
            direction *= -1j
        elif inst == "R":
            direction *= 1j
        else:
            for _ in range(int(inst)):
                position, direction = step_forward(
                    position, direction, plane, size, wrap_logic
                )
                # show_map(plane, size, position, direction)
    # print(position, direction)
    return final_score(position, direction)


def part_one(plane: InputMap, size: complex, instructions: list[str]) -> int:
    return follow_instructions(plane, size, instructions, part_one_wrapping)


def axis_in_common(s: Iterable[tuple[int, int, int]]) -> int:
    axis_id = -1
    for idx in (0, 1, 2):
        if sum(v[idx] for v in s) in (0, 4):
            axis_id = idx
            break
    assert axis_id != -1
    return axis_id


def swap_tuple_axis(t: tuple[int, int, int], axis_id: int) -> tuple[int, int, int]:
    new_vertex = list(t)
    new_vertex[axis_id] = 1 if new_vertex[axis_id] == 0 else 0
    return tuple(new_vertex)  # type: ignore


def get_wrapping_points(
    plane: InputMap,
) -> tuple[dict[complex, tuple[int, int, int]], int]:
    # hardcoded, given by the problem to be 50
    # but I prefer to calculate it so it works on the sample or variations
    area = sum(1 if cell != " " else 0 for cell in plane.values())
    square_size = int((area / 6) ** (1 / 2))
    ret: dict[complex, tuple[int, int, int]] = {}
    # now go on squares and search for a non-blank one
    # this extra for cycle is to follow "concave" structures
    # I was too lazy to implement BFS or similar for just 6 squares
    for _ in range(6):
        for r_i in range(6):
            for c_i in range(6):
                side_pos = c_i + r_i * 1j
                # let's name the 4 vertices ABCD, in reading order
                square_A = square_size * side_pos + 1 + 1j
                if plane.get(square_A, " ") == " ":
                    # empty square
                    continue
                # did we explore it already? skip
                if square_A in ret:
                    continue
                square_B = square_A + square_size - 1
                square_C = square_A + 1j * square_size - 1j
                square_D = square_C + square_size - 1
                # if it's the very first we find something, just assign arbitrary coordinates
                if len(ret) == 0:
                    ret[square_A] = (0, 0, 1)
                    ret[square_B] = (1, 0, 1)
                    ret[square_C] = (0, 0, 0)
                    ret[square_D] = (1, 0, 0)
                    continue
                # it's a first, let's try to assign coordinates based on the nearby squares
                for dir in (1, -1, 1j, -1j):
                    # check whether the square in direction dir is known
                    # notice that each 2D cell is in a single 3D face, no face overlapping to handle
                    if (square_A + dir) not in ret and (square_D + dir) not in ret:
                        continue
                    # OK, here the fun begins: we have a nearby known face, want to find the coordinates of this one
                    # first, the two adjacent cells in 2D have the same coordinates, just copy them
                    # also, store the 4 vertices of the adjacent square for the next step
                    near_vertices = set()
                    for sX in (square_A, square_B, square_C, square_D):
                        if (sX + dir) in ret:
                            ret[sX] = ret[sX + dir]
                            near_vertices.add(ret[sX + dir])
                            near_vertices.add(ret[sX + dir * square_size])
                    assert len(near_vertices) == 4
                    # now find the plane of the nearby face.
                    # This is the coordinate identical for 4 vertices, and the one that changes
                    axis_id = axis_in_common(near_vertices)
                    # now, calculate the 2 vertices further away by changing the coordinate with this index
                    for sX in (square_A, square_B, square_C, square_D):
                        if sX in ret:
                            # already known, skip
                            continue
                        if (sX + dir * square_size) in ret:
                            ret[sX] = swap_tuple_axis(
                                ret[sX + dir * square_size], axis_id
                            )
    # each face has its own 4 values
    assert len(ret) == 6 * 4
    return ret, square_size


def part_two(plane: InputMap, size: complex, instructions: list[str]) -> int:
    # first, calculate the vertices and map them to plane positions
    uv_wraps, square_size = get_wrapping_points(plane)
    inverse_wraps: dict[tuple[int, int, int], set[complex]] = {}
    for cell, xyz in uv_wraps.items():
        if xyz in inverse_wraps:
            inverse_wraps[xyz].add(cell)
        else:
            inverse_wraps[xyz] = {cell}

    def part_two_wrapping(
        position: complex,
        direction: complex,
        _plane: InputMap,
        _size: complex,
        square_size: int = square_size,
        uv_wraps: dict[complex, tuple[int, int, int]] = uv_wraps,
        inverse_wraps: dict[tuple[int, int, int], set[complex]] = inverse_wraps,
    ) -> tuple[complex, complex]:
        # print()
        # print(position, direction, uv_wraps)
        # print(inverse_wraps)
        # print()
        # first, I want to find out the corners from which I am "leaving"
        # on the left and right relative to where I'm facing
        leaving_left = position
        while leaving_left not in uv_wraps:
            leaving_left += direction * -1j
        # I want the current offset from the left corner
        offset_left = abs(leaving_left - position)
        # edge case (literally), that was the RIGHT corner
        if (
            offset_left == 0
            and (leaving_left + (direction * -1j) * (square_size - 1)) in uv_wraps
        ):
            leaving_right = leaving_left
            leaving_left = leaving_right + (direction * -1j) * (square_size - 1)
            offset_left = abs(leaving_left - position)
        else:
            leaving_right = position + direction * 1j
            while leaving_right not in uv_wraps:
                leaving_right += direction * 1j
        # these are the positions on the 2D plane, but I want the wrapping
        entering_left = uv_wraps[leaving_left]
        entering_right = uv_wraps[leaving_right]
        # now I want the two corners that I'm leaving behind
        leaving_back_left = uv_wraps[leaving_left - (square_size - 1) * direction]
        leaving_back_right = uv_wraps[leaving_right - (square_size - 1) * direction]
        # now I know the triplets (in 3D space) I'm leaving, so I can calculate the new ones
        idx_to_change = axis_in_common(
            [entering_left, entering_right, leaving_back_left, leaving_back_right]
        )
        # now I can calculate the new 3D coordinates I'm supposed to "see" in front after wrapping
        entering_left_forward = swap_tuple_axis(entering_left, idx_to_change)
        entering_right_forward = swap_tuple_axis(entering_right, idx_to_change)
        # print(
        #     entering_left, entering_right, entering_left_forward, entering_right_forward
        # )
        # now I know the 3D coordinates of the square I'm entering
        # I need to find a cell and a facing rotation for which the 4 squares match
        # only two cells ar eneeded, the opposite corners
        for candidate_left_cell in inverse_wraps[entering_left]:
            for new_direction in (1 + 0j, -1 + 0j, 1j, -1j):
                candidate_left_forward_cell = candidate_left_cell + new_direction * (
                    square_size - 1
                )
                candidate_right_forward_cell = candidate_left_forward_cell + (
                    1j * new_direction * (square_size - 1)
                )
                # print(candidate_left_cell, candidate_left_forward_cell, candidate_right_forward_cell)
                if (
                    candidate_right_forward_cell
                    in inverse_wraps[entering_right_forward]
                ):
                    # print(
                    #     "MATCH",
                    #     new_direction,
                    #     candidate_left_cell,
                    #     candidate_right_forward_cell,
                    # )
                    return (
                        candidate_left_cell + (offset_left * new_direction * 1j),
                        new_direction,
                    )
        raise ValueError('Impossible UV wrapping!')

    return follow_instructions(plane, size, instructions, part_two_wrapping)


def main() -> None:
    plane, size, instructions = get_input()
    print(part_one(plane, size, instructions))
    print(part_two(plane, size, instructions))


if __name__ == "__main__":
    main()
