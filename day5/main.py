from argparse import ArgumentParser
from random import shuffle
from pathlib import Path
from itertools import product
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Counter, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    return get_midpoint(update_head)


def get_midpoint(head: Node) -> int:
    # Get midpoint
    slow = fast = head
    while fast.next and fast.next.next:
        assert slow.next is not None
        slow = slow.next
        fast = fast.next.next
    midpoint = slow
    assert midpoint is not None and midpoint.val is not Node
    return midpoint.val


def topo_sort(edges: list[tuple[int, int]], values: list[int]) -> list[int]:
    outgoing_edges = defaultdict(list)
    for src, dst in edges:
        outgoing_edges[src].append(dst)

    result = []
    visited = set()

    def dfs(node: int):
        if node in visited:
            return
        visited.add(node)
        for dst in outgoing_edges[node]:
            dfs(dst)
        result.append(node)

    # dfs from each orphan node
    for value in values:
        if value in outgoing_edges:
            continue
        print(f"root: {value}")
        dfs(value)

    # Append unvisited nodes to the end
    print(result)
    return result


def fix_sequence(rules: list[tuple[int, int]], report: Node):
    values = report.values()
    edges: list[tuple[int, int]] = []  # Edge from A -> B means B must come after A
    for rule in rules:
        print(rule)
        a, b = rule
        # TODO: one or two edges?
        if a in values or b in values:
            edges.append(rule)
    sorted = topo_sort(edges, values)
    return get_midpoint(Node.from_list(sorted))  # XD


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()

    length: int | None = None
    matrix = []
    rules: list[tuple[int, int]] = []
    predecessors: dict[int, set[int]] = defaultdict(set)
    reports: list[Node] = []
    for line in lines:
        if "|" in line:
            split = line.split("|")
            assert len(split) == 2
            pre, post = split
            a, b = int(pre), int(post)
            predecessors[b].add(a)
        elif "," in line:

            reports.append(Node.from_list([int(x) for x in line.split(",")]))

    # Part 1
    total = 0
    for report in reports:
        result = check_update(predecessors, report)
        if result is not None:
            total += result
    print(f"part 1: {total}")

    total = 0
    for report in reports:
        if check_update(predecessors, report) is not None:
            continue
        result = fix_sequence(rules, report)
        total += result
    print(f"part 2: {total}")


def part_2_bogo(rules, report):
    """
    Bogo sort.
    """

    def process_report(report: Node) -> Optional[int]:
        result = check_update(rules, report)
        if result is not None:
            # Passed initially, so ignore it
            return None

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
                return result
            tried.add(tuple_vals)

    # Part 2
    total = 0
    with ThreadPoolExecutor() as executor:
        future_to_report = {
            executor.submit(process_report, report): report for report in reports
        }

        for future in tqdm(as_completed(future_to_report), total=len(reports)):
            result = future.result()
            if result is not None:
                total += result
