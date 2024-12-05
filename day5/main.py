from argparse import ArgumentParser
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Optional


@dataclass
class Node:
    val: Optional[int] = None
    next: Optional["Node"] = None


def print_list(node: Optional[Node]):
    if node is None:
        print("null list")
        return
    # Skip the head pointer if it has no value
    current = node.next if node.val is None else node
    values = []

    while current is not None:
        values.append(str(current.val))
        current = current.next


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
        print(value)
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
        print(line)
        if "|" in line:
            split = line.split("|")
            assert len(split) == 2
            pre, post = split
            rules[int(post)].add(int(pre))
        elif "," in line:
            head_pointer = Node()
            current = head_pointer
            for value in line.strip().split(","):
                current.next = Node(val=int(value.strip()))
                current = current.next

            assert head_pointer.next is not None
            reports.append(head_pointer.next)

    total = 0
    for report in reports:
        print_list(report.next)
        result = check_update(rules, report)
        if result is not None:
            total += result

    print(f"result: {total}")
