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


def print_data(data: list[int | None]):
    print("".join([str(x) if x is not None else "." for x in data]))


def part_one(numbers: list[int]) -> int:
    # Parse data positions
    on_data = True
    data = []
    empty_positions = deque()
    data_positions = deque()
    data_index = 0
    for number in numbers:
        # print(f"{number}: {on_data}")
        if on_data:
            for _ in range(number):
                data_positions.append(len(data))
                data.append(data_index)
            data_index += 1
        else:
            for _ in range(number):
                empty_positions.append(len(data))
                data.append(None)

        on_data = not on_data
    # print(data_positions)
    # print(empty_positions)
    # print_data(data)

    # Re-organize
    while empty_positions and data_positions:
        empty_pos = empty_positions.popleft()
        assert data[empty_pos] is None
        data_pos = data_positions.pop()
        if empty_pos > data_pos:
            break
        data[empty_pos] = data[data_pos]
        data[data_pos] = None
        # print_data(data)

    # Calculate result
    return sum([i * val for i, val in enumerate(data) if val is not None])


def part_two(matrix: list[list[str]]) -> int:
    return 0


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1
    map = [int(x) for x in lines[0].strip()]
    # print(map)

    print(f"Part one: {part_one(map)}")
    # print(f"Part two: {part_two(deepcopy(matrix))}")
