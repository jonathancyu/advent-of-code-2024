from argparse import ArgumentParser
from copy import copy, deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Callable, Counter, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm
import math
import functools

Point = tuple[int, int]


def split_rock(x):
    str_x = str(x)
    size = len(str(x))
    half = int(size / 2)
    return [int(str_x[:half]), int(str_x[half:])]


rules: list[tuple[str, Callable[[int], bool], Callable[[int], list[int]]]] = [
    ("0->1", lambda x: x == 0, lambda _: [1]),
    ("split", lambda x: len(str(x)) % 2 == 0, split_rock),
    ("2024", lambda x: True, lambda x: [x * 2024]),
]


def part_one(line: list[int], steps: int) -> int:
    for depth in tqdm(range(steps)):
        new_line = []
        while line:
            x = line.pop()
            for _, predicate, rule in rules:
                if not predicate(x):
                    continue
                new_line.extend(rule(x))
                break
        #     print(f"{depth}, {x} -> {new_line}")
        # print(new_line)
        line = new_line
    return len(line)


@functools.cache
def dfs(val: int, height: int) -> int:
    if height == 0:
        return 1
    # print(f"{depth}, {val}")
    expanded = None
    for name, predicate, rule in rules:
        if not predicate(val):
            continue
        # print(f"{val} -> {name}")
        expanded = rule(val)
        break
    assert expanded is not None
    total = 0
    for x in expanded:
        result = dfs(x, height - 1)
        total += result
    return total


def part_two(line: list[int], steps: int) -> int:
    return sum([dfs(x, steps) for x in line])


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    line = [int(c) for c in lines[0].strip().split()]
    print(f"part_one: {part_one(copy(line), 25)}")
    print(f"part_two: {part_two(copy(line), 75)}")
