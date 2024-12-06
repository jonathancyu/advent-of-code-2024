from argparse import ArgumentParser
from copy import deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Counter, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm


def print_mat(matrix, pos):
    for i, row in enumerate(matrix):
        for j, col in enumerate(row):
            if (i, j) == pos:
                print("^", end="")
            else:
                print(col, end="")
        print()


def rotate(i, j):
    return j, -i


def part_one(
    matrix: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]
) -> set:
    X, Y = len(matrix), len(matrix[0])
    pos_visited = set()
    visited = set()
    while True:
        # print(pos, dir)
        # print_mat(matrix, pos)
        if (pos, dir) in visited:
            return None

        pos_visited.add(pos)
        visited.add((pos, dir))
        p_i, p_j = pos
        matrix[p_i][p_j] = "X"
        d_i, d_j = dir
        x, y = p_i + d_i, p_j + d_j
        if not 0 <= x < X or not 0 <= y < Y:
            break
        next = matrix[x][y]

        # Rotate inplace til we get a good direction
        while next == "#":
            dir = rotate(*dir)
            d_i, d_j = dir
            x, y = p_i + d_i, p_j + d_j
            if not 0 <= x < X or not 0 <= y < Y:
                return pos_visited
            next = matrix[x][y]

        pos = (x, y)
    return pos_visited


def add_obs(matrix: list[list[str]], pos: tuple[int, int]) -> list[list[str]]:
    matrix = deepcopy(matrix)
    x, y = pos
    matrix[x][y] = "#"
    return matrix


def part_two(
    visited: set[tuple[int, int]],
    matrix: list[list[str]],
    start_pos: tuple[int, int],
    dir: tuple[int, int],
) -> int:
    count = 0
    for pos in visited:
        test = add_obs(matrix, pos)
        if part_one(test, start_pos, dir) is None:
            count += 1
    return count


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    matrix = []
    pos: Optional[tuple[int, int]] = None
    direction = (-1, 0)
    for x, line in enumerate(lines):
        row = []
        for y, char in enumerate(line.strip()):
            if char == "^":
                pos = (x, y)
                char = "."
            row.append(char)
        matrix.append(row)
    assert pos is not None
    visited = part_one(matrix, pos, direction)
    print(f"Part one: {len(visited)}")

    print(f"Part two: {part_two(visited, matrix, pos, direction)}")
