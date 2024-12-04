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
    let mut lines: Vec<String> = vec![];
    let matches = file
        .lines()
        .map(split_line)
        .map(|record| {
            let result = is_safe(record.clone());
            let lhs = record
                .iter()
                .map(|n| n.to_string())
                .collect::<Vec<String>>()
                .join(" ");
            lines.push(format!("{} = {}", lhs, result));
            result
        })
        .filter(|x| *x)
        .count();
    fs::write("test.txt", lines.join("\n")).unwrap();
    println!("Compliant reports: {matches}");
}
fn is_safe_lenient(report: Vec<u32>) -> bool {
    if is_safe(report.clone()) {
        return true;
    }

    for index in (0..report.len()) {
        let sub_report = report
            .iter()
            .enumerate()
            .filter(|&(i, _)| i != index)
            .map(|(_, val)| *val)
            .collect::<Vec<u32>>();
        if is_safe(sub_report) {
            return true;
        }
    }
    false
}

fn part_two() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);
    assert_eq!(2, args.len());
    let file_path = args.get(1).unwrap();
    let file = fs::read_to_string(file_path).expect("Unable to read file");
    let matches = file
        .lines()
        .map(split_line)
        .map(is_safe_lenient)
        .filter(|x| *x)
        .count();
    println!("Compliant reports: {matches}");
}

fn main() -> std::io::Result<()> {
    part_one();
    part_two();
    Ok(())
}
