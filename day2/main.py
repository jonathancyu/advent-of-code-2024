from argparse import ArgumentParser
from pathlib import Path


def parse_report(line: str) -> list[int]:
    return [int(s) for s in line.split()]


inc_range = range(1, 4)
dec_range = range(-1, -4, -1)


def safe_report(
    report: list[int], increasing: bool | None = None, skipped: bool = False
) -> bool:
    # print(f"  {skipped}, {report}")
    if len(report) <= 1:
        return True
    prev = report[0]
    curr = report[1]
    diff = curr - prev
    inc = diff in inc_range
    dec = diff in dec_range
    original_increasing = increasing
    if increasing is None:
        if inc:
            # print(1)
            increasing = True
        elif dec:
            # print(2)
            increasing = False
        else:
            # print(3)
            return False

    if (increasing and not inc) or (not increasing and not dec):
        return False

    return safe_report(report[1:], increasing, skipped) or (
        not skipped
        and safe_report(
            report[1:], original_increasing, True
        )  # If current not safe, remove it.
    )


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
    # print(reports)
    # part_one = len([report for report in reports if safe_report(report, skipped=True)])
    # print(f"Part 1: {part_one}")
    expected: dict[str, bool] = read_expected()
    actual: dict[str, bool] = {}
    for report in reports:
        print("-" * 100)
        key = " ".join(str(x) for x in report)
        actual[key] = safe_report(report)

    # Compare and print differences
    diffs = []
    for key in expected:
        if key in actual and expected[key] != actual[key]:
            diffs.append(f"{key}: expected {expected[key]}, got {actual[key]}")
    print("\n".join(diffs))
    print(len(diffs))

    # part_two = len([report for report in reports if safe_report(report)])
    # print(f"Part 2: {part_two}")
