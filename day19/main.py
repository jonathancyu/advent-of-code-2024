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


def part_one(towels: list[str], patterns: list[str]) -> int:
    lkp = {}

    def dfs(pattern: str) -> bool:
        if pattern in lkp:
            return lkp[pattern]
        for towel in towels:
            if not pattern.startswith(towel):
                continue
            if towel == pattern:
                lkp[pattern] = True
                return True
            towel_len = len(towel)
            if dfs(pattern[towel_len:]):
                lkp[pattern] = True
                return True
        lkp[pattern] = False
        return False

    possible = 0
    for pattern in patterns:
        if dfs(pattern):
            print(pattern)
            possible += 1

    return possible


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    towels = [x.strip() for x in lines[0].strip().split(",")]
    patterns = [x.strip() for x in lines[2:]]
    print(towels, patterns)
    print(f"Part one: {part_one(towels, patterns)}")
    # print(f"Part two: {part_two(points, size)}")
