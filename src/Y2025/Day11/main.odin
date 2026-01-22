package main

import "core:fmt"
import "core:strings"
import "core:os"

Graph :: map[string][dynamic]string

parse :: proc(filename: string) -> Graph {
    data, ok := os.read_entire_file(filename, context.allocator)
	defer delete(data)
    it := string(data)
    graph: Graph
	for line in strings.split_lines_iterator(&it) {
        stuff, err := strings.split(line, ": ")
        u := stuff[0]
        for v in strings.split(stuff[1], " ") {
            inner, ok := graph[u]
            if !ok {
                graph[u] = make([dynamic]string)
            }
            append(&graph[u], v)
        }
	}
    return graph
}

num_paths :: proc(dp: ^map[string]int, graph: Graph, u: string, v: string) -> int {
    if u in dp {return dp[u]}
    if u == v {return 1}
    children, ok := graph[u]
    if !ok {return 0}
    res := 0
    for i in 0..<len(children) {
        res += num_paths(dp, graph, children[i], v)
    }
    dp[u] = res
    return res
}

main :: proc() {
    graph := parse("input.txt")
    dp: map[string]int
    defer delete(dp)
    p1 := num_paths(&dp, graph, "you", "out")
    clear(&dp)

    p2 := 1
    a, b := "dac", "fft"
    num := num_paths(&dp, graph, a, b)
    if num == 0 {
        a, b = b, a
        clear(&dp)
    }
    p2 *= num_paths(&dp, graph, a, b)
    clear(&dp)
    p2 *= num_paths(&dp, graph, "svr", a)
    clear(&dp)
    p2 *= num_paths(&dp, graph, b, "out")

    fmt.println(p1, p2)
}

