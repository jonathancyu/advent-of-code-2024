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


directions = {"^": (-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}


def print_map(map: list[list[str]], pos: Vector) -> None:
    map = deepcopy(map)
    x, y = pos
    map[x][y] = "@"
    print("\n".join(["".join(x) for x in map]))
    print("-" * 100)
    print()


def make_move_one(map: list[list[str]], pos: Vector, move: str) -> Vector:
    # print(f"Move: {move}")
    X, Y = len(map), len(map[0])
    assert move in directions
    d_x, d_y = directions[move]
    x, y = pos
    path = []
    while True:
        x += d_x
        y += d_y
        if not 0 <= x < X or not 0 <= y <= Y:
            break

        value = map[x][y]
        if value == "#":
            return pos
        elif value == ".":
            break
        else:
            assert value == "O"
            path.append((x, y))
    # If we havent returned, then we're not blocked. So move everything in the path
    for x_old, y_old in path[::-1]:
        x, y = x_old + d_x, y_old + d_y
        map[x][y] = map[x_old][y_old]
        map[x_old][y_old] = "."
    p_x, p_y = pos
    new_pos = (p_x + d_x, p_y + d_y)
    # print_map(map, new_pos)
    return new_pos


def part_one(map: list[list[str]], pos: Vector, moves: list[str]) -> int:
    map = deepcopy(map)
    for move in moves:
        pos = make_move_one(map, pos, move)

    total = 0
    for i, row in enumerate(map):
        for j, val in enumerate(row):
            if val == "O":
                total += (100 * i) + j
    return total


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    map = []
    i = 0
    pos = None
    while len(lines[i].strip()) != 0:
        line = lines[i]
        row = []
        for j, c in enumerate(line.strip()):
            if c == "@":
                assert pos is None
                pos = (i, j)
                c = "."
            row.append(c)
        map.append(row)
        i += 1
    assert pos is not None
    moves: list[str] = []
    for line in lines[i + 1 :]:
        for move in line.strip():
            moves.append(move)
    print(moves)

    print_map(map, pos)
    print(f"part_one: {part_one(map, pos, moves)}")
