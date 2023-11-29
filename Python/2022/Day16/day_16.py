import re
from functools import cache
import networkx as nx


def parser(filename: str):
    with open(filename, 'r') as file:
        valve_map = nx.Graph()
        valve_info = []
        for line in file.read().splitlines():
            valve, flowrate = re.match(r'Valve (\w{2}).+?=(\d+)', line).groups()
            connected = re.search(r'; tunnels? leads? to valves? (.+)', line).group(1).split(', ')
            valve_info.append((valve, int(flowrate), connected))
        valves, _, c = zip(*valve_info)
        valve_map.add_nodes_from(valves)
        for v, f, c in valve_info:
            valve_map.nodes[v]['flowrate'] = f
            valve_map.add_edges_from([(v, i) for i in c])
        return valve_map


def part_a_solver(valve_map: nx.Graph):
    flowrates = {n: f for n, f in valve_map.nodes.data('flowrate') if f}
    min_paths = nx.floyd_warshall(valve_map)
    @cache
    def dfs(valve, time, opened):
        pressure = 0
        for n, f in flowrates.items():
            if n in opened:
                continue
            if time - min_paths[valve][n] >= 1:
                new_time = time - min_paths[valve][n] - 1
                new_opened = tuple(sorted((*opened, n)))
                pressure = max(pressure, dfs(n, new_time, new_opened) + new_time*f)
        return pressure
    return int(dfs('AA', 30, ()))


def part_b_solver(valve_map: nx.Graph):
    flowrates = {n: f for n, f in valve_map.nodes.data('flowrate') if f}
    min_paths = nx.floyd_warshall(valve_map)

    @cache
    def dfs(valve, time, opened):
        pressure = 0
        best_opened = ()
        for n, f in flowrates.items():
            if n in opened:
                continue
            if time - min_paths[valve][n] >= 1:
                new_time = time - min_paths[valve][n] - 1
                new_opened = tuple(sorted((*opened, n)))
                new_pressure, new_valves = dfs(n, new_time, new_opened)
                if new_pressure + new_time * f > pressure:
                    pressure = new_pressure + new_time * f
                    best_opened = new_valves + (n,)
        return pressure, best_opened

    p, o = dfs('AA', 26, ())
    return int(p + dfs('AA', 26, o)[0])


if __name__ == '__main__':
    inputs = parser('day_16.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
