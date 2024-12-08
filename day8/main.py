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

Point = tuple[int, int]


def part_one(matrix: list[list[str]]) -> int:
    X, Y = len(matrix), len(matrix[0])
    frequency_lookup: dict[str, list[Point]] = defaultdict(list)
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val.isalnum():
                frequency_lookup[val].append((i, j))
    antinodes = set()
    for _, positions in frequency_lookup.items():
        for a, b in product(positions, positions):
            if a == b:
                continue
            a_x, a_y = a
            b_x, b_y = b
            d_x = a_x - b_x
            d_y = a_y - b_y

            x_1 = a_x + d_x
            y_1 = a_y + d_y
            if 0 <= x_1 < X and 0 <= y_1 < Y:
                matrix[x_1][y_1] = "#"
                antinodes.add((x_1, y_1))
            x_2 = b_x - d_x
            y_2 = b_y - d_y
            if 0 <= x_2 < X and 0 <= y_2 < Y:
                matrix[x_2][y_2] = "#"
                antinodes.add((x_2, y_2))
            print("\n".join(["".join(line) for line in matrix]))
            print()
    return len(antinodes)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()

    matrix = []
    for line in lines:
        row = []
        for char in line.strip():
            row.append(char)
        matrix.append(row)

    print(f"Part one: {part_one(matrix)}")
    # print(f"Part two: {part_two}")
