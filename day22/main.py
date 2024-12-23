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


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


def part_one(numbers: list[int]) -> int:
    total = 0

    def next(sn: int) -> int:
        sn = prune(mix(sn * 64, sn))
        sn = prune(mix(sn // 32, sn))
        sn = prune(mix(sn * 2048, sn))
        return sn

    for sn in numbers:
        for _ in range(2000):
            sn = next(sn)
        total += sn

    return total


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    numbers = [int(line.strip()) for line in lines]
    print(f"Part one: {part_one(numbers)}")
    # print(f"Part two: {part_two(towels, patterns)}")
