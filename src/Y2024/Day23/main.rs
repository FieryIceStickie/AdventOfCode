use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

type Graph = HashMap<String, HashSet<String>>;
type Counter = HashMap<String, i32>;

fn main() {
    let graph = parse("input.txt");
    let (p1, p2) = solve(graph);
    println!("{p1} {p2}")
}

fn parse(filename: &str) -> Graph {
    let contents = fs::read_to_string(filename).expect("Bro did not cook");
    let mut graph: Graph = HashMap::new();
    for line in contents.lines() {
        let replace = line.replace("t", "T");
        let mut line = replace.split("-");
        let mut u = line.next().expect("Bro did not cook").to_string();
        let mut v = line.next().expect("Bro did not cook").to_string();
        if v < u {
            (u, v) = (v, u)
        }
        graph.entry(u).or_default().insert(v);
    }
    graph
}

fn solve(graph: Graph) -> (i32, String) {
    let mut p1 = 0;
    let mut counts: Counter = HashMap::new();

    for (u, n1) in graph.iter() {
        for v in n1.iter() {
            for w in graph.get(v).unwrap_or(&HashSet::new()).iter() {
                if n1.contains(w) {
                    *(counts.entry(u.clone()).or_default()) += 1;
                    *(counts.entry(v.clone()).or_default()) += 1;
                    *(counts.entry(w.clone()).or_default()) += 1;
                    if u.starts_with("T") { p1 += 1; }
                }
            }
        }
    }

    let mut network_keys = counts
        .iter()
        .filter_map(|(k, v)| if *v == 66 { Some(k) } else { None })
        .cloned()
        .collect::<Vec<_>>();
    network_keys.sort();
    let p2 = network_keys.join(",");
    (p1, p2)
}
