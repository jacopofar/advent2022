from dataclasses import dataclass
from copy import deepcopy
import logging
import math

logging.basicConfig(level=logging.INFO)


@dataclass
class Monkey:
    op: str
    argument_val: int
    argument_is_item: bool
    divisor: int
    target_if_divisible: int
    target_if_not_divisible: int

    def perform_monkey_business(
        self, own_items: list[int], lcm: int, worry_level_decrease_factor: int
    ) -> dict[int, list[int]]:
        """Simulate the monkey activities in a turn, return the thrown items.

        The rules are in the (long) exercise description, not copied here to
        keep it short.

        In short, the monkey consumes the items, applies some rules to
        change them and then throw each one (with a changed value) to a
        specific monkey.

        lcm is the LCM between the divisors of all the monkeys.

        This is necessary for part 2 because the numbers get HUGE. Part 1
        is fine without any trick.

        So, the trick is to notice that all we care about is the divisibility
        for a few numbers, the divisors of all the monkeys.
        This means that we don't need to know the actual worry level but just
        the fact it is or not divisible by some value D.
        For a given value D, the number X and X + kD are both divisible or not,
        for an integer k (positive here, everything is positive).
        The LCM between all divisors allows us to keep only the modulo of a
        worry level which is all w eneed to do all divisibility checks, not the
        value itself.

        I got this idea from a friend, my initial approach was to keep a list
        of factors and prune it when needed, but this is much simpler.

        You can imagine the numbers in a ring, and divisibility checks their
        position in the ring. The modulo calculates the number as a position
        of the ring ignoring multiple rounds. This works only if the ring
        length is a multiple of each possible divisor (otherwise the modulo
        will have an effect on divisibility), and LCM does that.
        """
        result: dict[int, list[int]] = dict()
        for worry_level in own_items:
            # argument can be either 'old' or an int
            if self.argument_is_item:
                arg = worry_level
            else:
                arg = self.argument_val
            if self.op == "*":
                worry_level *= arg
            elif self.op == "+":
                worry_level += arg
            else:
                raise ValueError(f"Cannot process operator '{self.op}'")
            worry_level = worry_level // worry_level_decrease_factor

            worry_level = worry_level % lcm
            if worry_level % self.divisor == 0:
                if self.target_if_divisible not in result:
                    result[self.target_if_divisible] = []
                result[self.target_if_divisible].append(worry_level)
            else:
                if self.target_if_not_divisible not in result:
                    result[self.target_if_not_divisible] = []
                result[self.target_if_not_divisible].append(worry_level)
        return result


def get_input() -> tuple[list[list[int]], list[Monkey]]:
    items: list[list[int]] = []
    monkeys: list[Monkey] = []

    with open("input/day11.txt") as fr:
        for monkey_description in fr.read().split("\n\n"):
            lines = monkey_description.splitlines()
            # line 0: 'Monkey X:'
            assert "Monkey" in lines[0]
            # check that they are in order (they are)
            monkey_id: int = int(lines[0].partition(" ")[2][:-1])
            assert monkey_id == len(monkeys)
            # line 1: '  Starting items: X, Y, Z'
            assert "Starting items:" in lines[1]
            items.append(
                [int(i) for i in lines[1].partition("Starting items:")[2].split(",")]
            )
            # line 2: '  Operation: new = old X Y' where X is an operator and Y a number or 'old'
            [op, argument] = lines[2].partition("new = old ")[2].split(" ")
            # line 3: 'divisible by X' where X is a number
            divisor = int(lines[3].split(" ")[-1])
            # line 4 and 5, true and false with a target index at the bottom
            assert "If true: throw to monkey" in lines[4]
            target_if_divisible = int(lines[4].split(" ")[-1])
            assert "If false: throw to monkey" in lines[5]
            target_if_not_divisible = int(lines[5].split(" ")[-1])

            monkeys.append(
                Monkey(
                    op,
                    0 if argument == "old" else int(argument),
                    argument == "old",
                    divisor,
                    target_if_divisible,
                    target_if_not_divisible,
                )
            )
    return items, monkeys


def simulate_rounds(
    items: list[list[int]],
    monkeys: list[Monkey],
    rounds: int,
    worry_level_decrease_factor: int = 3,
) -> dict[int, int]:
    items = deepcopy(items)
    inspected_items_count = {i: 0 for i in range(len(monkeys))}
    lcm = math.lcm(*[m.divisor for m in monkeys])
    for round_i in range(rounds):
        for m_idx, m in enumerate(monkeys):
            inspected_items_count[m_idx] += len(items[m_idx])
            thrown_items = m.perform_monkey_business(
                items[m_idx],
                lcm,
                worry_level_decrease_factor,
            )
            # the monkey throws away all the objects
            items[m_idx] = []

            for m_target, t_items in thrown_items.items():
                items[m_target] += t_items
        logging.debug(
            f"After round {round_i + 1}, the monkeys are holding items with these worry levels:"
        )
        for m_i, m_items in enumerate(items):
            logging.debug(f"Monkey {m_i}: {m_items}")
    return inspected_items_count


def part_one(items: list[list[int]], monkeys: list[Monkey]) -> int:
    inspected_items_count = simulate_rounds(items, monkeys, 20)
    most_inspected = sorted(inspected_items_count.values())
    return most_inspected[-1] * most_inspected[-2]


def part_two(items: list[list[int]], monkeys: list[Monkey]) -> int:
    inspected_items_count = simulate_rounds(items, monkeys, 10_000, 1)
    most_inspected = sorted(inspected_items_count.values())
    return most_inspected[-1] * most_inspected[-2]


def main() -> None:
    items, monkeys = get_input()
    print(part_one(items, monkeys))
    print(part_two(items, monkeys))


if __name__ == "__main__":
    main()
