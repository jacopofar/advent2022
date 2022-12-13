from ast import literal_eval
from typing import Any, Union

Packet = list[Union[int, "Packet"]]


def check_packet(p: Any) -> Packet:
    """Ensures that the packet is well-formed.

    Also, makes mypy happy.
    """
    assert type(p) == list
    ret: Packet = []
    for elem in p:
        if type(elem) == int:
            ret.append(elem)
        else:
            ret.append(check_packet(elem))
    return ret


def get_input() -> list[tuple[Packet, Packet]]:
    ret = []
    with open("input/day13.txt") as fr:
        couples = fr.read().split("\n\n")
        for cp in couples:
            [p1, p2] = cp.strip().split("\n")
            ret.append((check_packet(literal_eval(p1)), check_packet(literal_eval(p2))))
    return ret


def is_right_order(l: Packet | int, r: Packet | int) -> bool | None:
    """Recursively compares two packets.

    This is done according to the rules of the problem, the code mimics the
    description structure. Notice that sometimes the comparison is
    None and then the problem asks to keep checking.

    In theory this means two packets could be identical and the comparison
    will be None, but the input never presents this case.
    """
    # print(f"Compare {l} vs {r}")
    if type(l) == int and type(r) == int:
        if l < r:
            return True
        if l > r:
            return False
        return None
    elif type(l) == list and type(r) == list:
        for el, er in zip(l, r):
            result = is_right_order(el, er)
            if result is not None:
                return result
        if len(l) < len(r):
            return True
        if len(l) > len(r):
            return False
        return None
    else:
        if type(l) == int:
            l = [l]
        if type(r) == int:
            r = [r]
        return is_right_order(l, r)


def part_one(packets: list[tuple[Packet, Packet]]) -> int:
    tot = 0
    for idx, (p1, p2) in enumerate(packets):
        if is_right_order(p1, p2):
            tot += idx + 1
    return tot


def part_two(packets: list[tuple[Packet, Packet]]) -> int:
    """Part 2 requires to ignore the couples, put all the packets together
    plus two separator packets and order until the consecutive pairs
    are fine.

    Then we need to find the position of the dividers.
    """
    divider1 = [[2]]
    divider2 = [[6]]

    real_packets: list[Packet] = [
        check_packet(divider1),
        check_packet(divider2),
    ]
    for p1, p2 in packets:
        real_packets.append(p1)
        real_packets.append(p2)
    # bubble sort, the easiest one
    idx = 0
    while idx < len(real_packets) - 1:
        if is_right_order(real_packets[idx], real_packets[idx + 1]):
            idx += 1
        else:
            real_packets[idx], real_packets[idx + 1] = (
                real_packets[idx + 1],
                real_packets[idx],
            )
            idx = 0
    i1 = -1
    i2 = -1
    for idx, p in enumerate(real_packets):
        if p == divider1:
            i1 = idx + 1
        if p == divider2:
            i2 = idx + 1
    return i1 * i2


def main() -> None:
    packets = get_input()
    print(part_one(packets))
    print(part_two(packets))


if __name__ == "__main__":
    main()
