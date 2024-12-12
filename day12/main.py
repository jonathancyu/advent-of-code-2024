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


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def print_path(map, region):
    result = [["."] * len(map[0]) for _ in range(len(map))]
    for x, y in region:
        result[x][y] = map[x][y]
    for row in result:
        print("".join([str(v) for v in row]))


def part_one(map: list[list[str]]) -> int:
    X, Y = len(map), len(map[0])
    regions = []
    current_region: set[Point] = set()
    visited: set[Point] = set()

    def dfs(point, plant: str):
        x, y = point
        if point in visited or not 0 <= x < X or not 0 <= y < Y or map[x][y] != plant:
            return
        print(point, plant)

        visited.add(point)
        current_region.add(point)
        for d_x, d_y in directions:
            dfs((x + d_x, y + d_y), plant)

    for i, row in enumerate(map):
        for j, val in enumerate(row):
            current_region = set()
            dfs((i, j), val)
            print(current_region)
            if len(current_region) > 0:
                regions.append(current_region)
    for region in regions:
        print()
        print_path(map, region)
    return 0


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    map = []
    for line in lines:
        map.append([c for c in line.strip()])
    print(part_one(map))
