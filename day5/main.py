from argparse import ArgumentParser
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Optional

from tqdm.auto import tqdm


@dataclass
class Node:
    val: Optional[int] = None
    next: Optional["Node"] = None

    @classmethod
    def from_list(cls, lst: list[int]) -> "Node":
        head_pointer = Node()
        current = head_pointer
        for value in lst:
            current.next = Node(val=int(value))
            current = current.next

        assert head_pointer.next is not None
        return head_pointer.next

    def values(self):
        # Skip the head pointer if it has no value
        current = self.next if self.val is None else self
        values = []

        while current is not None:
            values.append(str(current.val))
            current = current.next
        return values


def check_update(rules: dict[int, set[int]], update_head: Node) -> Optional[int]:
    # Get set of all elements
    elements = set()
    current = update_head
    while current:
        elements.add(current.val)
        current = current.next

    # Check rules
    seen: set[int] = set()
    current = update_head
    while current:
        assert current.val is not None
        value = current.val
        if value in rules:
            for predecessor in rules[value]:
                if predecessor not in elements:
                    continue
                if predecessor not in seen:
                    return None
        seen.add(value)
        current = current.next

    # Get midpoint
    slow = fast = update_head
    while fast.next and fast.next.next:
        assert slow.next is not None
        slow = slow.next
        fast = fast.next.next
    midpoint = slow
    assert midpoint is not None
    return midpoint.val


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()

    length: int | None = None
    matrix = []
    rules: dict[int, set[int]] = defaultdict(set)
    reports: list[Node] = []
    for line in lines:
        if "|" in line:
            split = line.split("|")
            assert len(split) == 2
            pre, post = split
            rules[int(post)].add(int(pre))
        elif "," in line:

            reports.append(Node.from_list([int(x) for x in line.split(",")]))

    # Part 1
    total = 0
    for report in reports:
        result = check_update(rules, report)
        if result is not None:
            total += result
    print(f"part 1: {total}")

    # Part 2
    total = 0
    for report in tqdm(reports):
        result = check_update(rules, report)
        if result is not None:
            # Skip working
            continue
        tried = set()
        while True:
            values = report.values()
            shuffle(values)
            tuple_vals = tuple(values)
            if tuple_vals in tried:
                continue
            shuffled = Node.from_list(values)
            result = check_update(rules, shuffled)
            if result is not None:
                print(type(result), result)
                total += result
                break
            tried.add(tuple_vals)

    print(f"part 2: {total}")
