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


class UnionFind:
    def __init__(self, n: int):
        self.par = {}
        self.rank = {}

        for i in range(n):
            # Setting parent to itself makes union logic simpler
            self.par[i] = i
            self.rank[i] = 0

    def find(self, n: int):
        # Finds the root of x
        p = self.par[n]  # Starting from the NODE:
        # Path compression: As we find, shift each node up.
        # Ideally, the tree's rank is onl 1.
        while p != self.par[p]:  # Root node's parent is itself
            self.par[p] = self.par[self.par[p]]
            p = self.par[p]

        return p

    def union(self, n1: int, n2: int):
        # Union roots of n1 and n2 together
        p1, p2 = self.find(n1), self.find(n2)
        if p1 == p2:
            # Already the same tree, thus:
            # 1) duplicate edge
            # or
            # 2) cycle exists (if undirected)
            return False

            # Merge shorter tree into taller tree
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
        elif self.rank[p1] < self.rank[p2]:
            self.par[p1] = p2
        else:
            # Heights are equal, so rank will increase.
            self.par[p1] = p2
            self.rank[p2] += 1
        return True


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


@dataclass
class Edge:
    point: Vector
    outwards: Vector


@dataclass
class Region:
    plant: str
    points: set[Vector]
    edges: list[Edge]
    perimeter: int


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


@dataclass
class Side:
    inside: list[Vector]
    direction: Vector


def to_lateral(direction):
    x, y = direction
    return [(-y, x), (y, -x)]


def count_sides(region: Region) -> int:
    lookup: dict[tuple[Vector, Vector], int] = {}
    # Merge edges into sides.
    sides = UnionFind(len(region.edges))
    for i, edge in enumerate(region.edges):
        x, y = edge.point
        lookup[(edge.point, edge.outwards)] = i  # Add to lookup
        # Find adjacent sides
        neighbors = [(x + d_x, y + d_y) for d_x, d_y in to_lateral(edge.outwards)]
        adjacent_sides = [
            lookup[(pos, edge.outwards)]
            for pos in neighbors
            if (pos, edge.outwards) in lookup
        ]
        if len(adjacent_sides) == 1:
            sides.union(i, adjacent_sides[0])
        elif len(adjacent_sides) == 2:
            sides.union(i, adjacent_sides[0])
            sides.union(i, adjacent_sides[1])

    # Get final joined edges
    all_sides = set()
    for i in range(len(region.edges)):
        all_sides.add(sides.find(i))
    return len(all_sides)


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
                region.edges.append(Edge(point, direction))
                region.perimeter += 1
            return

        visited.add(point)
        region.points.add(point)
        for d_x, d_y in directions:
            dfs((x + d_x, y + d_y), region, point)

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
        total += len(region.points) * count_sides(region)

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
