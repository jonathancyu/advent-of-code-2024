from argparse import ArgumentParser
from copy import deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Counter, Optional
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


def sat(left: int, right: list[int]) -> bool:
    if len(right) == 1:
        return left == right[0]
    current, next = right[:2]
    remaining = right[2:]
    return (
        sat(left, [current * next] + remaining)
        or sat(left, [current + next] + remaining)
        or sat(left, [int(f"{current}{next}")] + remaining)
    )


def part_one(equations: list[Equation]) -> int:
    total = 0
    for equation in equations:
        target = equation.left
        result = sat(equation.left, equation.right)
        if result:
            total += target

    return total


def part_two(equations: list[Equation]) -> int:
    return 0


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    equations: list[Equation] = [Equation.from_line(line) for line in lines]

    print(f"Part one: {part_one(equations)}")

    # print(f"Part two: {part_two(visited, matrix, pos, direction)}")
