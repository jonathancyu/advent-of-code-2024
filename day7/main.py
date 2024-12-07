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


@dataclass
class Equation:
    left: int
    right: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Equation":
        split = line.split(":")
        assert len(split) == 2
        left, right = split
        return Equation(left=int(left), right=[int(x) for x in right.strip().split()])


def sat(left: int, right: list[int], rules: list[Callable[[int, int], int]]) -> bool:
    if len(right) == 1:
        return left == right[0]
    current, next = right[:2]
    remaining = right[2:]
    for rule in rules:
        if sat(left, [rule(current, next)] + remaining, rules):
            return True
    return False


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    equations: list[Equation] = [Equation.from_line(line) for line in lines]

    rules: list[Callable[[int, int], int]] = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: int(f"{x}{y}"),
    ]
    part_one = sum(
        equation.left
        for equation in equations
        if sat(equation.left, equation.right, rules[:2])
    )
    print(f"Part one: {part_one}")

    part_two = sum(
        equation.left
        for equation in equations
        if sat(equation.left, equation.right, rules)
    )
    print(f"Part two: {part_two}")
