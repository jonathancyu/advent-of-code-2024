from argparse import ArgumentParser
from copy import deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Callable, Counter, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm
import math

Point = tuple[int, int]


def split_rock(x):
    str_x = str(x)
    size = len(str(x))
    half = int(size / 2)
    return [int(str_x[:half]), int(str_x[half:])]


rules: list[tuple[Callable[[int], bool], Callable[[int], int | list[int]]]] = [
    (lambda x: x == 0, lambda _: 1),
    (lambda x: len(str(x)) % 2 == 0, split_rock),
    (lambda x: True, lambda x: x * 2024),
]


def part_one(line: list[int], steps: int) -> int:
    for _ in tqdm(range(steps)):
        new_line = []
        while line:
            x = line.pop()
            for predicate, rule in rules:
                if not predicate(x):
                    continue
                result = rule(x)
                if isinstance(result, int):
                    new_line.append(result)
                else:
                    new_line.extend(result)
                break
        line = new_line
    return len(line)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    line = [int(c) for c in lines[0].strip().split()]
    print(part_one(line, 75))
