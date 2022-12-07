from dataclasses import dataclass
import re
from typing import Generator, Optional


@dataclass
class Directory:
    files: dict[str, int]
    subdirectories: dict[str, "Directory"]
    parent: Optional["Directory"]

    def print_tree(self, prefix: str = "") -> str:
        """Return a human representation of the filesystem content."""
        ret = ""
        for fname, fsize in self.files.items():
            ret += f"{prefix}/{fname} (file, size={fsize})\n"
        for dname, dir_obj in self.subdirectories.items():
            ret += f"{prefix}/{dname} (dir)\n"
            dir_description = dir_obj.print_tree(prefix=f"{prefix}/{dname}")
            ret += dir_description
        return ret


def folder_size(d: Directory) -> int:
    """Calculate the total size of a folder, recursively."""
    return sum(d.files.values()) + sum(
        folder_size(sd) for sd in d.subdirectories.values()
    )


def walk_dirs(
    d: Directory, prefix: Optional[list[str]] = None
) -> Generator[tuple[list[str], Directory], None, None]:
    """Explore the tree, generate paths and directory objects"""
    if prefix is None:
        prefix = []
    yield prefix, d
    for dirname, sd in d.subdirectories.items():
        for path, dc in walk_dirs(sd):
            yield prefix + [dirname] + path, dc


def get_input() -> list[str]:
    with open("input/day07.txt") as fr:
        return [line.strip() for line in fr.readlines()]


def reconstruct_filesystem(problem_input: list[str]) -> Directory:
    """Parse the input into a tree."""
    root = Directory(dict(), dict(), None)
    root.parent = root
    wrkdir: Directory = root
    for line in problem_input:
        if line.startswith("$"):
            if line == "$ cd /":
                wrkdir = root
            elif line == "$ ls":
                # is not changing any state
                pass
            elif line == "$ cd ..":
                assert wrkdir.parent is not None
                wrkdir = wrkdir.parent
            elif line.startswith("$ cd"):
                folder_name = line.split(" ")[-1]
                if folder_name in wrkdir.subdirectories:
                    wrkdir = wrkdir.subdirectories[folder_name]
                else:
                    wrkdir.subdirectories[folder_name] = Directory(
                        dict(), dict(), wrkdir
                    )
            else:
                raise ValueError(f"Cannot parse $ command {line}")
        elif line.startswith("dir "):
            folder_name = line.split(" ")[-1]
            if folder_name not in wrkdir.subdirectories:
                wrkdir.subdirectories[folder_name] = Directory(dict(), dict(), wrkdir)
        elif re.match(r"\d+", line) is not None:
            fsize, _, fname = line.partition(" ")
            wrkdir.files[fname] = int(fsize)
        else:
            raise ValueError(f"Cannot parse command {line}")
    return root


def part_one(problem_input: list[str]) -> int:
    fs = reconstruct_filesystem(problem_input)
    total = 0
    for _p, dc in walk_dirs(fs):
        if folder_size(dc) < 100_000:
            total += folder_size(dc)
    return total


def part_two(problem_input: list[str]) -> int:
    fs = reconstruct_filesystem(problem_input)
    total_content: list[tuple[list[str], int]] = []
    UPDATE_SIZE = 30000000
    DISK_SIZE = 70000000
    free_space = -1
    for p, dc in walk_dirs(fs):
        dsize = folder_size(dc)
        if len(p) == 0:
            free_space = DISK_SIZE - dsize
        total_content.append((p, dsize))
    enough_to_delete = []
    for p, dsize in total_content:
        if free_space + dsize >= UPDATE_SIZE:
            enough_to_delete.append((p, dsize))
    enough_to_delete = sorted(enough_to_delete, key=lambda t: t[1])
    return enough_to_delete[0][1]


def main() -> None:
    problem_input = get_input()
    print(part_one(problem_input))
    print(part_two(problem_input))


if __name__ == "__main__":
    main()
