use std::{env, fs};

enum Direction {
    Unset,
    Increasing,
    Decreasing,
}

fn is_safe(report: Vec<u32>) -> bool {
    if report.is_empty() {
        return true;
    }

    let mut values = report.iter();
    let mut last = *values.next().unwrap();
    let mut dir = Direction::Unset;

    for &val in values {
        let gt = val > last;
        let lt = val < last;
        match dir {
            Direction::Unset => {
                if gt {
                    dir = Direction::Increasing;
                } else {
                    dir = Direction::Decreasing;
                }
            }

            Direction::Increasing => {
                if !gt {
                    return false;
                }
            }
            Direction::Decreasing => {
                if !lt {
                    return false;
                }
            }
        }
        let diff = last.abs_diff(val);
        if !(1..=3).contains(&diff) {
            return false;
        }
        last = val;
    }

    true
}

fn split_line(line: &str) -> Vec<u32> {
    line.split_whitespace()
        .map(|v| v.trim().parse::<u32>().unwrap())
        .collect::<Vec<u32>>()
}

fn part_one() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);
    assert_eq!(2, args.len());
    let file_path = args.get(1).unwrap();
    let file = fs::read_to_string(file_path).expect("Unable to read file");
    let matches = file
        .lines()
        .map(split_line)
        .map(is_safe)
        .filter(|x| *x)
        .count();
    println!("Compliant reports: {matches}");
}

fn part_two() {}

fn main() -> std::io::Result<()> {
    part_one();
    part_two();
    Ok(())
}
