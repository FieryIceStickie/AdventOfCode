use std::fs;
extern crate z3;
use std::cmp::min;
use std::collections::HashMap;
use z3::{Optimize, ast::Int};

#[derive(Debug)]
struct Machine {
    config: u16,
    buttons: Vec<u16>,
    joltages: Vec<u16>,
}

fn parse_line(line: &str) -> Machine {
    let mut config = 0;
    let mut buttons = Vec::new();
    let mut joltages = Vec::new();
    for part in line.split(" ") {
        match part.chars().next() {
            Some('[') => {
                config = part[1..part.len() - 1]
                    .chars()
                    .enumerate()
                    .map(|(i, v)| if v == '#' { 1 << i } else { 0 })
                    .sum();
            }
            Some('(') => {
                buttons.push(
                    part[1..part.len() - 1]
                        .split(",")
                        .map(|i| 1 << i.parse::<u8>().unwrap())
                        .sum(),
                );
            }
            Some('{') => {
                joltages = part[1..part.len() - 1]
                    .split(",")
                    .map(|i| i.parse::<u16>().unwrap())
                    .collect();
            }
            _ => panic!("joever"),
        }
    }
    Machine {
        config,
        buttons,
        joltages,
    }
}

fn parse(filename: &str) -> Vec<Machine> {
    let contents = fs::read_to_string(filename).expect("Bro did not cook");
    contents.lines().map(parse_line).collect()
}

fn solve_p1(machine: &Machine) -> u32 {
    let mut combos = HashMap::<u16, u32>::new();
    combos.insert(machine.config, 0);
    for button in &machine.buttons {
        let new_combos: HashMap<u16, u32> =
            combos.iter().map(|(k, v)| (k ^ button, v + 1)).collect();
        for (k, v) in new_combos {
            combos.entry(k).and_modify(|w| *w = min(v, *w)).or_insert(v);
        }
    }
    *combos.get(&0).unwrap_or(&42069)
}

fn solve_p2(machine: &Machine) -> u64 {
    let solver = Optimize::new();
    let variables: Vec<Int> = (0..machine.buttons.len())
        .map(|i| Int::fresh_const(&i.to_string()))
        .collect();
    for (idx, joltage) in machine.joltages.iter().enumerate() {
        let constraint: Int = (0..machine.buttons.len())
            .filter(|i| (machine.buttons[*i] >> idx) & 1 == 1)
            .map(|i| variables[i].clone())
            .sum();
        solver.assert(&constraint.eq(*joltage));
    }
    for variable in &variables {
        solver.assert(&variable.ge(0));
    }
    let handle: Int = variables.iter().cloned().sum();
    solver.minimize(&handle);
    solver.check(&[]);
    let Some(model) = solver.get_model() else {
        panic!("cooked")
    };
    model.eval(&handle, true).unwrap().as_u64().unwrap()
}

fn solve(machines: Vec<Machine>) -> (u32, u64) {
    let mut p1 = 0;
    let mut p2 = 0;
    for machine in machines {
        p1 += solve_p1(&machine);
        p2 += solve_p2(&machine);
    }
    (p1, p2)
}

fn main() {
    let graph = parse("input.txt");
    let (p1, p2) = solve(graph);
    println!("{p1} {p2}")
}
