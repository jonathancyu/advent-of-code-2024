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


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


@dataclass
class Result:
    points: set[Point]
    paths: set[tuple[Point, ...]]


def print_path(map, paths):
    result = [["."] * len(map[0]) for _ in range(len(map))]
    for path in paths:
        for x, y in path:
            result[x][y] = map[x][y]
    for row in result:
        print("".join([str(v) for v in row]))


def part_one(map: list[list[int]], trailheads: list[Point]) -> int:
    X, Y = len(map), len(map[0])
    # Parse data positions
    total_points = 0
    total_paths = 0
    for start in trailheads:
        result = Result(set(), set())

        def dfs(pos: Point, path: list[Point] | None = None):
            x, y = pos
            if (path is not None and pos in path) or not 0 <= x < X or not 0 <= y < Y:
                return
            height = map[x][y]

            if path is None:
                # First call, don't need to check.
                path = []
            else:
                # Check for height diff
                p_x, p_y = path[-1]
                prev_height = map[p_x][p_y]
                if height != prev_height + 1:
                    return
            path = path + [pos]
            if height == 9:
                result.paths.add(tuple(path))
                result.points.add(pos)

            # Traverse
            for d_x, d_y in directions:
                new_pos = (x + d_x, y + d_y)
                dfs(new_pos, path=path)

        dfs(start)

        print()
        print_path(map, result.paths)
        total_points += len(result.points)
        total_paths += len(result.paths)
        # break

    print(f"Part one: {total_points}")
    print(f"Part two: {total_paths}")
    return total_points


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    map = []
    trailheads = []
    for x, line in enumerate(lines):
        row = []
        for y, c in enumerate(line.strip()):
            if c == "0":
                trailheads.append((x, y))
            row.append(int(c))
        map.append(row)

    print(map)
    print(trailheads)

    part_one(map, trailheads)
