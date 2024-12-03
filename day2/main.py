from argparse import ArgumentParser
from pathlib import Path


def parse_report(line: str) -> list[int]:
    return [int(s) for s in line.split()]


inc_range = range(1, 4)
dec_range = range(-1, -4, -1)


def safe_report(report: list[int], increasing: bool | None = None) -> bool:
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
        else:  # Not allowed
            return False

    if (increasing and not inc) or (not increasing and not dec):
        return False

    return safe_report(report[1:], increasing)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=Path)
    file = arg_parser.parse_args().file
    with open(file, "r") as f:
        lines = f.readlines()
    reports = [parse_report(line) for line in lines]
    # print(reports)
    passing = [report for report in reports if safe_report(report)]
    print(len(passing))
