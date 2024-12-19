from argparse import ArgumentParser
import json
import sys
from copy import deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
import heapq
from typing import Callable, Counter, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm
import math

Vector = tuple[int, int]


def draw_map(points: list[Vector], size: Vector, char: str) -> None:
    result = [["."] * size[1] for _ in range(size[0])]
    for x, y in points:
        result[y][x] = char
    print("\n".join("".join(x) for x in result))


def to_vec(line: str) -> Vector:
    split = line.strip().split(",")
    return (int(split[0]), int(split[1]))


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def part_one(points: list[Vector], size: Vector, steps: int) -> int:
    X, Y = size
    target = (X - 1, Y - 1)

    corrupted = set(points[:steps])

    start = (0, 0)
    # Dijkstra's algorithm
    dist: dict[Vector, float] = defaultdict(lambda: math.inf)
    dist[start] = 0

    q: list[tuple[float, Vector]] = [(0, start)]
    visited: set[Vector] = corrupted
    while q:
        cur_dist, pos = heapq.heappop(q)
        x, y = pos
        print(pos)
        if not 0 <= x < X or not 0 <= y < Y or pos in visited:
            continue
        visited.add(pos)

        for d_x, d_y in directions:
            neighbor = (x + d_x, y + d_y)
            new_dist = cur_dist + 1
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
            heapq.heappush(q, (new_dist, neighbor))
    print(dist)

    return int(dist[target])


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    steps = int(lines[0].strip())
    size = to_vec(lines[1])
    lines = lines[2:]
    points: list[Vector] = []
    for line in lines:
        points.append(to_vec(line))
    sys.setrecursionlimit(5000)  # XD
    print(f"Part one: {part_one(points, size, steps)}")
