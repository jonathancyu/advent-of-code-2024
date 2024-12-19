from argparse import ArgumentParser
import json
import sys
from copy import deepcopy
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Callable, Counter, Literal, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm
import math

Register = Literal["A", "B", "C"]


def div(a: int, b: int) -> int:
    return int(a / math.pow(2, b))


def part_one(program: list[tuple[int, int]], reg: dict[Register, int]) -> str:
    combo: dict[int, Callable[[], int]] = {}
    combo[0] = lambda: 0
    combo[1] = lambda: 1
    combo[2] = lambda: 2
    combo[3] = lambda: 3
    combo[4] = lambda: reg["A"]
    combo[5] = lambda: reg["B"]
    combo[6] = lambda: reg["C"]

    output = []

    # Operations

    def adv(arg):
        reg["A"] = div(reg["A"], combo[arg]())

    def bxl(arg) -> None:
        reg["B"] = arg ^ reg["B"]

    def bst(arg) -> None:
        reg["B"] = combo[arg]() % 8

    def jnz(arg) -> Optional[int]:
        if reg["A"] == 0:
            return
        return arg

    def bxc(_) -> None:
        reg["B"] = reg["B"] ^ reg["C"]

    def out(arg) -> None:
        output.append(combo[arg]() % 8)

    def bdv(arg) -> None:
        reg["B"] = div(reg["A"], combo[arg]())

    def cdv(arg) -> None:
        reg["C"] = div(reg["A"], combo[arg]())

    ops: dict[int, Callable[[int], Optional[int]]] = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }
    pointer = 0
    while True:
        if pointer >= len(program):
            break
        op, arg = program[pointer]
        print(f"{pointer}: {op}, {arg}")
        print(f"{reg}")
        assert op in ops

        result = ops[op](arg)
        if result is not None:
            pointer = result
        else:
            pointer += 1
        print(output)
        print()
    print(f"{reg}")

    return ",".join(str(x) for x in output)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    registers: dict[Register, int] = {}

    def set_reg(reg: Register, line: str):
        rhs = line.split(":")[1].strip()
        registers[reg] = int(rhs)

    set_reg("A", lines[0])
    set_reg("B", lines[1])
    set_reg("C", lines[2])

    line = lines[4].split(":")[1]
    literals = [int(x) for x in line.strip().split(",")]
    program = list(zip(literals[::2], literals[1::2]))
    print(registers, program)
    print(f"Part one: {part_one(program, registers)}")
