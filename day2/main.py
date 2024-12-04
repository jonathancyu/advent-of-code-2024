from argparse import ArgumentParser
from pathlib import Path


def parse_report(line: str) -> list[int]:
    return [int(s) for s in line.split()]


inc_range = range(1, 4)
dec_range = range(-1, -4, -1)


def safe_report_wrapper(report: list[int]):
    return (
        safe_report(report, None, False)
        or safe_report(report[:1] + report[2:], None, True)
        or safe_report(report[1:], None, True)
    )


def safe_report(
    report: list[int], increasing: bool | None = None, skipped: bool = False
) -> bool:
    print(f"trying  {report}, skip={skipped}, inc={increasing}")
    prev = report[0]
    curr = report[1]
    diff = curr - prev
    inc = diff in inc_range
    dec = diff in dec_range

    if len(report) == 2:
        assert increasing is not None  # problem specific, oh well
        result = (increasing and inc) or (not increasing and dec)
        print(f" 2 -> {result}")
        return (not skipped) or (increasing and inc) or (not increasing and dec)
    assert len(report) > 2

    original_increasing = increasing

    if increasing is None:
        if inc:
            # print(1)
            increasing = True
        elif dec:
            # print(2)
            increasing = False

    print(f"   inc: {increasing}")
    if (
        increasing is not None
        and (increasing and not inc)
        or (not increasing and not dec)
    ):
        print("   non compliant")
        return False

    return safe_report(report[1:], increasing, skipped) or (
        not skipped
        and safe_report(
            report[:1] + report[2:],
            original_increasing,
            True,  # If current not safe, remove it.
        )
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
        print()
        print()
        key = " ".join(str(x) for x in report)
        actual[key] = safe_report_wrapper(report)
        if expected[key] != actual[key]:
            print(f"zOOO {report}")
            print(f"{key}: expected {expected[key]}, got {actual[key]}")
            print()

    part_two = len([report for report in reports if safe_report_wrapper(report)])
    print(f"Part 2: {part_two}")
