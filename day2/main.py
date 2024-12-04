from argparse import ArgumentParser
from pathlib import Path


def parse_report(line: str) -> list[int]:
    return [int(s) for s in line.split()]


inc_range = range(1, 4)
dec_range = range(-1, -4, -1)

lookup: dict[tuple[tuple[int, ...], bool | None, bool], bool] = {}


def safe_report_base_case(report: list[int]):
    # TODO: i dont wanna need this
    return (
        safe_report(report, None, False)
        or safe_report(report[:1] + report[2:], None, True)
        or safe_report(report[1:], None, True)
    )


def safe_report(
    report: list[int], increasing: bool | None = None, skipped: bool = False
) -> bool:
    """
    Recursive backtracking. Could also have been implemented with a graph search (DFS/BFS)
    """
    key = (tuple(report), increasing, skipped)
    if key in lookup:
        # Lookup cached value to prevent re-visiting nodes
        return lookup[key]
    prev = report[0]
    curr = report[1]
    diff = curr - prev
    inc = diff in inc_range
    dec = diff in dec_range

    if len(report) <= 2:
        result = (increasing and inc) or (not increasing and dec)
        lookup[key] = result
        return result

    original_increasing = increasing

    if increasing is None:
        if inc:
            increasing = True
        elif dec:
            increasing = False

    result = None
    if (
        increasing is not None
        and (increasing and not inc)
        or (not increasing and not dec)
    ):
        # End recursion if we fail a test.
        result = False
    elif skipped:
        result = safe_report(report[1:], increasing, skipped)  # Can't use a skip
    else:
        result = (
            # Try to not use a skip
            safe_report(report[1:], increasing, False)
            # Skip first
            or safe_report(report[1:], original_increasing, True)
            # Skip second
            or safe_report(report[:1] + report[2:], original_increasing, True)
            # Skip third
            or safe_report(report[:2] + report[3:], original_increasing, True)
        )

    lookup[key] = result
    return result


def read_expected() -> dict[str, bool]:
    result: dict[str, bool] = {}
    with open("day2/test.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        split = line.split("=")
        assert len(split) == 2
        rhs: str = split[1].strip()
        assert rhs in ["true", "false"]

        result[split[0].strip()] = rhs == "true"

    return result


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    reports = [parse_report(line) for line in lines]
    # Part one
    part_one = len([report for report in reports if safe_report(report, skipped=True)])
    print(f"Part 1: {part_one}")

    # Part two
    expected: dict[str, bool] = read_expected()
    actual: dict[str, bool] = {}
    for report in reports:
        key = " ".join(str(x) for x in report)
        actual[key] = safe_report_base_case(report)
        if expected[key] != actual[key]:
            print(f"{key}: expected {expected[key]}, got {actual[key]}")

    part_two = len([report for report in reports if safe_report_base_case(report)])
    print(f"Part 2: {part_two}")
