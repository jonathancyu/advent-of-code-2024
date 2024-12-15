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


@dataclass
class Robot:
    pos: Vector
    velocity: Vector


def part_one(robots: list[Robot], size: Vector, steps: int) -> int:
    X, Y = size
    print(size)
    positions = []
    for robot in robots:
        p_x, p_y = robot.pos
        v_x, v_y = robot.velocity
        positions.append(((p_x + v_x * steps) % X, (p_y + v_y * steps) % Y))

    h_x = X // 2
    h_y = Y // 2
    counts = [0] * 4
    for p_x, p_y in positions:
        if p_x == h_x or p_y == h_y:
            continue
        left, up = p_x < h_x, p_y < h_y
        if left and up:
            counts[0] += 1
        elif left and not up:
            counts[1] += 1
        elif not left and up:
            counts[2] += 1
        elif not left and not up:
            counts[3] += 1
    return math.prod(counts)


def get_positions(robots: list[Robot], size: Vector, steps: int) -> list[Vector]:
    X, Y = size
    positions = []
    for robot in robots:
        p_x, p_y = robot.pos
        v_x, v_y = robot.velocity
        positions.append(((p_x + v_x * steps) % X, (p_y + v_y * steps) % Y))
    return positions


def print_board(positions: list[Vector], size: Vector) -> None:
    X, Y = size
    counts = Counter(positions)
    result = [[" "] * Y for _ in range(X)]
    for pos, count in counts.items():
        x, y = pos
        result[x][y] = str(count)
    print("\n".join(["".join(x) for x in result]))
    print("-" * 100)
    print()


def part_two(robots: list[Robot], size: Vector) -> int:
    print(size)
    i = 0
    while True:
        i += 1
        positions = get_positions(robots, size, i)
        counts = Counter(positions)
        if max(counts.values()) == 1:
            break

    print_board(positions, size)

    return i


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    robots = []
    size_split = lines[0].split(",")
    steps = int(lines[1].strip())
    size: Vector = (int(size_split[0]), int(size_split[1]))
    lines = lines[2:]
    for line in lines:
        split = line.split(" ")
        pos_split = split[0].split("=")[1].split(",")
        vel_split = split[1].split("=")[1].split(",")
        robots.append(
            Robot(
                pos=(int(pos_split[0]), int(pos_split[1])),
                velocity=(int(vel_split[0]), int(vel_split[1])),
            )
        )

    print(f"part_one: {part_one(robots, size, steps)}")
    print(f"part_two: {part_two(robots, size)}")
