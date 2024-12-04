from argparse import ArgumentParser
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import deque


# HJKL
directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
directions.extend(product([-1, 1], [-1, 1]))  # Add diagonals
diagonals = list(product([-1, 1], [-1, 1]))
print(directions)


@dataclass(frozen=True)
class Entry:
    pos: tuple[int, int]
    remaining: deque[str]

    def __str__(self):
        return f"{self.pos}, {list(self.remaining)}"

    def __hash__(self):
        return hash((self.pos, tuple(self.remaining)))


def count_matches(matrix: list[list[str]], word: str, pos: tuple[int, int]) -> int:
    X = len(matrix)
    Y = len(matrix[0])
    queue: list[Entry] = [Entry(pos, deque([c for c in word]))]
    count = 0
    visited = set()
    while queue:
        entry = queue.pop()
        i, j = entry.pos
        if entry in visited or not 0 <= i < X or not 0 <= j < Y:
            continue
        visited.add(entry)

        remaining = entry.remaining.copy()
        first = remaining.popleft()

        if matrix[i][j] != first:
            continue
        if len(remaining) == 0:
            count += 1
            continue
        print(f"exploring {matrix[i][j]} at {entry}")
        for d_i, d_j in directions:
            queue.append(Entry(pos=(i + d_i, j + d_j), remaining=remaining))

    return count


def match_direction(
    matrix: list[list[str]], word: str, pos: tuple[int, int], dir: tuple[int, int]
) -> bool:
    p_i, p_j = pos
    d_i, d_j = dir
    X = len(matrix)
    Y = len(matrix[0])
    for d in range(len(word)):
        i, j = p_i + d_i * d, p_j + d_j * d
        if not 0 <= i < X or not 0 <= j < Y or matrix[i][j] != word[d]:
            return False

    return True


def count_easy_occurrences(matrix: list[list[str]], word: str, pos: tuple[int, int]):
    p_i, p_j = pos
    count = 0
    print(matrix[p_i][p_j])
    for dir in directions:
        if match_direction(matrix, word, pos, dir):
            count += 1
    return count


def count_occurrences(matrix: list[list[str]], word: str) -> int:
    X = len(matrix)
    Y = len(matrix[0])
    total = 0
    for i in range(X):
        for j in range(Y):
            num_matches = count_easy_occurrences(matrix, word, (i, j))

            if num_matches > 0:
                print(f"matrix[{i}][{j}] = {num_matches}")
            total += num_matches
    return total


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()

    length: int | None = None
    matrix = []
    for line in lines:
        line = line.strip()
        if length is None:
            length = len(line)
        assert len(line) == length
        matrix.append([c for c in line])
    print(f"Part 1: {count_occurrences(matrix, "XMAS")}")
