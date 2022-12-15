from dataclasses import dataclass
import re


@dataclass(frozen=True, eq=True)
class MultiRange:
    """Describe multiple non-overlapping ranges.

    This allows us to define a list of ranges, like:
        2-10, 4-22, 29-40
    and merge them to get ranges such that they remain ordered and not
    overlapping and each value that was in one of them remains in the result.
    The MultiRange is isomorphic with the set of numbers N such that there's a tuple
    (A, B) such that  A <= N <= B.

    A for cycle could have done the same for part 1, part 2 did require a
    completely different thing -_-
    """
    positions: tuple[tuple[int, int], ...]

    def __add__(self: "MultiRange", other: "MultiRange") -> "MultiRange":
        """Merges two MultiRanges.

        A MultiRange represents an ordered list of non-overlapping ranges.
        Ranges are INCLUSIVE, so (3, 7) means 3, 4, 5, 6, 7.
        """
        if self.positions == ():
            return MultiRange(other.positions)
        if other.positions == ():
            return MultiRange(self.positions)

        union_positions: tuple[tuple[int, int], ...] = tuple()
        all_sub_ranges = sorted(self.positions + other.positions, key=lambda r: r[0])
        # this is the interval we are going to add, we keep extending it until
        # we find a gap, then it's put in the new range and reset to the next position
        current_start, current_end = all_sub_ranges[0]
        for candidate_start, candidate_end in all_sub_ranges:
            # disjoint add current the results and set it to the new segment
            if current_end < candidate_start:
                union_positions = union_positions + ((current_start, current_end),)
                current_start, current_end = candidate_start, candidate_end
            # overlapping, extend the current interval
            else:
                current_end = max(candidate_end, current_end)
        # add the pending one, if any
        if len(union_positions) == 0 or union_positions[-1][1] != candidate_end:
            union_positions = union_positions + ((current_start, current_end),)
        return MultiRange(union_positions)

    def get_size(self) -> int:
        return sum(1 + pe - ps for ps, pe in self.positions)


@dataclass(frozen=True, eq=True)
class Sensor:
    sensor_x: int
    sensor_y: int
    beacon_x: int
    beacon_y: int

    def distance(self, x: int, y: int) -> int:
        return abs(self.sensor_x - x) + abs(self.sensor_y - y)

    def my_free_range(self) -> int:
        """Distance from this sensor and its nearest beacon.
        No other beacon can be within this distance
        """
        return self.distance(self.beacon_x, self.beacon_y)

    def range_of_covered_positions_at_y(self, y: int) -> MultiRange:
        """Get a MultiRange covering the free positions at the given height.
        NOTE: the beacon for this sensor itself is excluded!
        """
        max_variation = self.my_free_range() - self.distance(self.sensor_x, y)
        if max_variation < 0:
            # no empty positions, too far away
            return MultiRange(())
        else:
            start = self.sensor_x - max_variation
            end = self.sensor_x + max_variation
            if self.beacon_y == y:
                # edge case, this is the line with the beacon
                if self.sensor_x - max_variation == self.beacon_x:
                    return MultiRange(
                        (
                            (
                                1 + start,
                                end,
                            ),
                        )
                    )
                else:
                    return MultiRange(
                        (
                            (
                                start,
                                end - 1,
                            ),
                        )
                    )
            else:
                return MultiRange(
                    ((self.sensor_x - max_variation, self.sensor_x + max_variation),)
                )


def get_input() -> list[Sensor]:
    pattern = re.compile(
        r"Sensor at x=([^\,]+)\, y=([^\,]+): closest beacon is at x=([^\,]+), y=([^\,]+)"
    )
    ret = []
    with open("input/day15.txt") as fr:
        for line in fr:
            matches = pattern.match(line.strip())
            assert matches is not None
            sx, sy, bx, by = (int(m) for m in matches.group(1, 2, 3, 4))
            sensor = Sensor(sx, sy, bx, by)
            ret.append(sensor)
    return ret


def part_one(sensors: list[Sensor]) -> int:
    ranges: MultiRange = MultiRange(())
    for s in sensors:
        ranges += s.range_of_covered_positions_at_y(2000000)
    return ranges.get_size()


def part_two(sensors: list[Sensor]) -> int:
    return 42


def main() -> None:
    sensors = get_input()
    print(part_one(sensors))
    print(part_two(sensors))


if __name__ == "__main__":
    main()
