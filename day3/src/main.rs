use std::{env, fs};

use regex::Regex;

fn get_functions(text: &str) -> Vec<&str> {
    let re = Regex::new(r"[a-z][a-z0-9_']+\(([0-9]+,[0-9]+)?\)").unwrap();
    re.find_iter(text).map(|m| m.as_str()).collect()
}

fn compute(instruction: &&str) -> u32 {
    let numbers = Regex::new(r"[0-9]+").unwrap();
    let mut product = 1;
    numbers
        .find_iter(instruction)
        .for_each(|val| product *= val.as_str().trim().parse::<u32>().unwrap());
    product
}

fn part_one() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);
    assert_eq!(2, args.len());
    let file_path = args.get(1).unwrap();
    let file = fs::read_to_string(file_path).expect("Unable to read file");
    let mut total = 0;
    get_functions(file.as_str())
        .iter()
        .filter(|f| f.starts_with("mul("))
        .map(compute)
        .for_each(|result| total += result);
    println!("Total: {}", total);
}

fn part_two() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);
    assert_eq!(2, args.len());
    let file_path = args.get(1).unwrap();
    let file = fs::read_to_string(file_path).expect("Unable to read file");
    let mut total = 0;
    let mut do_mul = true;
    get_functions(file.as_str()).iter().for_each(|f| {
        if f.contains("do(") {
            do_mul = true;
        } else if f.contains("don't(") {
            do_mul = false;
        } else if f.starts_with("mul(") && do_mul {
            total += compute(f);
        }
    });
    println!("Total: {}", total);
}

fn main() -> std::io::Result<()> {
    part_one();
    part_two();
    Ok(())
}
