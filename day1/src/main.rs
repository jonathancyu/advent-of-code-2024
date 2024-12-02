use std::{
    collections::BinaryHeap,
    env,
    fs::{self, File},
    io::{BufReader, Read},
    iter::{from_fn, zip},
};
fn part_one() {
    let args: Vec<String> = env::args().collect();
    println!("{:?}", args);
    assert_eq!(2, args.len());
    let file_path = args.get(1).unwrap();
    let lines = fs::read_to_string(file_path).expect("Unable to read file");
    let mut left_heap = BinaryHeap::<u32>::new();
    let mut right_heap = BinaryHeap::<u32>::new();
    for line in lines.lines() {
        let split: Vec<&str> = line.split_whitespace().collect();
        assert_eq!(2, split.len());
        let left = split[0].trim().parse::<u32>().unwrap();
        let right = split[1].trim().parse::<u32>().unwrap();
        left_heap.push(left);
        right_heap.push(right);
    }

    println!("{}", left_heap.len());

    assert_eq!(left_heap.len(), right_heap.len());
    let total: u32 = zip(
        from_fn(move || left_heap.pop()),
        from_fn(move || right_heap.pop()),
    )
    .map(|(l, r)| l.abs_diff(r))
    .sum();

    println!("Total: {total}");
}

fn main() -> std::io::Result<()> {
    part_one();
    Ok(())
}
