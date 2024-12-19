from argparse import ArgumentParser
import json
import sys
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

    q: deque[tuple[Vector, set[Vector]]] = deque()
    start = (0, 0)
    q.append((start, set()))
    min_dist = math.inf
    while q:
        pos, visited = q.popleft()
        x, y = pos
        if pos in visited or not 0 <= x < X or not 0 <= y < Y or pos in corrupted:
            continue
        if pos == target:
            min_dist = min(len(visited), min_dist)
            continue
        visited.add(pos)

        for d_x, d_y in directions:
            q.append(((x + d_x, y + d_y), visited.copy()))

    return int(min_dist)


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
