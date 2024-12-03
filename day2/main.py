from argparse import ArgumentParser
from pathlib import Path


def parse_report(line: str) -> list[int]:
    return [int(s) for s in line.split()]


inc_range = range(1, 4)
dec_range = range(-1, -4, -1)


def safe_report(
    report: list[int], increasing: bool | None = None, skipped: bool = False
) -> bool:
    if len(report) <= 1:
        return True
    prev = report[0]
    curr = report[1]
    diff = curr - prev
    inc = diff in inc_range
    dec = diff in dec_range
    if increasing is None:
        if inc:
            increasing = True
        elif dec:
            increasing = False
        elif not skipped:
            # Only occurs when increasing is none, which only happens on first occurrence
            return safe_report(report[1:], skipped=True)
        else:
            return False

    if (increasing and not inc) or (not increasing and not dec):
        if not skipped:
            # Try to skip this value
            # [prev, next, ...] -> next is in violation, so skip next.
            spliced_report = report[:1] + report[2:]
            return safe_report(spliced_report, skipped=True)
        return False

    return safe_report(report[1:], increasing, skipped)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    reports = [parse_report(line) for line in lines]
    # print(reports)
    part_one = len([report for report in reports if safe_report(report, skipped=True)])
    print(f"Part 1: {part_one}")
    part_two = len([report for report in reports if safe_report(report)])
    print(f"Part 2: {part_two}")
