from argparse import ArgumentParser
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
) -> int:
    X, Y = len(matrix), len(matrix[0])
    pos_visited = set()
    while True:
        # print(pos, dir)
        # print_mat(matrix, pos)
        pos_visited.add(pos)
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
                return len(pos_visited)
            next = matrix[x][y]

        pos = (x, y)
    return len(pos_visited)


def part_two(
    matrix: list[list[str]], pos: tuple[int, int], dir: tuple[int, int]
) -> int:
    X, Y = len(matrix), len(matrix[0])
    directions_needed: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    obstructions = set()
    while True:
        # print(pos, dir)
        # print_mat(matrix, pos)
        p_i, p_j = pos
        matrix[p_i][p_j] = "X"
        d_i, d_j = dir
        x, y = p_i + d_i, p_j + d_j
        if not 0 <= x < X or not 0 <= y < Y:
            break
        next = matrix[x][y]
        # Rotate inplace til we get a good direction
        while next == "#":
            # Project away from wall
            opposite_dir = (-d_i, -d_j)
            x, y = pos
            while 0 <= x < X and 0 <= y < Y and matrix[x][y] != "#":
                directions_needed[(x, y)].add(dir)
                x -= d_i
                y -= d_j

            # Rotate til no wall
            dir = (d_j, -d_i)
            d_i, d_j = dir
            x, y = p_i + d_i, p_j + d_j
            if not 0 <= x < X or not 0 <= y < Y:
                return len(obstructions)
            next = matrix[x][y]

        # If next is a free square, then see if we can cause a loop
        rotated = rotate(*dir)
        if rotated in directions_needed[pos]:
            matrix[x][y] = "O"
            obstructions.add((x, y))
        directions_needed[pos].add(dir)

        pos = (x, y)

    for x, y in obstructions:
        matrix[x][y] = "O"
    return len(obstructions)


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
    # print(f"Part one: {part_one(matrix, pos, direction)}")
    print(f"Part two: {part_two(matrix, pos, direction)}")
