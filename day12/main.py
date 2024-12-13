from argparse import ArgumentParser
import json
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

Vector = tuple[int, int]


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def to_lateral(direction):
    x, y = direction
    return [(-y, x), (y, -x)]


@dataclass
class Side:
    inside: list[Vector]
    direction: Vector


@dataclass
class Region:
    plant: str
    points: set[Vector]
    sides: list[Side]
    perimeter: int

    def add_side(self, inside: Vector, direction: Vector):
        x, y = inside
        lateral = [(x + d_x, y + d_y) for d_x, d_y in to_lateral(direction)]
        for side in self.sides:
            if direction != side.direction:
                continue
            if inside in side.inside:
                return
            for point in side.inside:
                if point in lateral:
                    side.inside.append(inside)
                    print("attached")
                    return
        print("new side")
        self.sides.append(Side([inside], direction))


def print_path(map, region):
    result = [["."] * len(map[0]) for _ in range(len(map))]
    for x, y in region:
        result[x][y] = map[x][y]
    print(" 01234")
    for i, row in enumerate(result):
        print(str(i) + "".join([str(v) for v in row]))


def part_one(map: list[list[str]]) -> int:
    X, Y = len(map), len(map[0])
    regions: list[Region] = []
    visited: set[Vector] = set()

    def dfs(point, region: Region):
        x, y = point
        if point in visited or not 0 <= x < X or not 0 <= y < Y or map[x][y] != plant:
            if point not in region.points:
                region.perimeter += 1
            return

        visited.add(point)
        region.points.add(point)
        for d_x, d_y in directions:
            dfs((x + d_x, y + d_y), region)

    for i, row in enumerate(map):
        for j, plant in enumerate(row):
            region = Region(plant, set(), [], 0)
            dfs((i, j), region)
            if len(region.points) > 0:
                regions.append(region)

    total = 0
    for region in regions:
        area = len(region.points)
        perim = region.perimeter
        total += area * perim
        print_path(map, region.points)

    return total


def part_two(map: list[list[str]]) -> int:
    X, Y = len(map), len(map[0])
    regions: list[Region] = []
    visited: set[Vector] = set()

    def dfs(point, region: Region, prev: Optional[Vector] = None):
        x, y = point
        if point in visited or not 0 <= x < X or not 0 <= y < Y or map[x][y] != plant:
            if point not in region.points and prev is not None:
                p_x, p_y = prev
                direction = (x - p_x, y - p_y)
                region.add_side(prev, direction)
                region.perimeter += 1
            return

        visited.add(point)
        region.points.add(point)
        # update sides
        for d_x, d_y in directions:
            n_x, n_y = x + d_x, y + d_y
            next_point = (n_x, n_y)
            if not 0 <= n_x < X or not 0 <= n_y < Y or map[n_x][n_y] != region.plant:
                region.add_side(point, (d_x, d_y))
            dfs(next_point, region, point)

    for i, row in enumerate(map):
        for j, plant in enumerate(row):
            region = Region(plant, set(), [], 0)
            dfs((i, j), region)
            if len(region.points) > 0:
                regions.append(region)

    total = 0
    for region in regions:
        print_path(map, region.points)
        # print(f"sides: {len(region.sides)}")
        area = len(region.points) * len(region.sides)
        print(f"{region.plant}: {len(region.sides)} {area}")
        lookup = defaultdict(list)
        for side in region.sides:
            for pt in side.inside:
                lookup[pt].append(side.direction)
        print(f"sides: {" " + "\n".join(sorted([str(x) for x in region.sides]))}")
        for k in sorted(lookup.keys()):
            print(f"{k}: {lookup[k]}")
        print()
        total += area

    return total


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    map = []
    for line in lines:
        map.append([c for c in line.strip()])
    print(f"part_one: {part_one(map)}")
    print(f"part_two: {part_two(map)}")
